import random

import pygame


def get_box_config(res: tuple[int, int], grid_size: tuple[int, int]):
    width = res[0] - 100
    height = res[1] - 100

    box_width = min(width // grid_size[0], height // grid_size[1])
    offset_x = (res[0] - box_width * grid_size[0]) // 2 - 150
    offset_y = (res[1] - box_width * grid_size[1]) // 2

    print(offset_x, offset_y)
    return box_width, offset_x, offset_y


def draw_grid(scr: pygame.Surface, grid_size, box_width, offset_x, offset_y):
    for it in range(grid_size[0]):
        for ii in range(grid_size[1]):
            pygame.draw.rect(scr, (255, 255, 255),
                             (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width), width=1)


def draw_board_data(scr: pygame.Surface, board_data, start, end, grid_size, box_width, direction, offset_x=0,
                    offset_y=0):
    display_font = pygame.font.Font('freesansbold.ttf', box_width // 2)

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if str(board_data[ii][it]) == '-1':
                pygame.draw.rect(scr, (128, 128, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
            if str(board_data[ii][it]) > '0':
                box_value = display_font.render(str(board_data[ii][it]), True, (255, 255, 255))
                box_value_rect = box_value.get_rect()
                box_value_rect.center = (
                    offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)
                pygame.draw.rect(scr, (10, 200, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
                scr.blit(box_value, box_value_rect)

    pygame.draw.rect(scr, (255, 0, 0),
                     (offset_x + start[1] * box_width, offset_y + start[0] * box_width, box_width, box_width))

    pygame.draw.rect(scr, (0, 255, 0),
                     (offset_x + end[1] * box_width, offset_y + end[0] * box_width, box_width, box_width))


def generate_layout(board_data, grid_size):
    assets_layout = [list(lane) for lane in board_data]

    for ii in range(grid_size[0] - 1):
        for it in range(grid_size[1] - 1):
            if (assets_layout[ii][it] == -1 and
                    assets_layout[ii + 1][it] == -1 and
                    assets_layout[ii][it + 1] == -1 and
                    assets_layout[ii + 1][it + 1] == -1):
                assets_layout[ii][it] = random.choice((-2, -12))
                assets_layout[ii + 1][it] = -100
                assets_layout[ii][it + 1] = -100
                assets_layout[ii + 1][it + 1] = -100
            elif (assets_layout[ii][it] == -1 and
                    assets_layout[ii + 1][it] == -1):
                assets_layout[ii][it] = random.choice((-3, -13))
                assets_layout[ii + 1][it] = -100
            elif (assets_layout[ii][it] == -1 and
                  assets_layout[ii][it + 1] == -1):
                assets_layout[ii][it] = random.choice((-4, -14))
                assets_layout[ii][it + 1] = -100
            elif assets_layout[ii][it] >= 0:
                side = 0
                if -100 == assets_layout[ii + 1][it] or -14 <= assets_layout[ii + 1][it] <= -1:
                    side += 1
                if -100 == assets_layout[ii][it + 1] or -14 <= assets_layout[ii][it + 1] <= -1:
                    side += 2
                if ii > 0:
                    if -100 == assets_layout[ii - 1][it] or -14 <= assets_layout[ii - 1][it] <= -1:
                        side += 4
                else:
                    side += 4
                if it > 0:
                    if -100 == assets_layout[ii][it - 1] or -14 <= assets_layout[ii][it - 1] <= -1:
                        side += 8
                else:
                    side += 8

                assets_layout[ii][it] = - 200 - side

    for ii in range(grid_size[0]):
        it = grid_size[1] - 1
        if assets_layout[ii][it] >= 0:
            side = 2
            if ii < grid_size[0] - 1:
                if -100 == assets_layout[ii + 1][it] or -14 <= assets_layout[ii + 1][it] <= -1:
                    side += 1
            else:
                side += 1
            if ii > 0:
                if -100 == assets_layout[ii - 1][it] or -14 <= assets_layout[ii - 1][it] <= -1:
                    side += 4
            else:
                side += 4
            if -100 == assets_layout[ii][it - 1] or -14 <= assets_layout[ii][it - 1] <= -1:
                side += 8

            assets_layout[ii][it] = - 200 - side

    for it in range(grid_size[1]):
        ii = grid_size[0] - 1
        if assets_layout[ii][it] >= 0:
            side = 1
            if it < grid_size[1] - 1:
                if -100 == assets_layout[ii][it + 1] or -14 <= assets_layout[ii][it + 1] <= -1:
                    side += 2
            else:
                side += 2
            if -100 == assets_layout[ii - 1][it] or -14 <= assets_layout[ii - 1][it] <= -1:
                side += 4
            if it > 0:
                if -100 == assets_layout[ii][it - 1] or -14 <= assets_layout[ii][it - 1] <= -1:
                    side += 8
            else:
                side += 8

            assets_layout[ii][it] = - 200 - side

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if assets_layout[ii][it] == -1:
                assets_layout[ii][it] = random.choice((-1, -11))

    for aa in assets_layout:
        print(aa)
    return assets_layout


def draw_assets_board_data(scr: pygame.Surface, board_data, assets_generate, start, end, grid_size, box_width, direction, offset_x=0,
                           offset_y=0):
    display_font = pygame.font.Font('freesansbold.ttf', box_width // 2)

    assets_img = {
        'car': [pygame.image.load("assets/car_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'building': [pygame.image.load("assets/block_2x2_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'house': [pygame.image.load("assets/block_1x1_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'road': [pygame.image.load("assets/road_" + str(_) + ".png").convert_alpha() for _ in range(16)],
        'time_stop': [pygame.image.load("assets/time_stop_" + str(_) + ".png").convert_alpha() for _ in range(1)],
        'end_stop': [pygame.image.load("assets/end_" + str(_) + ".png").convert_alpha() for _ in range(1)],
        'landscape': [pygame.image.load("assets/block_1x2_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'portrait': [pygame.image.load("assets/block_2x1_" + str(_) + ".png").convert_alpha() for _ in range(2)],
    }

    car = pygame.transform.scale(pygame.transform.rotate(assets_img['car'][0], direction), (box_width + 2, box_width + 2))
    # building = pygame.transform.scale(pygame.transform.rotate(assets_img['building'][0], 0), (box_width * 2.2, box_width * 2.2))
    # court = pygame.transform.scale(pygame.transform.rotate(assets_img['portrait'][0], 0), (box_width * 1.2, box_width * 2.2))
    # park = pygame.transform.scale(pygame.transform.rotate(assets_img['landscape'][0], 0), (box_width * 2.2, box_width * 1.2))
    # house = pygame.transform.scale(pygame.transform.rotate(assets_img['house'][0], 0), (box_width * 1.2, box_width * 1.2))
    # road = pygame.transform.scale(pygame.transform.rotate(assets_img['road'][0], 0),(box_width, box_width))
    time_stop = pygame.transform.scale(pygame.transform.rotate(assets_img['time_stop'][0], 0),(box_width * 1.2, box_width * 1.2))
    end_point = pygame.transform.scale(pygame.transform.rotate(assets_img['end_stop'][0], 0),(box_width * 1.2, box_width * 1.2))

    # scr.blit(road, (offset_x, offset_y))

    # assets_generate = generate_layout(board_data, grid_size)
    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            road = pygame.transform.scale(pygame.transform.rotate(assets_img['road'][0], 0), (box_width, box_width))
            scr.blit(road, (offset_x + it * box_width, offset_y + ii * box_width))

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if assets_generate[ii][it] == -1 or assets_generate[ii][it] == -11:
                house = pygame.transform.scale(pygame.transform.rotate(assets_img['house'][assets_generate[ii][it] < -10], 0), (box_width * 1.2, box_width * 1.2))
                scr.blit(house, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
            if assets_generate[ii][it] == -2 or assets_generate[ii][it] == -12:
                building = pygame.transform.scale(pygame.transform.rotate(assets_img['building'][assets_generate[ii][it] < -10], 0), (box_width * 2.2, box_width * 2.2))
                scr.blit(building, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
            if assets_generate[ii][it] == -3 or assets_generate[ii][it] == -13:
                court = pygame.transform.scale(pygame.transform.rotate(assets_img['portrait'][assets_generate[ii][it] < -10], 0), (box_width * 1.2, box_width * 2.2))
                scr.blit(court, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
            if assets_generate[ii][it] == -4 or assets_generate[ii][it] == -14:
                park = pygame.transform.scale(pygame.transform.rotate(assets_img['landscape'][assets_generate[ii][it] < -10], 0),(box_width * 2.2, box_width * 1.2))
                scr.blit(park, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if assets_generate[ii][it] < -200:
                road = pygame.transform.scale(pygame.transform.rotate(assets_img['road'][(assets_generate[ii][it] + 200) * -1], 0),(box_width, box_width))
                scr.blit(road, (offset_x + it * box_width, offset_y + ii * box_width))

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if board_data[ii][it] > 0:
                scr.blit(time_stop, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
                box_value = display_font.render(str(board_data[ii][it]), True, (255, 255, 255))
                box_value_rect = box_value.get_rect()
                box_value_rect.center = (
                    offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)

    scr.blit(car, (offset_x + start[1] * box_width, offset_y + start[0] * box_width))
    scr.blit(end_point, (offset_x + end[1] * box_width, offset_y + end[0] * box_width))


def draw_step(scr: pygame.Surface, path_movement, step, box_size, scr_offset_x, scr_offset_y):
    for move in range(step):
        pygame.draw.rect(scr, (0, 128, 128),
                         (scr_offset_x + path_movement[move][1] * box_size,
                          scr_offset_y + path_movement[move][0] * box_size,
                          box_size, box_size))


def draw_expansion(scr: pygame.Surface, path_movement, step, box_size, scr_offset_x, scr_offset_y):
    for move in range(step):
        pygame.draw.rect(scr, (128, 40, 128),
                         (scr_offset_x + path_movement[move][1] * box_size,
                          scr_offset_y + path_movement[move][0] * box_size,
                          box_size, box_size))


def draw_info_box(scr: pygame.Surface, start, end, time_limit, fuel_limit, grid_size, box_size, scr_offset_x,
                  scr_offset_y):
    display_font = pygame.font.Font('freesansbold.ttf', box_size // 2)
    pygame.draw.rect(scr, (255, 255, 255),
                     (scr_offset_x * 2 + box_size * grid_size[0], scr_offset_y, box_size * 4, box_size * grid_size[1]),
                     width=2)
    start_value = display_font.render(f"Start: {start[0], start[1]}", True, (255, 255, 255))
    start_value_rect = start_value.get_rect()
    start_value_rect.center = (scr_offset_x * 3 + box_size * (grid_size[0] + 1), scr_offset_y + box_size)
    end_value = display_font.render(f"End: {end[0], end[1]}", True, (255, 255, 255))
    end_value_rect = end_value.get_rect()
    end_value_rect.center = (scr_offset_x * 3 + box_size * (grid_size[0] + 1), scr_offset_y * 3 + box_size)
    time_value = display_font.render(f"Time limit: {time_limit}", True, (255, 255, 255))
    time_value_rect = time_value.get_rect()
    time_value_rect.center = (scr_offset_x * 3 + box_size * (grid_size[0] + 1), scr_offset_y * 5 + box_size)
    fuel_value = display_font.render(f"Fuel limit :{fuel_limit}", True, (255, 255, 255))
    fuel_value_rect = fuel_value.get_rect()
    fuel_value_rect.center = (scr_offset_x * 3 + box_size * (grid_size[0] + 1), scr_offset_y * 7 + box_size)
    scr.blits([
        (start_value, start_value_rect),
        (end_value, end_value_rect),
        (time_value, time_value_rect),
        (fuel_value, fuel_value_rect),
    ])
