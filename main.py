import sys
import random
import csv
from maze import Maze
from simulator import Simulator

sys.setrecursionlimit(10000)

if __name__ == "__main__":
    n = 32                 
    max_limit = 32         
    total_simulations = 100  # 추출할 데이터 수
    
    # 2가지 전략 비교 설정
    strategies = [
        {"name": "Single_Spawn", "count": 1},
        {"name": "Quad_Spawn", "count": 4}
    ]
    
    csv_filename = "simulation_results.csv"
    fieldnames = [
        "Seed", "Spawn_Strategy", "Algorithm", "Goal_X", "Goal_Y", 
        "Optimal_Tick", "Used_Tick", "Map_Coverage_%", 
        "Spawn_Fail_Count", "Backtrack_Count", "Total_Spawned", "Success"
    ]
    
    # CSV 파일 열기 및 헤더 작성
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"데이터 추출 시작... (총 {total_simulations * len(strategies)}회 실행)")
        
        for i in range(total_simulations):
            # 두 전략이 완벽히 동일한 환경(지형, 목표 위치)에서 대결할 수 있도록 시드를 고정
            current_seed = random.randint(100000, 999999)
            
            for strategy in strategies:
                random.seed(current_seed) # 시드 고정
                
                # 맵 생성 및 배치
                maze_env = Maze(n, num_initial_drones=strategy["count"])
                
                # 시뮬레이터 가동 (visualize=False로 화면 출력 없이 고속 연산)
                sim = Simulator(maze_env, max_drones=max_limit, 
                                seed_value=current_seed, 
                                strategy_name=strategy["name"])
                
                result_data = sim.run(visualize=False)
                
                # 결과 CSV에 행 추가
                writer.writerow(result_data)
                
            # 진행률 표시
            if (i + 1) % 10 == 0:
                print(f"진행 상황: {i + 1} / {total_simulations} 세트 완료")
                
    print(f"\n✅ 시뮬레이션 종료! 데이터가 '{csv_filename}'에 성공적으로 저장되었습니다.")