import random
import math

class Maze:
    def __init__(self, n=32, num_initial_drones=1):
        self.n = n
        self.maze, self.d_locations, self.g_location = self.generate_maze(n, num_initial_drones)
        
    def generate_maze(self, n, num_initial_drones):
        maze = [[[] for _ in range(n)] for _ in range(n)]
        visited = [[False for _ in range(n)] for _ in range(n)]
        
        def backtrack(r, c):
            visited[r][c] = True
            local_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(local_directions)
            
            for dr, dc in local_directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                    maze[r][c].append((dr, dc))
                    maze[nr][nc].append((-dr, -dc))
                    backtrack(nr, nc)    
        
        backtrack(0, 0)
        
        drone_locations = []
        if num_initial_drones > 0:
            cols = int(math.sqrt(num_initial_drones))
            while num_initial_drones % cols != 0:
                cols -= 1
            rows = num_initial_drones // cols
            
            for i in range(rows):
                for j in range(cols):
                    r_start = i * n // rows
                    r_end = (i + 1) * n // rows - 1
                    c_start = j * n // cols
                    c_end = (j + 1) * n // cols - 1
                    
                    center_r = (r_start + r_end) // 2
                    center_c = (c_start + c_end) // 2
                    
                    # 물리적 좌표 변환 없이 순수 32x32 인덱스 자체가 좌표가 됨
                    drone_locations.append((center_r, center_c))
                    
        while True:
            gx, gy = random.randrange(0, n), random.randrange(0, n)
            if (gx, gy) not in drone_locations:
                goal_location = (gx, gy)
                break
                
        return maze, drone_locations, goal_location