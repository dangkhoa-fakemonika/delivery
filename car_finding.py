import pygame
from game_classes import Board
import search_algorithms as algo


def move_path(block: tuple[int, int], move: str) -> tuple[int, int]:
    if move == "w":
        return block[0] - 1, block[1]
    elif move == "s":
        return block[0] + 1, block[1]
    elif move == "d":
        return block[0], block[1] - 1
    elif move == "a":
        return block[0], block[1] + 1
    else:
        return block


size_of_grid = (10, 10)

# Case 1
# board = [
#     [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
#     [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
#     [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
#     [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
#     [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
#     [0, 0, "F10", 0, -1, 5, -1, 0, -1, 0],
#     [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
#     [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
#     [0, 0, 5, 0, 0, 0, -1, -1, -1, 0]
# ]
#
# s_pos = (1, 1)
# e_pos = (8, 7)

# Illusion of choice
# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [0, -1, 0, -1, 0, -1, 0, -1, 0, 0],
#     [100, -1, 50, -1, 20, -1, 10, -1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]

# Assets test
# Test 1:
# board = [
#     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
#     [ 0, -1, -1,  0,  0, -1,  0, -1,  0,  0],
#     [ 0, -1, -1,  0,  0,  0,  0, -1,  0,  0],
#     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
#     [ 0,  0,  0, -1,  0, -1, -1,  0,  0,  0],
#     [ 0, -1,  -1,  0,  0,  0,  0, -1, -1,  0],
#     [ 0,  0,  -1, -1,  0, -1,  0, -1,  0,  0],
#     [-1, -1,  -1, -1,  0,  0,  0,  0,  0,  0],
#     [100, 0, 50, 0, 20, -1, 10, -1,  0,  0],
#     [ 0,  0,  0,  0,  0,  0, -1,  0,  0,  0],
# ]

# s_pos = (0, 0)
# e_pos = (9, 0)
#////////////////////////////////////////////////////////////////////////
# Test 2: Car can now re-visited tile that have already visited by another path
# s_pos = (0, 0)
# e_pos = (9, 0)
# For example t(time limit) = 63, the car can move straight down from the start to reach the goal tile with the exact time of 63
# But with t = 62, the previous search path stop right before the goal because of exceeding time limit, so we find an alternative path,
# this time to be the optimal path it has to revisited tiles at position (0, 7) and (0, 8)

board = [
    [0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
    [0, -1, -1, -1, 0, -1, -1, 0, 0, 0],
    [0, -1, 0, -1, 0, -1, -1, 0, 0, 0],
    [-1, -1, 0, -1, 0, 0, 0, 0, -1, 0],
    [0, -1, 0, -1, -1, -1, 0, -1, 0, 0],
    [0, -1, 0, -1, -1, -1, 0, 0, -1, 0],
    [54, -1, 51, -1, 0, -1, 0, -1, 0, 0],
    [0, 0, 0, 0, 0, -1, 0, -1, 0, 0],
    [0, -1, 50, -1, 20, -1, 10, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

s_pos = (0, 0)
e_pos = (9, 0)

# Test3 for lvl3
#
# board = [
#     [0,    -1, "F1",  0, 0, -1, "F3", 0, 0, 0],
#     [0,    -1,    0, -1, 0, -1,    0, -1, 0, 0],
#     [0,    -1,    0, -1, 0, -1,    0, -1, 0, 0],
#     [0,    -1,    0, -1, 0, -1,    0, -1, 0, 0],
#     [0,    -1,    0, -1, 0, -1,    0, -1, 0, 0],
#     [0,    -1,    0, -1, 0, -1,    0, -1, 0, 0],
#     [10, "F4",   10, -1, 0, 10,    0, -1, 0, 0],
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1, 0],
#     [0, -1, 50, -1, 20, -1, 10, -1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# ]
#
# s_pos = (0, 0)
# e_pos = (9, 0)

game_board = Board(10, 10, s_pos, e_pos)
game_board.board_data = board

screen_res = (1020, 720)
fps = 12
pyclock = pygame.time.Clock()
game_board.box_config(screen_res)
path_steps = 0
expansion_steps = 0
frame = 0
auto_move = False
running = True

levels = ('bfs', 'dfs', 'ucs', 'gbfs', 'a*')

level = 'bfs'

pygame.init()
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("lmao")
get_path, get_expansion = game_board.configure_algorithm(level)
# get_path, get_expansion = game_board.configure_algorithm('lvl2')
# get_path, get_expansion = game_board.configure_algorithm()
cost = algo.generate_time_cost(game_board.board_data, get_path)

algorithm = 0

# game_board.board_layout_init()  # Uncomment to load textures
# print(get_path)

if get_path is None:
    get_path = []
# print(game_board)

while running:
    screen.fill((0, 0, 0))
    ta = pyclock.tick(fps)
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC to quit
                running = False
                break
            if event.key == pygame.K_a and path_steps >= 1:
                path_steps -= 1
            if event.key == pygame.K_d and path_steps <= cost:
                path_steps += 1
            if event.key == pygame.K_SPACE:  # Space to autoplay
                auto_move = not auto_move
                if auto_move:
                    print("\rPlaying...", end='', flush=True)
                else:
                    print("\rPlayback stopped.", end='', flush=True)

            if event.key == pygame.K_LEFT and level not in ('lvl2', 'lvl3'):
                algorithm -= 1
                if algorithm < 0:
                    algorithm = 4
                path_steps = 0
                expansion_steps = 0
                # Change algorithm here
                level = levels[algorithm]
                get_path, get_expansion = game_board.configure_algorithm(level)
                cost = algo.generate_time_cost(game_board.board_data, get_path)

            if event.key == pygame.K_RIGHT and level not in ('lvl2', 'lvl3'):
                algorithm += 1
                if algorithm > 4:
                    algorithm = 0
                path_steps = 0
                expansion_steps = 0
                # Change algorithm here
                level = levels[algorithm]
                get_path, get_expansion = game_board.configure_algorithm(level)
                cost = algo.generate_time_cost(game_board.board_data, get_path)

    if frame == fps:
        frame = 0

    if auto_move:
        path_steps += 1
        if path_steps > cost:
            path_steps = 0

    # game_board.board_search(screen, get_expansion, expansion_steps, level)
    game_board.board_display(screen, get_path, path_steps, level)
    pygame.display.flip()

pygame.quit()
