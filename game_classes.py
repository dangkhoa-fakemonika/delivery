from typing import Literal
import search_algorithms as algo
import display_setup as ds


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
        st = ds.draw_step(screen, self.board_data, path, step, self.fuel_limit, self.box_size, self.offset_x, self.offset_y)
        if step != 0 and st < len(path) - 1:
            ds.draw_board_data(screen, self.board_data, path[st], self.end, self.size, self.box_size, self.offset_x, self.offset_y)
        else:
            ds.draw_board_data(screen, self.board_data, self.end, self.end, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, level, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_search(self, screen, path, step):
        ds.draw_expansion(screen, path, step, self.box_size, self.offset_x, self.offset_y)

    def board_layout_init(self):
        self.board_layout = ds.generate_layout(self.board_data, self.size)

    def board_display_layout(self, screen, path, step, level):
        st = ds.draw_step(screen, self.board_data, path, step, self.fuel_limit, self.box_size, self.offset_x, self.offset_y)
        if step != 0 and st < len(path) - 1:
            ds.draw_assets_board_data(screen, self.board_data, self.board_layout, path[st], self.end, self.size, self.box_size, algo.configure_path(path[st], path[st + 1]) ,self.offset_x, self.offset_y)
        else:
            ds.draw_assets_board_data(screen, self.board_data, self.board_layout, self.end, self.end, self.size, self.box_size, 0 ,self.offset_x, self.offset_y)
        # ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, level, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_display(self, screen, path, step, level):
        if self.board_layout is None:
            self.board_display_default(screen, path, step, level)
        else:
            self.board_display_layout(screen, path, step, level)

    def import_board_data(self, filename):
        # Do the import data here
        fs = open(filename, "r")
        s_pos = (0, 0)
        e_pos = (0, 0)

        rows, cols, time, fuel = fs.readline().split()
        adj = []
        for i in range(int(rows)):
            line = fs.readline().split()
            temp = [int(i) if i.isnumeric() or (i.lstrip('-')).isnumeric() else i for i in line]
            if 'S' in temp:
                s_pos = (i, temp.index('S'))
                temp[s_pos[1]] = 0

            if 'G' in temp:
                e_pos = (i, temp.index('G'))
                temp[e_pos[1]] = 0
                print(e_pos)

            adj.append(temp)
        fs.close()

        self.board_data = adj
        self.start = s_pos
        self.end = e_pos
        self.time_limit = int(time) if time != "inf" else float('inf')
        self.fuel_limit = int(fuel) if fuel != "inf" else float('inf')
        self.size = (len(adj), len(adj[0]))

    def configure_algorithm(self, algorithm: str | Literal['bfs', 'dfs', 'ucs', 'gbfs', 'a*', 'lvl2', 'lvl3'] = 'bfs'):
        if algorithm == 'bfs':
            return algo.BFS(self.board_data, self.start, self.end)
        if algorithm == 'dfs':
            return algo.DFS(self.board_data, self.start, self.end)
        if algorithm == 'ucs':
            return algo.UCS(self.board_data, self.start, self.end)
        if algorithm == 'gbfs':
            return algo.GBFS(self.board_data, self.start, self.end)
        elif algorithm == 'a*':
            return algo.A_STAR(self.board_data, self.start, self.end)
        if algorithm == 'lvl2':
            return algo.LVL2_UCS(self.board_data, self.start, self.end, self.time_limit)
        if algorithm == 'lvl3':
            return algo.LVL3(self.board_data, self.start, self.end, self.time_limit, self.time_limit)
