import os
import time
from utils import get_maze_path_distance
from drone import Drone

class Simulator:
    def __init__(self, maze_obj, max_drones=32):
        self.maze_data = maze_obj.maze
        self.goal_location = maze_obj.g_location
        self.max_drones = max_drones
        self.ticks = 0
        self.is_cleared = False
        self.winner = None
        
        distances = []
        for d_loc in maze_obj.d_locations:
            dist = get_maze_path_distance(self.maze_data, d_loc, self.goal_location)
            distances.append(dist)
            
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
        os.system('cls' if os.name == 'nt' else 'clear')
        path_char, wall_char, goal_char = "  ", "▓▓", "GG"
        active_drones = [d for d in self.drones if d.active]
        gx, gy = self.goal_location
        
        print(f"--- 틱: {self.ticks} | 활성 드론: {len(active_drones)}/{self.max_drones} | 최단 거리(CSV용): {self.optimal_path_distance} ---")
        
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

    def run(self, visualize=True):
        while not self.is_cleared:
            active_drones = [d for d in self.drones if d.active]
            if len(active_drones) == 0:
                print("모든 드론이 길을 찾지 못하고 작동을 중지했습니다.")
                break
                
            if visualize:
                self.render()
            
            self.ticks += 1
            for drone in active_drones:
                drone.step(self)
                if self.is_cleared:
                    if visualize: self.render()
                    break
                    
        if self.is_cleared and visualize:
            print(f"\n🎉 보물 발견! [최초 도달 드론 ID: {self.winner}]")
            print(f"실제 소모 틱: {self.ticks}")
            print(f"이상적인 최단 틱: {self.optimal_path_distance}")
            print(f"탐색 효율: {(self.optimal_path_distance / self.ticks) * 100:.1f}%\n")