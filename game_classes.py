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

    def board_display(self, screen, path, step):
        if step < len(path) - 1 != 0:
            ds.draw_board_data(screen, self.board_data, path[step], self.end, self.size, self.box_size, algo.configure_path(path[step], path[step + 1]) ,self.offset_x, self.offset_y)
        else:
            ds.draw_board_data(screen, self.board_data, self.end, self.end, self.size, self.box_size, 0 ,self.offset_x, self.offset_y)
        ds.draw_step(screen, path, step, self.box_size, self.offset_x, self.offset_y)
        ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def board_search(self, screen, path, step):
        ds.draw_expansion(screen, path, step, self.box_size, self.offset_x, self.offset_y)

    def board_display_layout(self, screen, path, step):
        if step < len(path) - 1 != 0:
            ds.draw_assets_board_data(screen, self.board_data, path[step], self.end, self.size, self.box_size, algo.configure_path(path[step], path[step + 1]) ,self.offset_x, self.offset_y)
        else:
            ds.draw_assets_board_data(screen, self.board_data, self.end, self.end, self.size, self.box_size, 0 ,self.offset_x, self.offset_y)
        # ds.draw_step(screen, path, step, self.box_size, self.offset_x, self.offset_y)
        # ds.draw_grid(screen, self.size, self.box_size, self.offset_x, self.offset_y)
        ds.draw_info_box(screen, self.start, self.end, self.time_limit, self.fuel_limit, self.size, self.box_size, self.offset_x, self.offset_y)

    def import_board_data(self, filename):
        f = open(filename, 'r')
        # Do the import data here

    def configure_algorithm(self, algorithm: Literal['bfs', 'dfs', 'ucs', 'gbfs', 'a*'] = 'bfs', limit=float('inf')):
        if algorithm == 'bfs':
            return algo.BFS(self.board_data, self.start, self.end)
        if algorithm == 'dfs':
            return algo.BFS(self.board_data, self.start, self.end)
        if algorithm == 'ucs':
            # Implement UCS here
            pass
        if algorithm == 'gbfs' or 'a*':
            return algo.BestFS(self.board_data, self.start, self.end, limit)
        if algorithm == 'a*':
            # Implement A* here
            pass
