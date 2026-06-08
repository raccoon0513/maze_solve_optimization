from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_opposite(d):
    return (-d[0], -d[1])

def get_maze_path_distance(maze_data, start_loc, goal_loc):
    queue = deque([(start_loc[0], start_loc[1], 0)])
    visited = set()
    visited.add((start_loc[0], start_loc[1]))

    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == goal_loc:
            return dist

        # maze_data[x][y] 안에는 현재 위치에서 이동 가능한 방향(dx, dy) 리스트가 들어있음
        for dx, dy in maze_data[x][y]:
            next_x, next_y = x + dx, y + dy
            if (next_x, next_y) not in visited:
                visited.add((next_x, next_y))
                queue.append((next_x, next_y, dist + 1))
                    
    return -1