from utils import DIRECTIONS, get_opposite, manhattan_distance

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
                env.backtrack_count += 1 
            return

        came_from = self.memory.get('came_from')
        open_dirs = []
        for d in DIRECTIONS:
            if d != came_from and env.can_move(self.x, self.y, d):
                open_dirs.append(d)

        if len(open_dirs) == 0:
            if len(self.memory['missed_branches']) > 0:
                self.memory['is_backtracking'] = True
                back_dir = self.memory['backtrack_path'].pop()
                env.move(self, back_dir)
                env.backtrack_count += 1
            else:
                self.active = False
            return

        gx, gy = env.goal_location
        # 더 이상 *2를 하지 않고 바로 인접 칸으로 계산
        open_dirs.sort(key=lambda d: manhattan_distance(self.x + d[0], self.y + d[1], gx, gy))

        for d in open_dirs[1:]:
            new_x = self.x + d[0]
            new_y = self.y + d[1]
            
            new_memory = {
                'came_from': get_opposite(d),
                'backtrack_path': [get_opposite(d)], 
                'missed_branches': [],
                'is_backtracking': False
            }
            
            success = env.spawn_drone(new_x, new_y, new_memory)
            if not success:
                self.memory['missed_branches'].append((self.x, self.y, d))

        self._move_forward(env, open_dirs[0])

    def _move_forward(self, env, d):
        env.move(self, d)
        self.memory['came_from'] = get_opposite(d)
        self.memory['backtrack_path'].append(get_opposite(d))