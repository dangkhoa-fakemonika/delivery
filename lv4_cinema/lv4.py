def generate_neighbor_LVL4(block: tuple[int, int], board_data, reached: dict, goal):
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
    explored.sort(key=lambda a: abs(goal[0] - a[0]) + abs(goal[1] - a[1]))  #  Prioritize tile closer to goal based on manhattan distance
    return explored


def generate_time_cost(board_data: list[list[int]], path: list[tuple[int, int]]):
    if path is None:
        return 0
    total_time = 0
    for step in path:
        total_time += int(str(board_data[step[0]][step[1]]).strip('F')) + 1

    return total_time - 1


def get_timed_path(board_data, path):
    timed_path = []

    total_cost = 0
    total_time = 0
    stopped_time = 0

    while total_time <= generate_time_cost(board_data, path):
        timed_path.append(path[total_cost])

        total_time += 1
        stopped_time += 1
        current_block = board_data[path[total_cost][0]][path[total_cost][1]]

        if int(str(current_block).strip('F')) + 1 == stopped_time:  # Has finished through a cell
            stopped_time = 0
            total_cost += 1

    return timed_path


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
    explored.sort(key=lambda x: abs(goal[0] - x[0]) + abs(
        goal[1] - x[1]))  #prioritize tile closer to goal based on manhattan distance
    return explored


def LVL4(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], limit=float('inf'),
         fuel_cap=float('inf'), current_fuel=float('inf')):
    for step in range(0, len(board_data) * len(board_data[0])):
        # print('maxstep = ', step)
        reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
        path = [start]
        if LVL4_Backtracking(board_data, start, end, step, 0, limit, current_fuel, fuel_cap, path, reached):
            # print(step, 'step')
            return path

    return None


def LVL4_Backtracking(board_data: list[list[int]], current: tuple[int, int], end: tuple[int, int], remaining_step: int,
                      cur_time: int, time_limit: int, cur_fuel: int, fuel_cap: int, cur_path: list[int, int],
                      reached: dict[tuple[int, int]: tuple[int, int]]):
    if current == end:
        if cur_time <= time_limit:
            return True
        else:
            return False

    if remaining_step <= 0 or cur_fuel <= 0 or cur_time >= time_limit:
        return False
    if str(board_data[current[0]][current[1]])[0] == 'F':  # is a fuel station
        added_time_cost = int((board_data[current[0]][current[1]])[1:]) + 1
        cur_fuel = fuel_cap
    else:
        added_time_cost = board_data[current[0]][current[1]] + 1
    explored = generate_neighbor_LVL4(current, board_data, reached, end)
    for nods in explored:
        reached[nods] = current
        if str(board_data[nods[0]][nods[1]])[0] == 'F':  # is a fuel station
            new_reached: dict[tuple[int, int]: tuple[int, int]] = {nods: -1}
            cur_path.append(nods)
            # print('fuel station reached at', current, ', remaining step: ', remaining_step)
            if LVL4_Backtracking(board_data, nods, end, remaining_step - 1, cur_time + added_time_cost, time_limit,
                                 fuel_cap, fuel_cap, cur_path, new_reached):
                return True
            cur_path.pop()
            new_reached.pop(nods)
        cur_path.append(nods)
        if LVL4_Backtracking(board_data, nods, end, remaining_step - 1, cur_time + added_time_cost, time_limit,
                             cur_fuel - 1, fuel_cap, cur_path, reached):
            return True
        reached.pop(nods)
        cur_path.pop()
    return False
