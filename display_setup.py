import random
import pygame


def get_box_config(res: tuple[int, int], grid_size: tuple[int, int]):
    width = res[0] - 100
    height = res[1] - 100

    box_width = min(width // grid_size[0], height // grid_size[1])
    offset_x = (res[0] - box_width * grid_size[1]) // 2 - 100
    offset_y = (res[1] - box_width * grid_size[0]) // 2

    # offset_x = 10
    # offset_y = 10
    return box_width, offset_x, offset_y


def draw_grid(scr: pygame.Surface, grid_size, box_width, offset_x, offset_y):
    for it in range(grid_size[0]):
        for ii in range(grid_size[1]):
            pygame.draw.rect(scr, (255, 255, 255),
                             (offset_x + ii * box_width, offset_y + it * box_width, box_width, box_width), width=1)


def draw_text(text, font_name, size, coordinate, color=(255, 255, 255)) -> tuple:
    display_font = pygame.font.SysFont(font_name, size)
    display_text = display_font.render(text, True, color)
    display_text_rect = display_text.get_rect()
    display_text_rect.topleft = coordinate
    return display_text, display_text_rect


def draw_board_data(scr: pygame.Surface, level, board_data, start, end, grid_size, box_width, offset_x=0,
                    offset_y=0):
    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if str(board_data[ii][it]) == '-1':
                pygame.draw.rect(scr, (128, 128, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
            elif str(board_data[ii][it])[0] == 'F' and level == 'lvl3':
                pygame.draw.rect(scr, (200, 200, 0),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
                box_value, box_value_rect = draw_text(str(board_data[ii][it]), 'comicsansms',
                                                      box_width // 2, (0, 0))
                box_value_rect.center = (offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)
                scr.blit(box_value, box_value_rect)

            elif str(board_data[ii][it]) > '0' and level in ('lvl2', 'lvl3') and str(board_data[ii][it])[0] != 'F':
                pygame.draw.rect(scr, (10, 200, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
                box_value, box_value_rect = draw_text(str(board_data[ii][it]), 'comicsansms',
                                                      box_width // 2, (0, 0))
                box_value_rect.center = (offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)

                scr.blit(box_value, box_value_rect)

    pygame.draw.rect(scr, (255, 0, 0),
                     (offset_x + start[1] * box_width, offset_y + start[0] * box_width, box_width, box_width))

    pygame.draw.rect(scr, (0, 255, 0),
                     (offset_x + end[1] * box_width, offset_y + end[0] * box_width, box_width, box_width))


def generate_layout(board_data, grid_size):
    if grid_size[0] >= 30 or grid_size[1] >= 30:
        return None

    assets_layout = [list(lane) for lane in board_data]

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if str(assets_layout[ii][it])[0] == 'F':
                assets_layout[ii][it] = 0

    # Block generator
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

    # Road generator
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

    # for aa in assets_layout:
    #     print(aa)
    return assets_layout


def draw_assets_board_data(scr: pygame.Surface, level, board_data, assets_generate, start, end, grid_size, box_width,
                           direction, offset_x=0,
                           offset_y=0):
    display_font = pygame.font.SysFont("comicsansms", box_width // 2)
    fuels = []

    assets_img = {
        'car': [pygame.image.load("assets/car_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'building': [pygame.image.load("assets/block_2x2_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'house': [pygame.image.load("assets/block_1x1_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'road': [pygame.image.load("assets/road_" + str(_) + ".png").convert_alpha() for _ in range(16)],
        'time_stop': [pygame.image.load("assets/time_stop_" + str(_) + ".png").convert_alpha() for _ in range(1)],
        'fuel_stop': [pygame.image.load("assets/fuel_stop_" + str(_) + ".png").convert_alpha() for _ in range(1)],
        'end_stop': [pygame.image.load("assets/end_" + str(_) + ".png").convert_alpha() for _ in range(1)],
        'landscape': [pygame.image.load("assets/block_1x2_" + str(_) + ".png").convert_alpha() for _ in range(2)],
        'portrait': [pygame.image.load("assets/block_2x1_" + str(_) + ".png").convert_alpha() for _ in range(2)],
    }

    car = pygame.transform.scale(pygame.transform.rotate(assets_img['car'][0], direction),
                                 (box_width + 2, box_width + 2))
    time_stop = pygame.transform.scale(pygame.transform.rotate(assets_img['time_stop'][0], 0),
                                       (box_width * 1.2, box_width * 1.2))
    end_point = pygame.transform.scale(pygame.transform.rotate(assets_img['end_stop'][0], 0),
                                       (box_width * 1.2, box_width * 1.2))
    fuel_stop = pygame.transform.scale(pygame.transform.rotate(assets_img['fuel_stop'][0], 0),
                                       (box_width * 1.2, box_width * 1.2))

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if str(board_data[ii][it])[0] == 'F':
                fuels.append((ii, it, board_data[ii][it]))
                board_data[ii][it] = 0
            road = pygame.transform.scale(pygame.transform.rotate(assets_img['road'][0], 0), (box_width, box_width))
            scr.blit(road, (offset_x + it * box_width, offset_y + ii * box_width))

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if assets_generate[ii][it] == -1 or assets_generate[ii][it] == -11:
                house = pygame.transform.scale(
                    pygame.transform.rotate(assets_img['house'][assets_generate[ii][it] < -10], 0),
                    (box_width * 1.2, box_width * 1.2))
                scr.blit(house, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
            if assets_generate[ii][it] == -2 or assets_generate[ii][it] == -12:
                building = pygame.transform.scale(
                    pygame.transform.rotate(assets_img['building'][assets_generate[ii][it] < -10], 0),
                    (box_width * 2.2, box_width * 2.2))
                scr.blit(building, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
            if assets_generate[ii][it] == -3 or assets_generate[ii][it] == -13:
                court = pygame.transform.scale(
                    pygame.transform.rotate(assets_img['portrait'][assets_generate[ii][it] < -10], 0),
                    (box_width * 1.2, box_width * 2.2))
                scr.blit(court, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
            if assets_generate[ii][it] == -4 or assets_generate[ii][it] == -14:
                park = pygame.transform.scale(
                    pygame.transform.rotate(assets_img['landscape'][assets_generate[ii][it] < -10], 0),
                    (box_width * 2.2, box_width * 1.2))
                scr.blit(park, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if assets_generate[ii][it] < -200:
                road = pygame.transform.scale(
                    pygame.transform.rotate(assets_img['road'][(assets_generate[ii][it] + 200) * -1], 0),
                    (box_width, box_width))
                scr.blit(road, (offset_x + it * box_width, offset_y + ii * box_width))

    if level in ('lvl2', 'lvl3'):
        for ii in range(grid_size[0]):
            for it in range(grid_size[1]):
                if board_data[ii][it] > 0:
                    box_value, box_value_rect = draw_text(str(board_data[ii][it]), "comicsansms", box_width // 2, (0, 0))
                    box_value_rect.center = (
                        offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)
                    scr.blit(time_stop, (offset_x + (it - 0.1) * box_width, offset_y + (ii - 0.1) * box_width))
                    scr.blit(box_value, box_value_rect)

    for f in fuels:
        if level == 'lvl3':
            scr.blit(fuel_stop, (offset_x + (f[1] - 0.1) * box_width, offset_y + (f[0] - 0.1) * box_width))
            box_value, box_value_rect = draw_text(f[2], "comicsansms", box_width // 2, (0, 0))
            box_value_rect.center = (
                offset_x + f[1] * box_width + box_width // 2, offset_y + f[0] * box_width + box_width // 2)
            scr.blit(box_value, box_value_rect)
        board_data[f[0]][f[1]] = f[2]

    scr.blit(car, (offset_x + start[1] * box_width, offset_y + start[0] * box_width))
    scr.blit(end_point, (offset_x + end[1] * box_width, offset_y + end[0] * box_width))


def draw_step(scr: pygame.Surface, level, board_data, path_movement, time, fuel, box_size, scr_offset_x, scr_offset_y):
    if path_movement is None:
        invalid, invalid_rect = draw_text(f"No valid path.", "comicsansms",  20,
                                                (scr_offset_x * 2 + box_size * len(board_data[0]) + 10, scr_offset_y + 10 + box_size * 5),
                                          (255, 10, 10))
        scr.blit(invalid, invalid_rect)
        return 0

    total_cost = 0
    total_time = 0
    fuel_cost = fuel
    stopped_time = 0

    while total_time < time - 1:
        pygame.draw.rect(scr, (0, 128, 128),
                         (scr_offset_x + path_movement[total_cost][1] * box_size,
                          scr_offset_y + path_movement[total_cost][0] * box_size,
                          box_size, box_size))
        total_time += 1
        stopped_time += 1
        current_block = board_data[path_movement[total_cost][0]][path_movement[total_cost][1]]

        if level in ('bfs', 'dfs', 'ucs', 'gbfs', 'a*'):
            total_cost += 1

        elif level == 'lvl2':
            if str(current_block)[0] == 'F' or int(str(current_block).strip('F')) + 1 == stopped_time:
                stopped_time = 0
                total_cost += 1

        elif level == 'lvl3':
            if int(str(current_block).strip('F')) + 1 == stopped_time: # Has finished through a cell
                stopped_time = 0
                total_cost += 1
            if str(current_block)[0] == 'F':
                fuel_cost = fuel
            else:
                fuel_cost -= 1
    info = []
    current_cost, current_cost_rect = draw_text(f"Path cost: {total_cost}", "comicsansms",  20,
                                                (scr_offset_x + box_size * len(board_data[1]) + 40, 250))
    info.append((current_cost, current_cost_rect))
    if level in ('lvl2', 'lvl3'):
        time_cost, time_cost_rect = draw_text(f"Current Time: {total_time}", "comicsansms", 20,
                                          (scr_offset_x + box_size * len(board_data[1]) + 40, 280))
        info.append((time_cost, time_cost_rect))
    if level == 'lvl3':
        current_fuel, current_fuel_rect = draw_text(f"Current Fuel: {fuel_cost}", "comicsansms", 20,
                                                    (scr_offset_x + box_size * len(board_data[1]) + 40, 310))
        info.append((current_fuel, current_fuel_rect))

    scr.blits(info)

    return total_cost


def draw_expansion(scr: pygame.Surface, path_movement, step, box_size, scr_offset_x, scr_offset_y):
    for move in range(step):
        pygame.draw.rect(scr, (128, 40, 128),
                         (scr_offset_x + path_movement[move][1] * box_size,
                          scr_offset_y + path_movement[move][0] * box_size,
                          box_size, box_size))


def draw_info_box(scr: pygame.Surface, start, end, level, time_limit, fuel_limit, grid_size, box_size, scr_offset_x,
                  scr_offset_y):
    # display_font = pygame.font.Font('comicsansms', box_size // 2)

    info_list = []

    display_font = pygame.font.SysFont("comicsansms", box_size // 3)
    pygame.draw.rect(scr, (255, 255, 255),
                     (scr_offset_x + box_size * grid_size[1] + 20, 50, 250, 600),
                     width=2)

    start_value, start_value_rect = draw_text(f"Start: {start[0], start[1]}", "comicsansms",  20,
                                              (scr_offset_x + box_size * grid_size[1] + 40, 80))
    info_list.append((start_value, start_value_rect))

    end_value, end_value_rect = draw_text(f"End: {end[0], end[1]}", "comicsansms",  20,
                                          (scr_offset_x + box_size * grid_size[1] + 40, 110))
    info_list.append((end_value, end_value_rect))

    if level in ('lvl2', 'lvl3', 'lvl4'):
        time_value, time_value_rect = draw_text(f"Time limit: {time_limit}", "comicsansms",  20,
                                                (scr_offset_x + box_size * grid_size[1] + 40, 140))

        info_list.append((time_value, time_value_rect))
    if level in ('lvl3', 'lvl4'):
        fuel_value, fuel_value_rect = draw_text(f"Fuel limit: {fuel_limit}", "comicsansms",  20,
                                                (scr_offset_x + box_size * grid_size[1] + 40, 170))
        info_list.append((fuel_value, fuel_value_rect))

    alias_name, alias_name_rect = draw_text(level.upper(), "comicsansms",  20,
                                            (scr_offset_x + box_size * grid_size[1] + 100, 210))
    info_list.append((alias_name, alias_name_rect))

    pygame.draw.polygon(scr, (255, 255, 255), [
        (scr_offset_x + box_size * grid_size[1] + 20 + 75, 205 + 10),
        (scr_offset_x + box_size * grid_size[1] + 10 + 75, 205 + 20),
        (scr_offset_x + box_size * grid_size[1] + 20 + 75, 205 + 30),
    ])
    pygame.draw.polygon(scr, (255, 255, 255), [
        (scr_offset_x + box_size * grid_size[1] + 10 + 145, 205 + 10),
        (scr_offset_x + box_size * grid_size[1] + 20 + 145, 205 + 20),
        (scr_offset_x + box_size * grid_size[1] + 10 + 145, 205 + 30),
    ])

    scr.blits(info_list)


# Lv4 territory

def draw_lv4_step(scr: pygame.Surface, agents_count, board_data, path_movement, time, fuel, box_size, scr_offset_x, scr_offset_y):
    if path_movement[0] is None:
        invalid, invalid_rect = draw_text(f"No valid path for main agent.", "comicsansms",  20,
                                                (scr_offset_x * 2 + box_size * len(board_data[0]) + 10, scr_offset_y + 10 + box_size * 5),
                                          (255, 10, 10))
        scr.blit(invalid, invalid_rect)
        return

    for a in range(agents_count):
        for m in range(time):
            pygame.draw.rect(scr, (0, 128, 128),
                             (scr_offset_x + path_movement[a][m][1] * box_size,
                              scr_offset_y + path_movement[a][m][0] * box_size,
                              box_size, box_size))

    info = []


def draw_lv4_board_data(scr: pygame.Surface, agents_count, board_data, start, end, grid_size, box_width, offset_x=0,
                    offset_y=0):

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if str(board_data[ii][it]) == '-1':
                pygame.draw.rect(scr, (128, 128, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
            elif str(board_data[ii][it])[0] == 'F':
                pygame.draw.rect(scr, (200, 200, 0),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
                box_value, box_value_rect = draw_text(str(board_data[ii][it]), 'comicsansms',
                                                      box_width // 2, (0, 0))
                box_value_rect.center = (
                offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)
                scr.blit(box_value, box_value_rect)

            elif str(board_data[ii][it]) > '0' and str(board_data[ii][it])[0] != 'F':
                pygame.draw.rect(scr, (10, 200, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
                box_value, box_value_rect = draw_text(str(board_data[ii][it]), 'comicsansms',
                                                      box_width // 2, (0, 0))
                box_value_rect.center = (
                offset_x + it * box_width + box_width // 2, offset_y + ii * box_width + box_width // 2)

                scr.blit(box_value, box_value_rect)

    agent_color = (
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (128, 255, 0),
        (128, 0, 255),
        (255, 128, 0),
        (0, 128, 255)
    )

    for i in range(agents_count):
        pygame.draw.rect(scr, agent_color[i],
                         (offset_x + end[i][1] * box_width, offset_y + end[i][0] * box_width, box_width, box_width))
    for i in range(agents_count):
        pygame.draw.circle(scr, agent_color[i],
                         (offset_x + (start[i][1] + .5) * box_width, offset_y + (start[i][0] + .5) * box_width), box_width / 2)
        pygame.draw.circle(scr, (255, 255, 255),
                           (offset_x + (start[i][1] + .5) * box_width, offset_y + (start[i][0] + .5) * box_width),
                           box_width / 2, 1)
