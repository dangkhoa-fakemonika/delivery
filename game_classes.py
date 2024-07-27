from typing import Literal
import search_algorithms as algo
import display_setup as ds
import lv4 as l4
import random


class GridLV4:
    def __init__(self):
        self.grid_data: list[list[int]] | None = None
        self.starts: list[tuple[int, int]] | None = None
        self.goals: list[tuple[int, int]] | None = None
        self.paths: list[list[tuple[int, int]] | None] | None = None
        self.agents_count: int = 0
        self.main_time: float | int = float('inf')
        self.time_limit: float | int = float('inf')
        self.fuel_limit: float | int = float('inf')
        self.current_fuel: list[float | int] | None = None
        self.paying_toll: list[int | float] | None = None

    def init_path(self):
        for i in range(len(self.starts)):
            get_path = l4.LVL4(self.grid_data, self.starts[i], self.goals[i], self.time_limit, self.fuel_limit)
            if get_path is None:
                self.paths[i] = None
                continue
            timed_path = l4.get_timed_path(self.grid_data, get_path)
            print(timed_path)
            self.paths[i] = timed_path

        self.main_time = len(self.paths[0])

    def get_initial_data(self, data, starts, goals, time_limit=float('inf'), fuel_limit=float('inf')):
        self.grid_data = data
        self.starts = starts
        self.goals = goals
        self.agents_count = len(starts)
        self.paths = [[] for _ in range(self.agents_count)]
        self.time_limit = time_limit
        self.fuel_limit = fuel_limit
        self.current_fuel = [fuel_limit for _ in range(self.agents_count)]
        self.paying_toll = [0 for _ in range(self.agents_count)]

    def algo1(self):

        # From the start, initiate all new part of the goal
        # A goal will move through its next step if it is not blocked
        stalemate = True
        break_stalemate = False

        self.init_path()

        # Main agent can't reach goal
        if self.paths[0] is None:
            print("Can't really proceed.")
            return None

        # if self.main_time is float('inf'):
        #     self.main_time = 0
        t = 0
        while t < self.main_time:
            stalemate = True
            print("\n\nTime", t)
            if break_stalemate:
                print("Breaking stalemate.")
            print("Current path state:")
            for p in self.paths:
                print(p)

            for a in range(self.agents_count):
                print("Agent", a+1)
                if self.paths[a] is None:
                    continue

                print("Current location:", self.paths[a][t])

                # if self.paths[a][t] == (-1, -1):
                #     print("This agent is paying his debt of his afterlife.")
                #     self.paying_toll[a] = float('inf')
                #     self.paths[a].append((-1, -1))

                if self.paying_toll[a] > 0:  # Is waiting
                    print("Is paying road toll")
                    self.paying_toll[a] -= 1
                    continue
                elif str(self.grid_data[self.paths[a][t][0]][self.paths[a][t][1]]) > '0': # Will wait
                    self.paying_toll[a] = int(str(self.grid_data[self.paths[a][t][0]][self.paths[a][t][1]]).strip('F'))
                    continue

                if self.paths[a][t] == self.goals[a]:
                    if a != 0:
                        print("Goal reached, generating a new one.")
                        new_goal = self.goals[a]
                        new_path = None
                        can_locations = [(x, y) for x in range(len(self.grid_data)) for y in range(len(self.grid_data[0])) if
                                         (new_goal in self.goals or str(self.grid_data[x][y]) != '-1'
                                          or new_goal in [self.paths[_][t] for _ in range(self.agents_count)])
                                         ]
                        while new_path is None:
                            new_goal = random.choice(can_locations)
                            new_path = l4.LVL4(self.grid_data, self.goals[a], new_goal, self.time_limit, self.current_fuel[a])
                            if new_path is None:
                                can_locations.remove(new_goal)

                        self.paths[a].extend(l4.get_timed_path(self.grid_data, new_path))
                        print("Goal is generated at:", new_goal)
                        self.goals[a] = new_goal
                    if a == 0:
                        return self.paths

                # Find candidate directions that current agent can move to
                cans = l4.generate_candidates_LVL4(self.paths[a][t], self.grid_data, self.goals[a], break_stalemate)

                # Checking collision
                for va in range(a):
                    if self.paths[va] is not None:
                        if self.paths[va][t + 1] in cans:
                            cans.remove(self.paths[va][t + 1])
                for va in range(a + 1, self.agents_count):
                    if self.paths[va] is not None:
                        if self.paths[va][t] in cans:
                            cans.remove(self.paths[va][t])

                print("Candidates found: ", cans)

                # If the agent can't move
                if len(cans) == 0:
                    self.paths[a].insert(t, self.paths[a][t])
                    continue

                # If the agent can move to it's designated path
                elif self.paths[a][t + 1] in cans:
                    print("Normal movement to", self.paths[a][t+1])
                    self.current_fuel[a] -= 1
                    stalemate = False
                    continue

                # If the agent can't move to it's designated path, finding a "new" path to it
                else:
                    self.current_fuel[a] -= 1
                    best_path = []

                    cans_set = [
                        [_ for _ in cans if _ not in self.paths[a]], # New candidates
                        [_ for _ in cans if _ in self.paths[a]] # Old candidates
                    ]

                    # Minimal path changes
                    for cset in cans_set:
                        new_flag = False
                        for can in cset:
                            if str(self.grid_data[can[0]][can[1]]) == 'F':
                                temp_path = l4.LVL4(self.grid_data, can, self.goals[a], self.time_limit - t - 1, self.fuel_limit, self.fuel_limit)
                            else:
                                temp_path = l4.LVL4(self.grid_data, can, self.goals[a], self.time_limit - t - 1, self.fuel_limit, self.current_fuel[a])

                            if temp_path is None:
                                continue

                            if len(temp_path) <= len(best_path) or len(best_path) == 0:
                                best_path = temp_path
                                new_flag = True

                        if new_flag:
                            break

                    # No path can be selected or it wants to do nothing
                    if len(best_path) == 0 or best_path[0] == self.paths[a][t]:
                        print("Can't move")
                        self.paths[a].insert(t, self.paths[a][t])
                        continue

                    stalemate = False
                    # Rewrite its path
                    print("Can move with ", best_path)
                    self.paths[a][t+1:] = l4.get_timed_path(self.grid_data, best_path)
                    print("Moved to", best_path[0])

                    if a == 0:  # Main agent
                        self.main_time = len(self.paths[0])

                    # Re-fuel
                    if str(self.grid_data[self.paths[a][t][0]][self.paths[a][t][1]])[0] == 'F':
                        self.current_fuel[a] = self.fuel_limit
                    else:
                        self.current_fuel[a] -= 1

            t += 1
            break_stalemate = stalemate or (0 not in set(self.paying_toll) and len(self.paying_toll) > 1)

    def get_poss(self, time):
        if 0 <= time <= self.main_time + 1:
            return [self.paths[_][time] for _ in range(self.agents_count)]
        else:
            return self.goals


class Board:
    def __init__(self, grid_width = 0, grid_height = 0, start_pos = (0, 0), end_pos = (0, 0)):  # Constructor
        self.size = (grid_width, grid_height)
        self.board_data = [[0 for _ in range(grid_width)] for __ in range(grid_height)]
        self.start = start_pos
        self.end = end_pos
        self.box_size = 1
        self.offset_x = 0  # Screen X
        self.offset_y = 0  # Screen Y
        self.time_limit = float('inf')
        self.fuel_limit = float('inf')
        self.board_layout = None
        self.algorithm_paths = None
        self.lv4_data = GridLV4()

    def __str__(self):  # To use print(game_board)
        res = f"""
Size: {self.size}
Start: {self.start}, End :{self.end}
Screen offset: ({self.offset_x, self.offset_y})

"""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                res += f"{self.board_data[x][y]: <3}"
            res += "\n"
        return res

    def box_config(self, screen_res: tuple[int, int]):
        self.box_size, self.offset_x, self.offset_y = ds.get_box_config(screen_res, self.size)

    def board_display_default(self, screen, path, step, level):
        if level != 'lvl4':
            st = ds.draw_step(screen, level, self.board_data, path, step, self.fuel_limit, self.box_size, self.offset_x, self.offset_y)
            if step != 0 and st < len(path) and path is not None:
                ds.draw_board_data(screen, level, self.board_data, path[st], self.end, self.size, self.box_size, self.offset_x, self.offset_y)
            else:
                ds.draw_board_data(screen, level, self.board_data, self.start, self.end, self.size, self.box_size, self.offset_x, self.offset_y)
        else:
            print(self.lv4_data.get_poss(step))
            ds.draw_lv4_step(screen, self.lv4_data.agents_count, self.board_data, path, step, self.fuel_limit, self.box_size, self.offset_x, self.offset_y)
            ds.draw_lv4_board_data(screen, self.lv4_data.agents_count, self.board_data, self.lv4_data.get_poss(step), self.lv4_data.goals, self.size, self.box_size, self.offset_x, self.offset_y)

        ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, level, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_search(self, screen, path, step):
        ds.draw_expansion(screen, path, step, self.box_size, self.offset_x, self.offset_y)

    def board_layout_init(self):
        self.board_layout = ds.generate_layout(self.board_data, self.size)

    def board_display_layout(self, screen, path, step, level):
        st = ds.draw_step(screen, level, self.board_data, path, step, self.fuel_limit, self.box_size, self.offset_x, self.offset_y)
        if step != 0 and st < len(path) and path is not None:
            ds.draw_assets_board_data(screen, level, self.board_data, self.board_layout, path[st], self.end, self.size, self.box_size, algo.configure_path(path[st], path[st + 1]) ,self.offset_x, self.offset_y)
        else:
            ds.draw_assets_board_data(screen, level, self.board_data, self.board_layout, self.start, self.end, self.size, self.box_size, 0 ,self.offset_x, self.offset_y)
        # ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, level, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_display(self, screen, path, step, level):
        if self.board_layout is None:
            self.board_display_default(screen, path, step, level)
        else:
            self.board_display_layout(screen, path, step, level)

    def import_board_lv4(self, filename):
        fs = open(filename, "r")

        s_list = [(-1, -1)] * 10
        g_list = [(-1, -1)] * 10

        n, m, t, f = fs.readline().split()
        adj = []
        for _ in range(int(n)):
            line = fs.readline().split()
            temp = [int(i) if i.isnumeric() or (i.lstrip('-')).isnumeric() else i for i in line]

            for s in temp:
                if isinstance(s, str):
                    if s == 'S':
                        s_list[0] = (_, temp.index(s))
                    elif s[0] == 'S':
                        pos = int(s[-1])
                        s_list[pos] = (_, temp.index(s))

            for g in temp:
                if isinstance(g, str):
                    if g == 'G':
                        g_list[0] = (_, temp.index(g))
                    elif g[0] == 'G':
                        pos = int(g[-1])
                        g_list[pos] = (_, temp.index(g))

            adj.append(temp)
        fs.close()

        s_list = list(filter(lambda x: x != (-1, -1), s_list))
        g_list = list(filter(lambda x: x != (-1, -1), g_list))

        self.lv4_data.get_initial_data(self.board_data, s_list, g_list, self.time_limit, self.fuel_limit)

    def import_board_data(self, filename):
        # Do the import data here
        fs = open(filename, "r")
        s_pos = (0, 0)
        e_pos = (0, 0)

        rows, cols, time, fuel = fs.readline().split()
        adj = []
        for i in range(int(rows)):
            line = fs.readline().split()
            temp = [int(i) if i.isnumeric() or (i.lstrip('-')).isnumeric()
                    else 0 if len(i) == 2 and i[0] != 'F' else i for i in line]
            if 'S' in temp:
                s_pos = (i, temp.index('S'))
                temp[s_pos[1]] = 0

            if 'G' in temp:
                e_pos = (i, temp.index('G'))
                temp[e_pos[1]] = 0
                # print(e_pos)

            adj.append(temp)
        fs.close()

        self.board_data = adj
        self.start = s_pos
        self.end = e_pos
        self.time_limit = int(time) if time != "inf" else float('inf')
        self.fuel_limit = int(fuel) if fuel != "inf" else float('inf')
        self.size = (len(adj), len(adj[0]))

        self.import_board_lv4(filename)

    def run_algorithms(self):
        print("Running algorithm...", end="")
        self.algorithm_paths = []
        self.algorithm_paths.append(algo.BFS(self.board_data, self.start, self.end)[0])
        print("\r BFS is running...", end="")
        self.algorithm_paths.append(algo.DFS(self.board_data, self.start, self.end)[0])
        print("\r DFS is running...", end="")
        self.algorithm_paths.append(algo.UCS(self.board_data, self.start, self.end)[0])
        print("\r UCS is running...", end="")
        self.algorithm_paths.append(algo.GBFS(self.board_data, self.start, self.end)[0])
        print("\r A* is running...", end="")
        self.algorithm_paths.append(algo.A_STAR(self.board_data, self.start, self.end)[0])
        print("\r LV2 is running...", end="")
        self.algorithm_paths.append(algo.LVL2_UCS(self.board_data, self.start, self.end, self.time_limit)[0])
        print("\r LV3 is running...", end="")
        self.algorithm_paths.append(algo.LVL3_UCS(self.board_data, self.start, self.end, self.time_limit, self.fuel_limit)[0])
        # print("\r LV4 is running...", end="")
        # self.lv4_data.algo1()
        # self.algorithm_paths.append(self.lv4_data.paths)
        print("\rFinished!")

    def configure_algorithm(self, algorithm: str | Literal['bfs', 'dfs', 'ucs', 'gbfs', 'a*', 'lvl2', 'lvl3'] = 'bfs'):
        if algorithm == 'bfs':
            return self.algorithm_paths[0]
        if algorithm == 'dfs':
            return self.algorithm_paths[1]
        if algorithm == 'ucs':
            return self.algorithm_paths[2]
        if algorithm == 'gbfs':
            return self.algorithm_paths[3]
        elif algorithm == 'a*':
            return self.algorithm_paths[4]
        if algorithm == 'lvl2':
            return self.algorithm_paths[5]
        if algorithm == 'lvl3':
            return self.algorithm_paths[6]
        # if algorithm == 'lvl4':
        #     return self.algorithm_paths[7]
