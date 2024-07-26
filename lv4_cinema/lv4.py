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
    explored.sort(key=lambda x: abs(goal[0] - x[0]) + abs(
        goal[1] - x[1]))  #prioritize tile closer to goal based on manhattan distance
    return explored


def give_location(board_data, path_movement, time):
    total_cost = 0
    total_time = 0
    stopped_time = 0

    while total_time < time - 1:
        total_time += 1
        stopped_time += 1
        current_block = board_data[path_movement[total_cost][0]][path_movement[total_cost][1]]

        if int(str(current_block).strip('F')) + 1 == stopped_time:  # Has finished through a cell
            stopped_time = 0
            total_cost += 1

    return path_movement[total_cost]


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
        neighbors.append((0, 0)) # Stand still action
    explored = []

    for neighbor in neighbors:
        x, y = block[0] + neighbor[0], block[1] + neighbor[1]
        if (
            0 <= x < len(board_data) and
            0 <= y < len(board_data[0]) and
            str(board_data[x][y]) >= '0'
        ):
            explored.append((x, y))
    explored.sort(key=lambda x: abs(goal[0] - x[0]) + abs(goal[1] - x[1])) #prioritize tile closer to goal based on manhattan distance
    return explored


def LVL3(board_data: list[list[int]], start: tuple[int, int], end: tuple[int, int], limit=float('inf'),
         fuel_cap=float('inf'), current_fuel=float('inf')):
    for step in range(0, len(board_data) * len(board_data[0])):
        # print('maxstep = ', step)
        reached: dict[tuple[int, int]: tuple[int, int]] = {start: -1}
        path = [start]
        if LVL3_Backtracking(board_data, start, end, step, 0, limit, current_fuel, fuel_cap, path, reached):
            # print(step, 'step')
            return path

    return None


def LVL3_Backtracking(board_data: list[list[int]], current: tuple[int, int], end: tuple[int, int], remaining_step: int,
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
    explored = generate_neighbor_LVL3(current, board_data, reached, end)
    for nods in explored:
        reached[nods] = current
        if str(board_data[nods[0]][nods[1]])[0] == 'F':  # is a fuel station
            new_reached: dict[tuple[int, int]: tuple[int, int]] = {nods: -1}
            cur_path.append(nods)
            # print('fuel station reached at', current, ', remaining step: ', remaining_step)
            if LVL3_Backtracking(board_data, nods, end, remaining_step - 1, cur_time + added_time_cost, time_limit,
                                 fuel_cap, fuel_cap, cur_path, new_reached):
                return True
            cur_path.pop()
            new_reached.pop(nods)
        cur_path.append(nods)
        if LVL3_Backtracking(board_data, nods, end, remaining_step - 1, cur_time + added_time_cost, time_limit,
                             cur_fuel - 1, fuel_cap, cur_path, reached):
            return True
        reached.pop(nods)
        cur_path.pop()
    return False


def LVL4_RESOLVE_PATHS(board_data: list[list[int]], paths, starts: list[tuple[int, int]], ends: list[tuple[int, int]],
                 limit=float('inf'),
                 fuel_cap=float('inf')):
    min_time = float('inf')
    # Find all path:
    for i in range(len(starts)):
        get_path = LVL3(board_data, starts[i], ends[i], limit, fuel_cap)
        if generate_time_cost(board_data, get_path) < min_time:
            min_time = len(get_path)

    conflict_points: dict = {}

    for i in range(min_time):
        pos: dict = {}
        list_pos = []

        for path in paths:
            l = give_location(board_data, path, i)
            if l not in pos:
                pos[l] = 1
            else:
                pos[l] += 1
            list_pos.append(l)

        for p in pos:
            if pos[p] > 1:
                conflict_points[(i, p[0], p[1])] = []
                for fi in range(len(list_pos)):
                    if p == list_pos[fi]:
                        conflict_points[(i, p[0], p[1])].append(fi)

    # Try to search for alternative pathing for each conflict
    if len(conflict_points) == 0:
        return paths
    else:
        for conflicts in conflict_points:
            for points in conflict_points[conflicts]:
                pass


def LVL4_EXTREME(board_data: list[list[int]], starts: list[tuple[int, int]], ends: list[tuple[int, int]],
                 limit=float('inf'),
                 fuel_cap=float('inf')):
    paths = []
    min_time = float('inf')
    # Find all path:
    for i in range(len(starts)):
        get_path = LVL3(board_data, starts[i], ends[i], limit, fuel_cap, fuel_cap)
        paths.append(get_path)
        # print(get_path)
        if generate_time_cost(board_data, get_path) < min_time:
            min_time = len(get_path)
            # print(min_time)

    # print(LVL4_RESOLVE_PATHS(board_data, paths, starts, ends, limit, fuel_cap))

#
# #
# # graph = [
# #     [0, 0, 0, -1, -1, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, -1, 0, -1],
# #     [0, 0, -1, -1, -1, 0, 0, -1, 0, -1],
# #     [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
# #     [0, 0, -1, -1, -1, 0, 0, -1, -1, 0],
# #     [0, 0, -1, 0, 0, 0, 0, 0, -1, 0],
# #     [0, 0, 0, 0, -1, 0, -1, 0, -1, 0],
# #     [0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
# #     [0, -1, -1, -1, -1, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, -1, -1, -1, 0],
# # ]
#
# graph = [
#     [0, 0, 0, 0, 0],
#     [-1, -1, 0, -1, -1],
#     [0, 0, 0, 0, 0],
#     [-1, -1, 0, -1, -1],
#     [0, 0, 0, 0, 0]
# ]
#
# starts = [(0, 0), (2, 0), (4, 0)]
# ends = [(2, 4), (4, 4), (0, 4)]
#
# LVL4_EXTREME(graph, starts, ends)
#
#
