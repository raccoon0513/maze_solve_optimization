import random
import math

class Maze:
    def __init__(self, n=32, num_initial_drones=1):
        self.n = n
        self.maze, self.d_locations, self.g_location = self.generate_maze(n, num_initial_drones)
        
    def generate_maze(self, n, num_initial_drones):
        wall = 0
        path = 1
        maze_size = 2 * n + 1
        maze = [[wall for _ in range(maze_size)] for _ in range(maze_size)]
        visited = [[False for _ in range(n)] for _ in range(n)]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        def backtrack(r, c):
            visited[r][c] = True
            maze[2 * r + 1][2 * c + 1] = path
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                    maze[2 * r + 1 + dr][2 * c + 1 + dc] = path
                    backtrack(nr, nc)    
        
        backtrack(0, 0)
        
        # --- [수정된 구역 분할 및 중앙 스폰 로직] ---
        drone_locations = []
        
        if num_initial_drones > 0:
            # 1. 드론 개수에 맞춰 맵을 나눌 행(rows)과 열(cols)의 개수를 계산 (가장 정사각형에 가까운 비율로 분할)
            cols = int(math.sqrt(num_initial_drones))
            while num_initial_drones % cols != 0:
                cols -= 1
            rows = num_initial_drones // cols
            
            # 2. 쪼개진 구역마다 순회를 돌며 정중앙 좌표를 계산
            for i in range(rows):
                for j in range(cols):
                    # 현재 구역의 논리적 맵 인덱스 범위 계산
                    r_start = i * n // rows
                    r_end = (i + 1) * n // rows - 1
                    c_start = j * n // cols
                    c_end = (j + 1) * n // cols - 1
                    
                    # 해당 구역의 정중앙 인덱스 산출
                    center_r = (r_start + r_end) // 2
                    center_c = (c_start + c_end) // 2
                    
                    # 미로 배열의 물리적 좌표(무조건 홀수인 '방' 위치)로 변환
                    px = 2 * center_r + 1
                    py = 2 * center_c + 1
                    
                    drone_locations.append((px, py))
                    
        # --- [목적지 생성 로직] ---
        while True:
            gx, gy = random.randrange(1, maze_size, 2), random.randrange(1, maze_size, 2)
            if maze[gx][gy] == path and (gx, gy) not in drone_locations:
                goal_location = (gx, gy)
                break
                
        return maze, drone_locations, goal_location