import random
import sys
import os
import time

sys.setrecursionlimit(10000)

class Maze:
    def __init__(self, n=32):
        self.n = n
        self.maze, self.d_location, self.g_location = self.generate_maze(n)
        
    def generate_maze(self, n):
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
        
        while True:
            px, py = random.randrange(1, maze_size, 2), random.randrange(1, maze_size, 2)
            if maze[px][py] == path:
                drone_location = (px, py)
                break
        while True:
            gx, gy = random.randrange(1, maze_size, 2), random.randrange(1, maze_size, 2)
            if maze[gx][gy] == path and (gx, gy) != drone_location:
                goal_location = (gx, gy)
                break
                
        return maze, drone_location, goal_location

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_opposite(d):
    return (-d[0], -d[1])

class Drone:
    def __init__(self, drone_id, x, y, memory=None):
        self.id = drone_id
        self.x = x
        self.y = y
        self.active = True
        
        if memory is None:
            self.memory = {
                'came_from': None,
                'backtrack_path': [],
                'missed_branches': [],
                'is_backtracking': False
            }
        else:
            self.memory = memory

    def step(self, env):
        if not self.active: return

        if (self.x, self.y) == env.goal_location:
            env.clear(winner_id=self.id)
            return

        if self.memory['is_backtracking']:
            target = self.memory['missed_branches'][-1]
            if (self.x, self.y) == (target[0], target[1]):
                self.memory['is_backtracking'] = False
                d = target[2]
                self.memory['missed_branches'].pop()
                self._move_forward(env, d)
            else:
                back_dir = self.memory['backtrack_path'].pop()
                env.move(self, back_dir)
            return

        # 1. 뚫려있는 길 탐색 (기존과 동일)
        came_from = self.memory.get('came_from')
        open_dirs = []
        for d in DIRECTIONS:
            if d != came_from and env.can_move(self.x, self.y, d):
                open_dirs.append(d)

        # 막다른 길 처리 로직... (기존과 동일)

        # 💡 2. 휴리스틱 판단: 보물과 가까워지는 순서대로 방향 정렬
        gx, gy = env.goal_location
        open_dirs.sort(key=lambda d: manhattan_distance(self.x + d[0]*2, self.y + d[1]*2, gx, gy))

        # 3. 분기점 처리 로직 (기존과 동일)
        for d in open_dirs[1:]:
            # 자식 드론이 태어날 위치를 이미 할당받은 길 방향으로 1칸(실제 배열상 2칸) 전진시킴
            new_x = self.x + d[0] * 2
            new_y = self.y + d[1] * 2
            
            new_memory = {
                'came_from': get_opposite(d),
                'backtrack_path': [get_opposite(d)], # 이미 1칸 전진했으니 돌아갈 발자취도 하나 남겨줌
                'missed_branches': [],
                'is_backtracking': False
            }
            
            # 교차로가 아닌 새 경로 위에서 드론 소환 시도
            success = env.spawn_drone(new_x, new_y, new_memory)
            if not success:
                # 제한에 걸려 소환 실패 -> 부모 드론이 이 교차로 위치와 방향을 기억해둠
                self.memory['missed_branches'].append((self.x, self.y, d))

        # 본체는 첫 번째 열린 길로 전진
        self._move_forward(env, open_dirs[0])

    def _move_forward(self, env, d):
        env.move(self, d)
        self.memory['came_from'] = get_opposite(d)
        self.memory['backtrack_path'].append(get_opposite(d))

class Simulator:
    def __init__(self, maze_obj, max_drones=32):
        self.maze_data = maze_obj.maze
        self.goal_location = maze_obj.g_location
        self.max_drones = max_drones
        self.ticks = 0
        self.is_cleared = False
        self.winner = None
        
        self.drones = []
        first_drone = Drone(0, maze_obj.d_location[0], maze_obj.d_location[1])
        self.drones.append(first_drone)

    def can_move(self, x, y, d):
        wall_x = x + d[0]
        wall_y = y + d[1]
        return self.maze_data[wall_x][wall_y] == 1

    def move(self, drone, d):
        drone.x += d[0] * 2
        drone.y += d[1] * 2

    def spawn_drone(self, x, y, memory):
        active_count = sum(1 for d in self.drones if d.active)
        if active_count >= self.max_drones:
            return False
            
        new_id = len(self.drones)
        new_drone = Drone(new_id, x, y, memory)
        self.drones.append(new_drone)
        return True

    def clear(self, winner_id):
        self.is_cleared = True
        self.winner = winner_id

    def render(self):
        # 터미널 화면 지우기 (애니메이션 효과)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        path_char = "  "
        wall_char = "▓▓"
        goal_char = "GG"
        
        active_drones = [d for d in self.drones if d.active]
        gx, gy = self.goal_location
        
        print(f"--- 틱(Tick): {self.ticks} | 활성 드론: {len(active_drones)}/{self.max_drones} ---")
        
        for r in range(len(self.maze_data)):
            line = ""
            for c in range(len(self.maze_data[r])):
                # 현재 좌표에 겹쳐 있는 활성 드론의 수를 계산
                drones_on_cell = sum(1 for d in active_drones if d.x == r and d.y == c)
                
                if drones_on_cell == 1:
                    line += "DR"  # 1대만 있으면 DR
                elif drones_on_cell > 1:
                    # 여러 대가 겹치면 숫자로 표시 (예: 2대면 02, 3대면 03)
                    line += f"{drones_on_cell:02d}" 
                elif r == gx and c == gy:
                    line += goal_char
                elif self.maze_data[r][c] == 1:
                    line += path_char
                else:
                    line += wall_char
            print(line)
        
        # 프레임 간 딜레이
        time.sleep(0.05)

    def run(self):
        while not self.is_cleared:
            active_drones = [d for d in self.drones if d.active]
            if len(active_drones) == 0:
                print("모든 드론이 길을 찾지 못하고 작동을 중지했습니다.")
                break
                
            self.render()
            
            self.ticks += 1
            for drone in active_drones:
                drone.step(self)
                if self.is_cleared:
                    self.render() # 클리어 시 최종 화면 렌더링
                    break
                    
        if self.is_cleared:
            print(f"\n🎉 보물 발견! [최초 도달 드론 ID: {self.winner}]")
            print(f"총 소모 틱(프레임): {self.ticks}")
            print(f"총 소환된 드론 수: {len(self.drones)}대\n")

if __name__ == "__main__":
    n = 32 # 시각적으로 한눈에 보기 편하도록 15로 임시 조정 (원래는 32)
    max_limit = 32
    
    maze_env = Maze(n)
    sim = Simulator(maze_env, max_drones=max_limit)
    sim.run()