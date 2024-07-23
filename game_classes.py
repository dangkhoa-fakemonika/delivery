from typing import Literal
import search_algorithms as algo
import display_setup as ds


class Board:
    def __init__(self, grid_width, grid_height, start_pos, end_pos):  # Constructor
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

    def board_display_default(self, screen, path, step):
        st = ds.draw_step(screen, self.board_data, path, step, self.box_size, self.offset_x, self.offset_y)
        if step != 0 and st < len(path) - 1:
            ds.draw_board_data(screen, self.board_data, path[st], self.end, self.size, self.box_size, self.offset_x, self.offset_y)
        else:
            ds.draw_board_data(screen, self.board_data, self.start, self.end, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_search(self, screen, path, step):
        ds.draw_expansion(screen, path, step, self.box_size, self.offset_x, self.offset_y)

    def board_layout_init(self):
        self.board_layout = ds.generate_layout(self.board_data, self.size)

    def board_display_layout(self, screen, path, step):
        st = ds.draw_step(screen, self.board_data, path, step, self.fuel_limit, self.box_size, self.offset_x, self.offset_y)
        if step != 0 and st < len(path) - 1:
            ds.draw_assets_board_data(screen, self.board_data, self.board_layout, path[st], self.end, self.size, self.box_size, algo.configure_path(path[st], path[st + 1]) ,self.offset_x, self.offset_y)
        else:
            ds.draw_assets_board_data(screen, self.board_data, self.board_layout, self.start, self.end, self.size, self.box_size, 0 ,self.offset_x, self.offset_y)
        # ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_display(self, screen, path, step):
        if self.board_layout is None:
            self.board_display_default(screen, path, step)
        else:
            self.board_display_layout(screen, path, step)

    def import_board_data(self, filename):
        f = open(filename, 'r')
        # Do the import data here

    def configure_algorithm(self, algorithm: Literal['bfs', 'dfs', 'ucs', 'gbfs', 'a*', 'lvl2', 'lvl3'] = 'bfs', limit=float('inf'), fuel_cap=float('inf')):
        if algorithm == 'bfs':
            return algo.BFS(self.board_data, self.start, self.end)
        if algorithm == 'dfs':
            return algo.DFS(self.board_data, self.start, self.end)
        if algorithm == 'ucs':
            return algo.UCS(self.board_data, self.start, self.end)
        if algorithm == 'gbfs' or algorithm == 'a*':
            return algo.BestFS(self.board_data, self.start, self.end)
        elif algorithm == 'a*':
            # Implement A* here
            pass
        if algorithm == 'lvl2':
            return algo.LVL2_UCS(self.board_data, self.start, self.end, limit)
        if algorithm == 'lvl3':
            self.time_limit = limit
            self.fuel_limit = fuel_cap
            return algo.LVL3(self.board_data, self.start, self.end, limit, fuel_cap)
        
