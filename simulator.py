import os
import time
from utils import get_maze_path_distance
from drone import Drone

class Simulator:
    def __init__(self, maze_obj, max_drones=32, seed_value=None, strategy_name="Single"):
        self.n = maze_obj.n
        self.maze_data = maze_obj.maze
        self.goal_location = maze_obj.g_location
        self.max_drones = max_drones
        self.seed_value = seed_value
        self.strategy_name = strategy_name
        
        self.initial_d_locations = maze_obj.d_locations
        
        self.ticks = 0
        self.is_cleared = False
        self.winner = None
        
        self.spawn_fail_count = 0
        self.backtrack_count = 0
        self.total_spawned_drones = len(maze_obj.d_locations)
        
        # 탐색률 분모가 이제 완벽하게 n * n 으로 고정됨
        self.total_path_cells = self.n * self.n
        self.visited_cells = set()
        
        distances = []
        for d_loc in maze_obj.d_locations:
            dist = get_maze_path_distance(self.maze_data, d_loc, self.goal_location)
            distances.append(dist)
            self.visited_cells.add((d_loc[0], d_loc[1])) 
            
        self.optimal_path_distance = min(distances) if distances else 0
        
        self.drones = []
        for i, d_loc in enumerate(maze_obj.d_locations):
            new_drone = Drone(i, d_loc[0], d_loc[1])
            self.drones.append(new_drone)

    def can_move(self, x, y, d):
        # 얇은 벽 검사: 가고자 하는 방향 d가 현재 방의 '뚫린 방향 리스트' 안에 있는가?
        return d in self.maze_data[x][y]

    def move(self, drone, d):
        drone.x += d[0]
        drone.y += d[1]
        self.visited_cells.add((drone.x, drone.y))

    def spawn_drone(self, x, y, memory):
        active_count = sum(1 for d in self.drones if d.active)
        if active_count >= self.max_drones:
            self.spawn_fail_count += 1
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
        active_drones = [d for d in self.drones if d.active]
        gx, gy = self.goal_location
        
        print(f"--- 틱: {self.ticks} | 활성 드론: {len(active_drones)}/{self.max_drones} ---")
        
        for r in range(self.n):
            # 1. 방 위의 천장(북쪽 벽) 선 그리기
            top_line = "+"
            for c in range(self.n):
                if (-1, 0) in self.maze_data[r][c]:
                    top_line += "   +" # 북쪽이 뚫려있음
                else:
                    top_line += "---+" # 북쪽이 막혀있음
            print(top_line)
            
            # 2. 방 안쪽 내용 및 좌측(서쪽) 벽 그리기
            room_line = ""
            for c in range(self.n):
                if (0, -1) in self.maze_data[r][c]:
                    room_line += " "   # 서쪽이 뚫려있음
                else:
                    room_line += "|"   # 서쪽이 막혀있음
                    
                drones_on_cell = sum(1 for d in active_drones if d.x == r and d.y == c)
                if drones_on_cell == 1: room_line += " D "
                elif drones_on_cell > 1: room_line += f"{drones_on_cell:02d} "
                elif r == gx and c == gy: room_line += " G "
                else: room_line += "   "
                
            room_line += "|" # 가장 오른쪽 닫는 벽
            print(room_line)
            
        # 3. 미로 가장 아랫단 닫는 벽
        print("+" + "---+" * self.n)
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
        
        coverage_percent = round((len(self.visited_cells) / self.total_path_cells) * 100, 2)
        
        return {
            "Seed": self.seed_value,
            "Spawn_Strategy": self.strategy_name,
            "Initial_Drones_XY": str(self.initial_d_locations),
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