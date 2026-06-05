import random
import sys
sys.setrecursionlimit(10000)
class Maze():
    def __init__(self, n):
        self.maze, self.p_location, self.g_location = self.generate_maze(n)
    def generate_maze(self, n):
        wall = 0
        path = 1
        player = 2
        goal = 3
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
        while True:
            px = random.randrange(1, maze_size, 2) 
            py = random.randrange(1, maze_size, 2)
            if maze[px][py] == path:
                maze[px][py] = player
                player_location = (px, py)
                break
        while True:
            gx = random.randrange(1, maze_size, 2)
            gy = random.randrange(1, maze_size, 2)
            if maze[gx][gy] == path: 
                maze[gx][gy] = goal
                goal_location = (gx, gy)
                break
                
        return maze, player_location, goal_location

    def print_maze(self):
        path = "  "
        wall = "▓▓"
        player = "PP"
        goal = "GG"
        objects = [wall, path, player, goal] 
        for row in self.maze:
            line = ""
            for i in row:
                line += objects[i]
            print(line)

if __name__ == "__main__":
    n = 10
    maze = Maze(n)
    print(f"Player Location: {maze.p_location}")
    print(f"Goal Location: {maze.g_location}")
    maze.print_maze()