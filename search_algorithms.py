def configure_path(move_1: tuple[int, int], move_2: tuple[int, int]):
    if move_1 == -1:
        return 0
    elif move_2[1] - move_1[1] == 1:
        return -90
    elif move_2[1] - move_1[1] == -1:
        return 90
    elif move_2[0] - move_1[0] == 1:
        return 180
    elif move_2[0] - move_1[0] == -1:
        return 0


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

def generate_neighbor_LVL2(block: tuple[int, int], board_data, reached: dict):
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    explored = []

    for neighbor in neighbors:
        x, y = block[0] + neighbor[0], block[1] + neighbor[1]

        if (
            0 <= x < len(board_data) and
            0 <= y < len(board_data[0]) and 
            #(x, y) not in reached  and //// now its alway generate 4 surrounding drivable tile
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
    expansion: list[tuple[int, int]] = []

    while True:
        # No node can be explored
        if len(frontier) == 0:
            return None, expansion

        current_node = frontier.pop(0)
        expansion.append(current_node)

        explored = generate_neighbor(current_node, board_data, reached)

        if end in explored:  # Early goal test
            reached[end] = current_node
            return generate_path(reached, start, end), expansion

        elif len(explored) != 0:
            frontier.extend(explored)
            reached.update({_: current_node for _ in explored})


def DFS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    expansion: list[tuple[int, int]] = []

    while True:
        # No node can be explored
        if len(frontier) == 0:
            return None, expansion

        current_node = frontier.pop()
        expansion.append(current_node)

        explored = generate_neighbor(current_node, board_data, reached)

        if end in explored:  # Early goal test
            reached[end] = current_node
            return generate_path(reached, start, end), expansion

        elif len(explored) != 0:
            frontier.extend(explored)
            reached.update({_: current_node for _ in explored})


def BestFS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], limit=float('inf')):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    time_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    road_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    expansion: list[tuple[int, int]] = []

    time_cost[start[0]][start[1]] = board_data[start[0]][start[1]]
    road_cost[start[0]][start[1]] = 0

    while True:
        # No node can be explored
        if len(frontier) == 0:
            # for pp in time_cost:
            #     for ppp in pp:
            #         print(f"{ppp:<3}", end=" ")
            #     print()
            return None, expansion  

        current_node = frontier.pop(0)
        # print(cost[current_node[0]][current_node[1]])
        expansion.append(current_node)

        if end == current_node:
            return generate_path(reached, start, end), expansion

        elif time_cost[current_node[0]][current_node[1]] < limit:
            explored = generate_neighbor(current_node, board_data, reached)

            # if end in explored:
            #     time_cost[end[0]][end[1]] = time_cost[current_node[0]][current_node[1]] + board_data[end[0]][
            #         end[1]] + 1
            #     road_cost[end[0]][end[1]] = road_cost[current_node[0]][current_node[1]] + 1
            #     frontier.append(end)
            #     reached[end] = current_node

            for nods in explored:
                time_cost[nods[0]][nods[1]] = time_cost[current_node[0]][current_node[1]] + board_data[nods[0]][nods[1]] + 1
                road_cost[nods[0]][nods[1]] = road_cost[current_node[0]][current_node[1]] + 1
                frontier.append(nods)
                reached[nods] = current_node
                if nods == end:    
                    return generate_path(reached, start, end), expansion


            # frontier.sort(key=lambda x: cost[x[0]][x[1]])
            frontier.sort(key=lambda x: road_cost[x[0]][x[1]])

def LVL2_UCS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], limit=float('inf')):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    time_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    road_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    expansion: list[tuple[int, int]] = []

    time_cost[start[0]][start[1]] = board_data[start[0]][start[1]]
    road_cost[start[0]][start[1]] = 0

    while True:
        # No node can be explored
        if len(frontier) == 0:
            print("pq empty!")
            return None, expansion  
        
        current_node = frontier.pop(0)
        expansion.append(current_node) 
        if (current_node == end):
            print("found1")
            return generate_path(reached, start, end), expansion
        
        if time_cost[current_node[0]][current_node[1]] < limit:
            print(current_node)
            explored = generate_neighbor_LVL2(current_node, board_data, reached)
            for nods in explored:
                if nods not in reached or time_cost[nods[0]][nods[1]] > time_cost[current_node[0]][current_node[1]] + board_data[nods[0]][nods[1]] + 1: # add this so that reached tile can revisited if the new time_cost is better
                    time_cost[nods[0]][nods[1]] = time_cost[current_node[0]][current_node[1]] + board_data[nods[0]][nods[1]] + 1
                    road_cost[nods[0]][nods[1]] = road_cost[current_node[0]][current_node[1]] + 1
                    frontier.append(nods)
                    reached[nods] = current_node
                    if nods == end and time_cost[nods[0]][nods[1]] <= limit:
                        return generate_path(reached, start, end), expansion
        frontier.sort(key=lambda x: road_cost[x[0]][x[1]])
