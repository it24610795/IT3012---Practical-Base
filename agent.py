# agent.py
import random
from collections import deque
import heapq


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """A Simple Reflex Agent that reacts purely to immediate local percepts using Condition-Action rules."""

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here') or percept.get('smells_food'):
            return 'suck'
        elif percept.get('wall_here') or percept.get('hit_wall') or percept.get('wall_ahead'):
            return random.choice(['Up', 'Down', 'Left', 'Right'])
        elif percept.get('trap_here') or percept.get('smells_toxin'):
            return random.choice(['Up', 'Down', 'Left', 'Right'])
        else:
            return 'Up'


class ModelBasedAgent:
    """A Model-Based Agent that maintains internal memory state to avoid infinite loops."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.last_action = None
        self.visited_cells = set()

    def sense_and_act(self, percept: dict) -> str:
        if self.last_action == 'Up':
            self.y += 1
        elif self.last_action == 'Down':
            self.y -= 1
        elif self.last_action == 'Left':
            self.x -= 1
        elif self.last_action == 'Right':
            self.x += 1

        self.visited_cells.add((self.x, self.y))

        if percept.get('food_here') or percept.get('smells_food'):
            action = 'Stay'
        else:
            candidates = {
                'Up': (self.x, self.y + 1),
                'Down': (self.x, self.y - 1),
                'Left': (self.x - 1, self.y),
                'Right': (self.x + 1, self.y)
            }

            if percept.get('wall_here') or percept.get('hit_wall') or percept.get('wall_ahead'):
                if self.last_action in candidates:
                    del candidates[self.last_action]

            unvisited_actions = [a for a, pos in candidates.items() if pos not in self.visited_cells]

            if unvisited_actions:
                action = random.choice(unvisited_actions)
            elif candidates:
                action = random.choice(list(candidates.keys()))
            else:
                action = random.choice(['Up', 'Down', 'Left', 'Right'])

        self.last_action = action
        return action


class SearchAgent:
    """
    Goal-Based / Planning Agent for Practical 03 implementing
    Breadth-First Search (BFS), Depth-First Search (DFS), and Uniform-Cost Search (UCS).
    """

    def __init__(self):
        self.plan = []
        # Switch between 'BFS', 'DFS', and 'UCS' to evaluate path execution
        self.active_algo = 'BFS'

    def bfs_search(self, start_pos, goal_pos, walls, grid_size) -> list:
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        queue = deque([(start, [])])
        visited = {start}

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            x, y = current
            moves = [
                ('Up', (x, y + 1)),
                ('Down', (x, y - 1)),
                ('Left', (x - 1, y)),
                ('Right', (x + 1, y))
            ]

            for action, next_pos in moves:
                nx, ny = next_pos
                if 0 <= nx < width and 0 <= ny < height and next_pos not in walls_set:
                    if next_pos not in visited:
                        visited.add(next_pos)
                        queue.append((next_pos, path + [action]))

        return []

    def dfs_search(self, start_pos, goal_pos, walls, grid_size) -> list:
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        stack = [(start, [])]
        visited = {start}

        while stack:
            current, path = stack.pop()

            if current == goal:
                return path

            x, y = current
            moves = [
                ('Up', (x, y + 1)),
                ('Down', (x, y - 1)),
                ('Left', (x - 1, y)),
                ('Right', (x + 1, y))
            ]

            for action, next_pos in moves:
                nx, ny = next_pos
                if 0 <= nx < width and 0 <= ny < height and next_pos not in walls_set:
                    if next_pos not in visited:
                        visited.add(next_pos)
                        stack.append((next_pos, path + [action]))

        return []

    def ucs_search(self, start_pos, goal_pos, walls, grid_size) -> list:
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        width, height = grid_size

        counter = 0
        pq = [(0, counter, start, [])]
        visited = set()

        while pq:
            cost, _, current, path = heapq.heappop(pq)

            if current == goal:
                return path

            if current not in visited:
                visited.add(current)
                x, y = current
                moves = [
                    ('Up', (x, y + 1)),
                    ('Down', (x, y - 1)),
                    ('Left', (x - 1, y)),
                    ('Right', (x + 1, y))
                ]

                for action, next_pos in moves:
                    nx, ny = next_pos
                    if 0 <= nx < width and 0 <= ny < height and next_pos not in walls_set:
                        if next_pos not in visited:
                            counter += 1
                            heapq.heappush(pq, (cost + 1, counter, next_pos, path + [action]))

        return []

    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:
            agent_pos = tuple(percept.get('agent_pos', [0, 0]))
            all_food = percept.get('all_food', [])
            walls = percept.get('walls', [])
            grid_size = percept.get('grid_size', (10, 10))

            if not all_food:
                return 'Stay'

            # Target the closest food pellet by Manhattan distance
            closest_food = min(
                all_food,
                key=lambda f: abs(f[0] - agent_pos[0]) + abs(f[1] - agent_pos[1])
            )

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(agent_pos, closest_food, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(agent_pos, closest_food, walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(agent_pos, closest_food, walls, grid_size)

        if self.plan:
            return self.plan.pop(0)
        return 'Stay'