def configure_path(move_1: tuple[int, int], move_2: tuple[int, int]):
    if move_1 == -1:
        return ""
    elif move_2[1] - move_1[1] == 1:
        return "d"
    elif move_2[1] - move_1[1] == -1:
        return "a"
    elif move_2[0] - move_1[0] == 1:
        return "w"
    elif move_2[0] - move_1[0] == -1:
        return "s"


def generate_neighbor(block: tuple[int, int], board_data, reached: dict):
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    explored = []

    for neighbor in neighbors:
        x, y = block[0] + neighbor[0], block[1] + neighbor[1]

        if (
            0 <= x < len(board_data) and
            0 <= y < len(board_data[0]) and
            (x, y) not in reached and
            board_data[x][y] >= 0
        ):

            explored.append((x, y))

    return explored


def generate_path(reached_table: dict[tuple[int, int]: tuple[int, int]], start: tuple[int, int], end: tuple[int, int]):
    # path_move = []
    path_block = []
    while True:
        # path_move.insert(0, configure_path(reached_table[end], end))
        path_block.insert(0, end)
        end = reached_table[end]
        if end == -1:
            # path_move.insert(0, configure_path(reached_table[end], end))
            # path_block.insert(0, end)
            return path_block  # path_move


def BFS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]

    while True:
        # No node can be explored
        if len(frontier) == 0:
            return

        current_node = frontier.pop(0)

        explored = generate_neighbor(current_node, board_data, reached)

        if end in explored:  # Early goal test
            reached[end] = current_node
            return generate_path(reached, start, end)

        elif len(explored) != 0:
            frontier.extend(explored)
            reached.update({_: current_node for _ in explored})


def DFS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]

    while True:
        # No node can be explored
        if len(frontier) == 0:
            return [], []

        current_node = frontier.pop()

        explored = generate_neighbor(current_node, board_data, reached)

        if end in explored:  # Early goal test
            reached[end] = current_node
            return generate_path(reached, start, end)

        elif len(explored) != 0:
            frontier.extend(explored)
            reached.update({_: current_node for _ in explored})


def BestFS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], limit = float('inf')):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    time_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    road_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]

    time_cost[start[0]][start[1]] = board_data[start[0]][start[1]]
    road_cost[start[0]][start[1]] = 0

    while True:
        # No node can be explored
        if len(frontier) == 0:
            # for pp in time_cost:
            #     for ppp in pp:
            #         print(f"{ppp:<3}", end=" ")
            #     print()
            return [], []

        current_node = frontier.pop(0)
        # print(cost[current_node[0]][current_node[1]])

        if end == current_node:
            print("Final time cost:", time_cost[end[0]][end[1]])
            print("Final path cost:", road_cost[end[0]][end[1]])
            return generate_path(reached, start, end)

        elif time_cost[current_node[0]][current_node[1]] < limit:
            explored = generate_neighbor(current_node, board_data, reached)

            if end in explored:
                time_cost[end[0]][end[1]] = time_cost[current_node[0]][current_node[1]] + board_data[end[0]][
                    end[1]] + 1
                road_cost[end[0]][end[1]] = road_cost[current_node[0]][current_node[1]] + 1
                frontier.append(end)
                reached[end] = current_node

            elif time_cost[current_node[0]][current_node[1]] < limit - 1:
                for nods in explored:
                    time_cost[nods[0]][nods[1]] = time_cost[current_node[0]][current_node[1]] + board_data[nods[0]][nods[1]] + 1
                    road_cost[nods[0]][nods[1]] = road_cost[current_node[0]][current_node[1]] + 1
                    frontier.append(nods)
                    reached[nods] = current_node

            # frontier.sort(key=lambda x: cost[x[0]][x[1]])
            frontier.sort(key=lambda x: road_cost[x[0]][x[1]])