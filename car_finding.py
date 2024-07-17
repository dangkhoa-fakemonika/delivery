import pygame
from game_classes import Board


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
#     [0, 0, 0, 0, -1, 5, -1, 0, -1, 0],
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
board = [
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0, -1, -1,  0,  0, -1,  0, -1,  0,  0],
    [ 0, -1, -1,  0,  0,  0,  0, -1,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0, -1,  0, -1, -1,  0,  0,  0],
    [ 0, -1,  -1,  0,  0,  0,  0, -1, -1,  0],
    [ 0,  0,  -1, -1,  0, -1,  0, -1,  0,  0],
    [-1, -1,  -1, -1,  0,  0,  0,  0,  0,  0],
    [100, 0, 50, 0, 20, -1, 10, -1,  0,  0],
    [ 0,  0,  0,  0,  0,  0, -1,  0,  0,  0],
]

s_pos = (0, 0)
e_pos = (9, 0)

game_board = Board(10, 10, s_pos, e_pos)
game_board.board_data = board

screen_res = (1020, 720)
fps = 12
pyclock = pygame.time.Clock()
game_board.box_config(screen_res)

pygame.init()
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("lmao")

get_path, get_expansion = game_board.configure_algorithm('bfs')

game_board.board_layout_init()  # Uncomment to load textures

if get_path is None:
    get_path = []

path_steps = 0
expansion_steps = 0
frame = 0
auto_move = False

running = True
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
            if event.key == pygame.K_d and path_steps < len(get_path):
                path_steps += 1
            if event.key == pygame.K_SPACE:  # Space to autoplay
                auto_move = not auto_move
                if auto_move:
                    print("\rPlaying...", end='', flush=True)
                else:
                    print("\rPlayback stopped.", end='', flush=True)

    if frame == fps:
        frame = 0

    if auto_move:
        path_steps += 1
        if path_steps == len(get_path):
            path_steps = 0

    game_board.board_search(screen, get_expansion, expansion_steps)
    game_board.board_display(screen, get_path, path_steps)
    pygame.display.flip()

pygame.quit()
