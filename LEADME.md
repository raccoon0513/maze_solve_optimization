## 연구 배경
본 연구는 steam에서 판매 중인 게임 "**농부는 대체되었다**<sub>The Farmer Was Replaced</sub>"에 등장하는 미로 탐색 문제를 효율적으로 풀기 위해 상향식/하향식 접근을 통한 알고리즘 최적화<sub>optimization</sub>에 목적을 둔다.

## 연구 방법
1. 미로 생성
    1.엘러의 알고리즘<sub>Eller's Algorithm</sub>을 사용한 $n \times n$ 미로를 생성을 시도하였으나, 벽으로 이루어진 방(2x2 이상)이 생성되었음을 확인함
    1. 재귀적 생성 알고리즘으로 변환
        1. 시간 복잡도 $O(N)$에서 $O(N\log{N})$으로 격상
    1. 수정후 미로 중 벽으로 이루어진 방이 생성되지 않음을 확인
    1. 클래스화하여 0과 1로 이루어진 이중 배열로 리턴
        1. 0은 벽<sub>wall</sub>
        1. 1은 길<sub>path</sub>
        1. 2는 플레이어<sub>PP : Player</sub>
        1. 3은 목적지<sub>GG : Goal</sub>
2.

## 연구 결과


