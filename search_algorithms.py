import heapq
import copy

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
            board_data[x][y] != -1
        ):

            explored.append((x, y))

    return explored

def generate_path(reached_table: dict[tuple[int, int]: tuple[int, int]], start: tuple[int, int], end: tuple[int, int]):
    path_block = []
    while True:
        path_block.insert(0, end)
        end = reached_table[end]
        if end == -1:
            return path_block  # path_move


def generate_time_cost(board_data: list[list[int]], path: list[tuple[int, int]], level):
    if path is None:
        return 0

    if level == 'lvl4':
        if path[0] is None:
            return 0
        return len(path[0])

    total_time = len(path) - 1

    for step in path:
        if level in ('lvl2', 'lvl3') and str(board_data[step[0]][step[1]])[0] != 'F': # Time toll
            total_time += board_data[step[0]][step[1]]
        elif level == 'lvl3' and str(board_data[step[0]][step[1]])[0] == 'F': # Fuel toll
            total_time += int(str(board_data[step[0]][step[1]]).strip('F'))

    return total_time

def get_timed_path(board_data, path):
    timed_path = []

    total_cost = 0
    total_time = 0
    stopped_time = 0

    while total_time <= generate_time_cost(board_data, path, 'lvl3'):
        timed_path.append(path[total_cost])

        total_time += 1
        stopped_time += 1
        current_block = board_data[path[total_cost][0]][path[total_cost][1]]

        if int(str(current_block).strip('F')) + 1 == stopped_time:  # Has finished through a cell
            stopped_time = 0
            total_cost += 1

    return timed_path


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


def UCS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    road_cost = [[float('inf') for _ in range(len(board_data[0]))] for __ in range(len(board_data))]
    expansion: list[tuple[int, int]] = []

    road_cost[start[0]][start[1]] = 0
    
    while True:
        if len(frontier) == 0:
            return None, expansion

        current_node = frontier.pop(0)
        expansion.append(current_node)

        explored = generate_neighbor(current_node, board_data, reached)
        
        if current_node == end:
            return generate_path(reached, start, end), expansion

        for nods in explored:
            if nods not in reached or road_cost[nods[0]][nods[1]] > road_cost[current_node[0]][current_node[1]] + 1:
                frontier.append(nods)
                reached[nods] = current_node
                road_cost[nods[0]][nods[1]] = road_cost[current_node[0]][current_node[1]] + 1
        
        frontier.sort(key=lambda x: road_cost[x[0]][x[1]])
            

def GBFS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    if start == end:
        return [start], []
    
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

        for nods in explored:
            if nods not in reached:
                frontier.append(nods)
                reached[nods] = current_node
                if nods == end:    
                    return generate_path(reached, start, end), expansion

        frontier.sort(key=lambda x: abs(end[0] - x[0]) + abs(end[1] - x[1])) # Manhattan distance


def A_STAR(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    road_cost = [[float('inf') for _ in range(len(board_data[0]))] for __ in range(len(board_data))]
    expansion: list[tuple[int, int]] = []

    road_cost[start[0]][start[1]] = 0 
    
    while True:
        if len(frontier) == 0:
            return None, expansion

        current_node = frontier.pop(0)
        expansion.append(current_node)

        explored = generate_neighbor(current_node, board_data, reached)
        
        if current_node == end:
            return generate_path(reached, start, end), expansion

        for nods in explored:
            new_cost = road_cost[current_node[0]][current_node[1]] + 1
            if nods not in reached or road_cost[nods[0]][nods[1]] > new_cost:
                frontier.append(nods)
                reached[nods] = current_node
                road_cost[nods[0]][nods[1]] = new_cost
        
        frontier.sort(key=lambda x: road_cost[x[0]][x[1]] + abs(end[0] - x[0]) + abs(end[1] - x[1])) # F = G + H  


def LVL2_UCS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], time_limit=float('inf')):
    rows, cols = len(board_data), len(board_data[0])
    
    # Priority queue: (path_cost, time, current_position, path)
    pq = [(0, 0, start, [])]
    reached = {start: 0}

    while pq:
        steps, time, current, path = heapq.heappop(pq)
        
        if current == end:
            # print(f"Path cost: {steps}, Time: {time}")
            return path + [current], []
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_pos = (nx, ny)
                cell = board_data[nx][ny]
                
                # Skip blocked cells
                if cell == -1:
                    continue
                
                # Ignore gas station
                if isinstance(cell, str) and cell.startswith('F'):
                    new_time = time + 1
                else:
                    new_time = time + cell + 1
                
                if new_time <= time_limit:
                    if new_pos not in reached or new_time < reached[new_pos]:
                        reached[new_pos] = new_time
                        heapq.heappush(pq, (steps + 1, new_time, new_pos, path + [current]))
    
    return None, None

def LVL3_UCS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], time_limit=float('inf'), fuel_cap = float('inf')):
    rows, cols = len(board_data), len(board_data[0])
    
    initial_priority = (0, 0, 0)
    
    # Priority queue: (priority, steps, time, fuel, current_position, path)
    pq = [(initial_priority, 0, 0, fuel_cap, start, [])]
    reached = {start: (0, fuel_cap)}
    
    while pq:
        _, steps, time, fuel, current, path = heapq.heappop(pq)
        
        if time > time_limit or fuel < 0:
            continue
        
        if current == end:
            return path + [current], None
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_pos = (nx, ny)
                cell = board_data[nx][ny]
                
                # Skip blocked cells
                if cell == -1:
                    continue
                
                if str(cell)[0] == 'F':
                    new_fuel = fuel_cap
                    new_time = time + int(str(cell)[1:]) + 1
                else:
                    new_fuel = fuel - 1
                    new_time = time + cell + 1
                
                if new_pos not in reached or new_time < reached[new_pos][0] or new_fuel > reached[new_pos][1]:
                    reached[new_pos] = (new_time, new_fuel)
                    # Priority is now based on steps, with time and fuel as tiebreakers
                    priority = (steps + 1, new_time, -new_fuel)
                    heapq.heappush(pq, (priority, steps + 1, new_time, new_fuel, new_pos, path + [current]))
    
    return None, None

def generate_candidates_LVL4(block: tuple[int, int], board_data, goal, breaking):
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    if not breaking:
        neighbors.append((0, 0))  # Stand still action
    explored = []

    for neighbor in neighbors:
        x, y = block[0] + neighbor[0], block[1] + neighbor[1]
        if (
                0 <= x < len(board_data) and
                0 <= y < len(board_data[0]) and
                str(board_data[x][y]) >= '0'
        ):
            explored.append((x, y))
    explored.sort(key=lambda a: abs(goal[0] - a[0]) + abs(
        goal[1] - a[1]))  #prioritize tile closer to goal based on manhattan distance
    return explored

def LVL4_UCS(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], time_limit=float('inf'),
             fuel_cap=float('inf'), current_fuel=float('inf')):
    rows, cols = len(board_data), len(board_data[0])
    initial_priority = (0, 0, 0)

    # Priority queue: (priority, steps, time, current_position, path)
    pq = [(initial_priority, 0, 0, current_fuel, start, [])]
    reached = {start: (0, current_fuel)}

    while pq:
        _, steps, time, fuel, current, path = heapq.heappop(pq)
        # if (current == (17, 6)):
        #     print(f"Path cost: {steps}, Time: {time}, Fuel: {fuel}")

        if time > time_limit or fuel < 0:
            continue

        if current == end:
            # print(f"Path cost: {steps}, Time: {time}")
            return path + [current]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_pos = (nx, ny)
                cell = board_data[nx][ny]

                # Skip blocked cells
                if cell == -1:
                    continue

                if str(cell)[0] == 'F':
                    # print(f"Cell {cell} is fuel")
                    new_fuel = fuel_cap
                    new_time = time + int(str(cell)[1:]) + 1
                else:
                    new_fuel = fuel - 1
                    new_time = time + cell + 1

                if new_pos not in reached or new_time < reached[new_pos][0] or new_fuel > reached[new_pos][1]:
                    reached[new_pos] = (new_time, new_fuel)
                    # Priority is now based on steps, with time and fuel as tiebreakers
                    priority = (steps + 1, new_time, -new_fuel)
                    heapq.heappush(pq, (priority, steps + 1, new_time, new_fuel, new_pos, path + [current]))

    return None

