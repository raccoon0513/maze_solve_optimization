import random
import sys

# 재귀 깊이 제한 해제 (미로 크기가 커질 때 파이썬의 기본 재귀 한도 초과 방지)
sys.setrecursionlimit(10000)

class Maze():
    def __init__(self, n):
        self.maze = self.generate_maze(n)
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
        for item in [player, goal]:
            x,y = -1,-1
            while(True):
                x = random.randrange(0, maze_size, 1)
                y = random.randrange(0, maze_size, 1)
                if maze[x][y] == 1 and not (maze[x][y] in [player, goal]):
                    maze[x][y] = item
                    break
        return maze

    def print_maze(self):
        path = "▓▓"
        wall = "░░"
        player = "PP"
        goal = "GG"
        objects = [path, wall, player, goal]
        for row in self.maze:
            line = ""
            for i in row:
                line+= objects[i]
            print(line)
if __name__ == "__main__":
    n = 10
    maze = Maze(n)
    print(maze.maze)
    maze.print_maze()