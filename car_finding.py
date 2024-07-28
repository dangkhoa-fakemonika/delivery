import pygame
from game_classes import Board
import search_algorithms as algo


if __name__ == '__main__':
    # file_input = input('Enter the input file name (ex: input.txt): ')
    # custom = input('Use custom input? [Y/N] ')

    file_input = "input/input_textures_test_1"
    custom = 'y'

    game_board = Board()
    game_board.import_board_data(file_input)

    # Initializing
    screen_res = (1020, 720)
    fps = 12
    pyclock = pygame.time.Clock()
    game_board.box_config(screen_res)
    path_steps = 0
    expansion_steps = 0
    frame = 0
    auto_move = False
    running = True

    levels = ('bfs', 'dfs', 'ucs', 'gbfs', 'a*', 'lvl2', 'lvl3', 'lvl4')
    level = 'bfs'

    pygame.init()
    screen = pygame.display.set_mode(screen_res)
    pygame.display.set_caption("Delivery System")
    game_board.run_algorithms()

    get_path = game_board.configure_algorithm(level)
    cost = algo.generate_time_cost(game_board.board_data, get_path, level)

    if custom.lower() == 'y':
        game_board.board_layout_init()

    algorithm = levels.index(level)

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
                if event.key == pygame.K_a and path_steps >= 1 and get_path is not None:
                    path_steps -= 1
                if event.key == pygame.K_d and path_steps < cost and get_path is not None:
                    path_steps += 1
                if event.key == pygame.K_SPACE and get_path is not None:  # Space to autoplay
                    auto_move = not auto_move
                    if auto_move:
                        print("\rPlaying...", end='', flush=True)
                    else:
                        print("\rPlayback stopped.", end='', flush=True)

                if event.key == pygame.K_LEFT:
                    algorithm -= 1
                    if algorithm < 0:
                        algorithm = 7
                    path_steps = 0
                    expansion_steps = 0
                    # Change algorithm here
                    level = levels[algorithm]
                    get_path = game_board.configure_algorithm(level)
                    cost = algo.generate_time_cost(game_board.board_data, get_path, level)

                if event.key == pygame.K_RIGHT:
                    algorithm += 1
                    if algorithm > 7:
                        algorithm = 0
                    path_steps = 0
                    expansion_steps = 0
                    # Change algorithm here
                    level = levels[algorithm]
                    get_path = game_board.configure_algorithm(level)
                    cost = algo.generate_time_cost(game_board.board_data, get_path, level)

        if frame == fps:
            frame = 0

        if auto_move:
            path_steps += 1
            if path_steps > cost:
                path_steps = 0

        game_board.board_display(screen, get_path, path_steps, level)
        pygame.display.flip()

    pygame.quit()
