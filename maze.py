import random

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
        
        drone_locations = []
        for _ in range(num_initial_drones):
            while True:
                px, py = random.randrange(1, maze_size, 2), random.randrange(1, maze_size, 2)
                if maze[px][py] == path and (px, py) not in drone_locations:
                    drone_locations.append((px, py))
                    break
                    
        while True:
            gx, gy = random.randrange(1, maze_size, 2), random.randrange(1, maze_size, 2)
            if maze[gx][gy] == path and (gx, gy) not in drone_locations:
                goal_location = (gx, gy)
                break
                
        return maze, drone_locations, goal_location