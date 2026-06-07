import sys
from maze import Maze
from simulator import Simulator

# 미로 생성 시 재귀 깊이 제한 해제
sys.setrecursionlimit(10000)

if __name__ == "__main__":
    # --- [실험 변수 통제 구역] ---
    n = 15                 # 미로 크기 ($n \times n$)
    max_limit = 32         # 최대 동시 유지 제한 에이전트 수 ($n$)
    initial_drone_count = 4 # 초기 사전 배치 전략용 드론 수
    # -----------------------------
    
    # 1. 맵 생성
    maze_env = Maze(n, num_initial_drones=initial_drone_count)
    
    # 2. 시뮬레이터 객체 초기화
    sim = Simulator(maze_env, max_drones=max_limit)
    
    # 3. 시뮬레이션 가동
    # visualize=False로 변경 시 렌더링 과정을 생략하여 초고속 연산 가능 (데이터 수집용)
    sim.run(visualize=True)