# agent.py
import random

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)
    

class SimpleReflexAgent:
    """A Simple Reflex Agent that reacts purely to immediate local percepts using Condition-Action rules."""

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here') or percept.get('smells_food'):
            return 'suck'   #eat food
        elif percept.get('wall_here') or percept.get('hit_wall'):
            return random.choice(['Up','Down','Left','Right'])  #avoid wall
        elif percept.get('trap_here') or percept.get('smells_toxin'):
            return random.choice(['Up','Down','Left','Right'])  #avoid trap
        else:
            return 'Up' #default move


class ModelBasedAgent:
    """A Model-Based Agent that maintains internal memory state to avoid infinite loops."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.last_action  = None
        self.visited_cells = set ()

    def sense_and_act(self, percept:dict) -> str:
        if self.last_action == 'Up':
            self.y +=1
        elif self.last_action == "Down":
            self.y -=1
        elif self.last_action == 'Left':
            self.x -=1
        elif self.last_action == 'Right':
            self.x +=1
        
        self.visited_cells.add((self.x,self.y))

        if percept.get('food_here') or percept.get('smells_food'):
            action = 'Stay'
        
        else:
            candidates ={
                'Up': (self.x,self.y+1),
                'Down': (self.x,self.y-1),
                'Left': (self.x-1,self.y),
                'Right': (self.x+1,self.y)
                }
        
            if percept.get('wall_here') or percept.get('hit_wall') or percept.get('wall_ahead'):
                if self.last_action in candidates:
                    del candidates[self.last_action]
        
            unvisited_actions = [a for a,pos in candidates.items() if pos not in self.visited_cells]

            if unvisited_actions:
                action = random.choice(unvisited_actions)
            elif candidates:
                action = random.choice(list(candidates.keys()))
            else:
                action = random.choice(['Up','Down','Left','Right'])
        self.last_action = action
        return action


