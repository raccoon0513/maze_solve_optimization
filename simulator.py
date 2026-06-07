import os
import time
from utils import get_maze_path_distance
from drone import Drone

class Simulator:
    def __init__(self, maze_obj, max_drones=32, seed_value=None, strategy_name="Single"):
        self.maze_data = maze_obj.maze
        self.goal_location = maze_obj.g_location
        self.max_drones = max_drones
        self.seed_value = seed_value
        self.strategy_name = strategy_name
        
        self.ticks = 0
        self.is_cleared = False
        self.winner = None
        
        # 데이터 추적용 변수
        self.spawn_fail_count = 0
        self.backtrack_count = 0
        self.total_spawned_drones = len(maze_obj.d_locations)
        
        # 탐색률(Coverage) 계산을 위한 전체 길 개수 파악
        self.total_path_cells = sum(row.count(1) for row in self.maze_data)
        self.visited_cells = set()
        
        distances = []
        for d_loc in maze_obj.d_locations:
            dist = get_maze_path_distance(self.maze_data, d_loc, self.goal_location)
            distances.append(dist)
            self.visited_cells.add((d_loc[0], d_loc[1])) # 초기 위치 방문 처리
            
        self.optimal_path_distance = min(distances) if distances else 0
        
        self.drones = []
        for i, d_loc in enumerate(maze_obj.d_locations):
            new_drone = Drone(i, d_loc[0], d_loc[1])
            self.drones.append(new_drone)

    def can_move(self, x, y, d):
        wall_x = x + d[0]
        wall_y = y + d[1]
        return self.maze_data[wall_x][wall_y] == 1

    def move(self, drone, d):
        # 이동 시 벽(중간 칸)과 도착 방(끝 칸)을 모두 방문 기록에 추가
        wall_x, wall_y = drone.x + d[0], drone.y + d[1]
        drone.x += d[0] * 2
        drone.y += d[1] * 2
        
        self.visited_cells.add((wall_x, wall_y))
        self.visited_cells.add((drone.x, drone.y))

    def spawn_drone(self, x, y, memory):
        active_count = sum(1 for d in self.drones if d.active)
        if active_count >= self.max_drones:
            self.spawn_fail_count += 1  # 제한 초과 시 실패 기록
            return False
            
        new_id = len(self.drones)
        new_drone = Drone(new_id, x, y, memory)
        self.drones.append(new_drone)
        self.total_spawned_drones += 1
        
        self.visited_cells.add((x, y))
        return True

    def clear(self, winner_id):
        self.is_cleared = True
        self.winner = winner_id

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        path_char, wall_char, goal_char = "  ", "▓▓", "GG"
        active_drones = [d for d in self.drones if d.active]
        gx, gy = self.goal_location
        
        print(f"--- 틱: {self.ticks} | 활성 드론: {len(active_drones)}/{self.max_drones} ---")
        for r in range(len(self.maze_data)):
            line = ""
            for c in range(len(self.maze_data[r])):
                drones_on_cell = sum(1 for d in active_drones if d.x == r and d.y == c)
                if drones_on_cell == 1: line += "DR"
                elif drones_on_cell > 1: line += f"{drones_on_cell:02d}" 
                elif r == gx and c == gy: line += goal_char
                elif self.maze_data[r][c] == 1: line += path_char
                else: line += wall_char
            print(line)
        time.sleep(0.05)

    def run(self, visualize=False):
        while not self.is_cleared:
            active_drones = [d for d in self.drones if d.active]
            if len(active_drones) == 0:
                break
                
            if visualize:
                self.render()
            
            self.ticks += 1
            for drone in active_drones:
                drone.step(self)
                if self.is_cleared:
                    if visualize: self.render()
                    break
        
        # 탐색률 계산 (%)
        coverage_percent = round((len(self.visited_cells) / self.total_path_cells) * 100, 2)
        
        # CSV에 기록할 딕셔너리 반환
        return {
            "Seed": self.seed_value,
            "Spawn_Strategy": self.strategy_name,
            "Algorithm": "Heuristic_DFS",
            "Goal_X": self.goal_location[0],
            "Goal_Y": self.goal_location[1],
            "Optimal_Tick": self.optimal_path_distance,
            "Used_Tick": self.ticks,
            "Map_Coverage_%": coverage_percent,
            "Spawn_Fail_Count": self.spawn_fail_count,
            "Backtrack_Count": self.backtrack_count,
            "Total_Spawned": self.total_spawned_drones,
            "Success": self.is_cleared
        }