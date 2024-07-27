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

def generate_neighbor_LVL3(block: tuple[int, int], board_data, reached: dict, goal):
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    explored = []

    for neighbor in neighbors:
        x, y = block[0] + neighbor[0], block[1] + neighbor[1]
        if (
            0 <= x < len(board_data) and
            0 <= y < len(board_data[0]) and 
            (x, y) not in reached and
            str(board_data[x][y]) >= '0'
        ):
            explored.append((x, y))
    explored.sort(key=lambda x: abs(goal[0] - x[0]) + abs(goal[1] - x[1])) #prioritize tile closer to goal based on manhattan distance 
    return explored

def generate_neighbor_LVL3_alter(block: tuple[int, int], board_data, reached: dict, goal):
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    explored = []

    for neighbor in neighbors:
        x, y = block[0] + neighbor[0], block[1] + neighbor[1]
        if (
            0 <= x < len(board_data) and
            0 <= y < len(board_data[0]) and 
            #(x, y) not in reached and
            str(board_data[x][y]) >= '0'
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


def generate_time_cost(board_data: list[list[int]], path: list[tuple[int, int]], level):
    if path is None:
        return 0
    if level == 'lvl4':
        return len(path[0])

    total_time = len(path) - 1

    for step in path:
        if level in ('lvl2', 'lvl3') and str(board_data[step[0]][step[1]])[0] != 'F':
            total_time += board_data[step[0]][step[1]]
        elif level == 'lvl3' and str(board_data[step[0]][step[1]])[0] == 'F':
            total_time += int(str(board_data[step[0]][step[1]]).strip('F'))

    return total_time


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


def LVL2_UCS(board_data : list[list[int]], start : tuple[int, int], end : tuple[int, int], time_limit=float('inf')):
    rows, cols = len(board_data), len(board_data[0])
    
    # Priority queue: (path_cost, time, current_position, path)
    pq = [(0, 0, start, [])]
    reached = set()

    while pq:
        path_cost, time, current, path = heapq.heappop(pq)
        
        if current == end and time <= time_limit:
            print(f"Path cost: {path_cost}, Time: {time}")
            return path + [current], []
        
        if (current, path_cost) in reached or time > time_limit:
            continue
        
        reached.add((current, path_cost))
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_pos = (nx, ny)
                cell = board_data[nx][ny]
                
                # Skip blocked cells
                if cell == -1:
                    continue
                
                new_path_cost = path_cost + 1
                
                # Ignore gas station
                if str(cell)[0] == 'F':
                    new_time = time + 1
                else:
                    new_time = time + cell + 1
                
                if new_time <= time_limit:
                    new_path = path + [current]
                    heapq.heappush(pq, (new_path_cost, new_time, new_pos, new_path))
    
    return None, None

def LVL3(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], limit=float('inf'), fuel_cap = float('inf')):
    for step in range (0, len(board_data) * len(board_data[0])):
        print('maxstep = ', step)
        reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
        path = [start]
        if LVL3_Backtracking(board_data, start, end, step, 0, limit, fuel_cap, fuel_cap, path, reached):
            print(step, 'step')
            return path, None

    return None, None


def LVL3_Backtracking(board_data: list[list[int]], current: tuple[int, int], end: tuple[int, int], remaining_step: int, cur_time: int, time_limit: int, cur_fuel: int, fuel_cap: int, cur_path: list[int, int], reached: dict[tuple[int, int]: tuple[int, int]]):
    #Base case
    if current == end:
        if cur_time <= time_limit:
            return True
        else:
            return False
    #If these conditions are violated, further exploration becomes meaningless because it's already an invalid path, so we return early
    if remaining_step <= 0 or cur_fuel <= 0 or cur_time >= time_limit: 
        return False
    if str(board_data[current[0]][current[1]])[0] == 'F': #is a fuel station
        added_time_cost = int((board_data[current[0]][current[1]])[1:]) + 1
        cur_fuel = fuel_cap
    else:
        added_time_cost = board_data[current[0]][current[1]] + 1
    explored = generate_neighbor_LVL3(current, board_data, reached, end)
    for nods in explored:
        if str(board_data[nods[0]][nods[1]])[0] == 'F': #if it's a fuel station, we reset the reached map by create a new one in order to allow past tiles to be traversed
            new_reached: dict[tuple[int, int]: tuple[int, int]] = {nods: -1}
            cur_path.append(nods)
            if LVL3_Backtracking(board_data, nods, end, remaining_step - 1, cur_time + added_time_cost, time_limit, fuel_cap, fuel_cap, cur_path, new_reached):
                return True
            new_reached.pop(nods)
            cur_path.pop()     
        else: #default recursive case, call the recursion function on the neighbor tile with updated status(remaining step, current time, current fule)
            reached[nods] = current
            cur_path.append(nods)
            if LVL3_Backtracking(board_data, nods, end, remaining_step - 1, cur_time + added_time_cost, time_limit, cur_fuel - 1, fuel_cap, cur_path, reached):
                return True
            reached.pop(nods)
            cur_path.pop()
    return False

# Still in progress
def LVL3_UCS(board_data, start, end, time_limit=float('inf'), fuel_cap=float('inf')):
    rows, cols = len(board_data), len(board_data[0])
    
    # Priority queue: (priority, path cost, time, fuel, current_position, path)
    pq = [(0, 0, 0, fuel_cap, start, [])]
    visited = set()

    while pq:
        _, path_cost, time, fuel, current, path = heapq.heappop(pq)
        
        if current == end and time <= time_limit:
            return path + [current], []
        
        if (current, fuel) in visited or time > time_limit or fuel < 0:
            continue
        
        visited.add((current, fuel))
        
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
                    new_time = time + cell
                    new_path_cost = path_cost + 1
                
                if new_time <= time_limit and new_fuel >= 0:
                    new_path = path + [current]
                    # Priority considers path cost, and remaining fuel
                    priority = path_cost - (new_fuel / fuel_cap)
                    heapq.heappush(pq, (priority, new_path_cost, new_time, new_fuel, new_pos, new_path))
    
    return None, None  # No path found

def LVL3_alter(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], time_limit=float('inf'), fuel_cap = float('inf')):
    path = []
    if LVL3_Recursive_alter(board_data, start, end, time_limit, fuel_cap, path):
        return path, None

    return None, None


def LVL3_Recursive_alter(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], time_limit: int, fuel_cap: int, cur_path: list[int, int]):
    reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
    frontier: list[tuple[int, int]] = [start]
    time_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    road_cost = [[float('inf') for _ in range(len(board_data))] for __ in range(len(board_data))]
    expansion: list[tuple[int, int]] = []
    candidate: list[tuple[int, int]] = []
    shortest_path: list[tuple[int, int]] = []

    if str(board_data[start[0]][start[1]])[0] == 'F':
        time_cost[start[0]][start[1]] = int((board_data[start[0]][start[1]])[1:])
    else:
        time_cost[start[0]][start[1]] = board_data[start[0]][start[1]]
    road_cost[start[0]][start[1]] = 0
    
    while True:
        if len(frontier) == 0:
            break
        
        current_node = frontier.pop(0)
        expansion.append(current_node)
        if time_cost[current_node[0]][current_node[1]] < time_limit and road_cost[current_node[0]][current_node[1]] < fuel_cap:
            explored = generate_neighbor_LVL3_alter(current_node, board_data, reached, end)
            for nods in explored:
                if str(board_data[nods[0]][nods[1]])[0] == 'F': #is a fuel station
                    added_time_cost = int((board_data[nods[0]][nods[1]])[1:]) + 1
                else:
                    added_time_cost = board_data[nods[0]][nods[1]] + 1
                if nods not in reached or time_cost[nods[0]][nods[1]] > time_cost[current_node[0]][current_node[1]] + added_time_cost:
                    time_cost[nods[0]][nods[1]] = time_cost[current_node[0]][current_node[1]] + added_time_cost
                    road_cost[nods[0]][nods[1]] = road_cost[current_node[0]][current_node[1]] + 1
                    reached[nods] = current_node
                    if str(board_data[nods[0]][nods[1]])[0] != 'F': 
                        frontier.append(nods)
                        if nods == end and time_cost[nods[0]][nods[1]] <= time_limit:
                            cur_path += generate_path(reached, start, end)
                            if len(shortest_path) == 0 or len(shortest_path) > len(cur_path):           
                                shortest_path = copy.deepcopy(cur_path)
                    else:
                        candidate.append(nods)
            frontier.sort(key=lambda x: road_cost[x[0]][x[1]])
    for nods in candidate:
        temp_path = []
        if LVL3_Recursive_alter(board_data, nods, end, time_limit - (time_cost[nods[0]][nods[1]] - 1), fuel_cap, temp_path):
            new_path = generate_path(reached, start, nods) 
            new_path.pop()
            new_path += temp_path
            if len(shortest_path) == 0 or len(shortest_path) > len(new_path):
                shortest_path = copy.deepcopy(new_path)
    if (len(shortest_path) != 0):
        cur_path.clear()
        cur_path += shortest_path
        return True
    else:
        return False

