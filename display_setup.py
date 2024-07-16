import pygame


def get_box_config(res: tuple[int, int], grid_size: tuple[int, int]):
    width = res[0] - 100
    height = res[1] - 100

    box_width = min(width // grid_size[0], height // grid_size[1])
    offset_x = (res[0] - box_width * grid_size[0]) // 2
    offset_y = (res[1] - box_width * grid_size[1]) // 2

    return box_width, offset_x, offset_y


def draw_grid(scr: pygame.Surface, grid_size, box_width, offset_x, offset_y):
    for it in range(grid_size[0]):
        for ii in range(grid_size[1]):
            pygame.draw.rect(scr, (255, 255, 255),
                             (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width), width=2)


def draw_board_data(scr: pygame.Surface, board_data, start, end, grid_size, box_width, offset_x=0, offset_y=0):
    display_font = pygame.font.Font('freesansbold.ttf', box_width // 2)

    for ii in range(grid_size[0]):
        for it in range(grid_size[1]):
            if board_data[ii][it] == -1:
                pygame.draw.rect(scr, (128, 128, 128),
                                 (offset_x + it * box_width, offset_y + ii * box_width, box_width, box_width))
            if board_data[ii][it] > 0:
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


def draw_step(scr: pygame.Surface, path_movement, step, box_size, scr_offset_x, scr_offset_y):
    for move in range(step):
        pygame.draw.rect(scr, (0, 128, 128),
                         (scr_offset_x + path_movement[move][1] * box_size,
                          scr_offset_y + path_movement[move][0] * box_size,
                          box_size, box_size))
