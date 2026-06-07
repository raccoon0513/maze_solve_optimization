import sys
import random
import csv
import os
import threading
from maze import Maze
from simulator import Simulator

sys.setrecursionlimit(10000)

# 전역 종료 플래그
keep_running = True

def wait_for_exit():
    """백그라운드에서 사용자의 입력을 대기하는 함수"""
    global keep_running
    input()  # 사용자가 Enter를 누를 때까지 대기
    keep_running = False
    print("\n\n🛑 종료 신호 접수됨: 현재 진행 중인 미로 탐색까지만 완료하고 안전하게 저장한 뒤 종료합니다...")

if __name__ == "__main__":
    n = 32                 
    max_limit = 32         
    
    # 1, 2, 4, 8, 16, 32 단위로 테스트하는 전략 리스트
    strategies = [{"name": i, "count": i} for i in [1, 2, 4, 8, 16, 32]]
    
    csv_filename = "simulation_results.csv"
    
    # 💡 [수정된 부분] fieldnames에 "Initial_Drones_XY" 칼럼 추가
    fieldnames = [
        "Seed", "Spawn_Strategy", "Initial_Drones_XY", "Goal_X", "Goal_Y", 
        "Optimal_Tick", "Used_Tick", "Map_Coverage_%", 
        "Spawn_Fail_Count", "Backtrack_Count", "Total_Spawned", "Success"
    ]
    
    # 💡 파일이 이미 존재하는지 확인
    file_exists = os.path.isfile(csv_filename)
    
    # 💡 mode="a" (Append)로 변경하여 기존 내용을 보존
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 💡 파일이 처음 만들어질 때(새 파일일 때)만 헤더를 작성
        if not file_exists:
            writer.writeheader()
        
        print("🚀 데이터 추출 시작... (종료하려면 터미널에서 '엔터(Enter)' 키를 누르세요!)")
        
        # 입력을 대기하는 스레드를 백그라운드(daemon)로 실행
        exit_thread = threading.Thread(target=wait_for_exit, daemon=True)
        exit_thread.start()
        
        simulation_count = 0
        
        # 무한 루프 대신 플래그 상태를 확인하며 반복
        while keep_running:
            current_seed = random.randint(100000, 999999)
            
            for strategy in strategies:
                random.seed(current_seed) 
                
                maze_env = Maze(n, num_initial_drones=strategy["count"])
                
                sim = Simulator(maze_env, max_drones=max_limit, 
                                seed_value=current_seed, 
                                strategy_name=strategy["name"])
                
                result_data = sim.run(visualize=False)
                writer.writerow(result_data)
                
            file.flush() 
            simulation_count += 1
            
            # 종료 신호가 들어오지 않았을 때만 진행률 출력
            if simulation_count % 10 == 0 and keep_running:
                print(f"진행 상황: {simulation_count} 세트 완료 (현재까지 총 {simulation_count * len(strategies)}줄 기록됨)")
                    
    print(f"\n✅ 안전하게 종료되었습니다! 총 {simulation_count} 세트(데이터 {simulation_count * len(strategies)}개)가 '{csv_filename}'에 완벽하게 보존되었습니다.")