import random

from car_path_finding.car_finding.delivery import lv4 as l4


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


test = GridLV4()
#
b = [
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1],
    [-0,  0,  0,  0,  0,  0,  0],
    [-1, -1, -1,  0, -1, -1, -1],
    [-1, -1, -1,  0, -1, -1, -1]
]
#
# b = [
#     [0, -1, -1, -1, -1, -1, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, -1, -1, -1, -1, -1, 0]
# ]

# b = [
#     [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
#     [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
#     [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
# ]
#
s = [(2, 1), (2, 5)]
g = [(2, 6), (4, 3)]

# s = [(1, 1), (1, 3), (1, 5), (1, 7), (1, 9), (5, 8), (5, 6), (5, 4), (5, 2), (5, 0)]
# g = [(6, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (6, 8), (6, 6), (6, 4), (6, 2)]

test.get_initial_data(data=b, starts=s, goals=g)
test.algo1()
print(test.paths)
