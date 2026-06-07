from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_opposite(d):
    return (-d[0], -d[1])

def get_maze_path_distance(maze_data, start_loc, goal_loc):
    """BFS를 이용해 실제 미로 경로상의 최단 물리 거리를 구합니다."""
    queue = deque([(start_loc[0], start_loc[1], 0)])
    visited = set()
    visited.add((start_loc[0], start_loc[1]))

    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == goal_loc:
            return dist

        for dx, dy in DIRECTIONS:
            wall_x, wall_y = x + dx, y + dy
            next_x, next_y = x + 2 * dx, y + 2 * dy

            if 0 <= next_x < len(maze_data) and 0 <= next_y < len(maze_data[0]):
                if maze_data[wall_x][wall_y] == 1 and (next_x, next_y) not in visited:
                    visited.add((next_x, next_y))
                    queue.append((next_x, next_y, dist + 1))
                    
    return -1