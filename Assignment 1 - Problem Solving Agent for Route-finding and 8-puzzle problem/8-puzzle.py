import copy
import sys


class Node:
    def __init__(self,state, action):
        self.state = state
        if action == None:
           self.action = ''   #the move that changed the state to this
        else:
            self.action = action 

class Puzzle:

    def __init__(self, state):
        self.state = state
        self.tile = state.index('*')

    def move(self, action):
        newstate = copy.deepcopy(list(self.state))
        state = copy.deepcopy(self.state)
        row = int(self.tile/3)
        col = self.tile % 3
        if action == 'up':
            if row == 0:
                return state
            newtile = (row-1) * 3 + col
        elif action == 'down':
            if row == 2:
                return state
            newtile = (row+1) * 3 + col
        elif action == 'right':
            if col == 2:
                return state
            newtile = self.tile + 1
        elif action == 'left':
            if col == 0:
                return state
            newtile = self.tile - 1
        newstate[self.tile], newstate[newtile] = newstate[newtile], newstate[self.tile]
        string = ''
        for i in newstate:
            string += i
        return string


class PuzzleSol:
    def __init__(self):
        print("* represents the blank tile.")
        self.initial = input('Enter Initial State:')
        self.goal = input('Enter Goal State:')
        search_type = int(
            input('1. BFS\n2. DFS\n3. GBFS\n4. A-star\nYout Choice: '))
        if search_type == 1:
            self.bfs()
        elif search_type == 2:
            self.dfs()
        elif search_type == 3:
            self.gbfs()
        elif search_type == 4:
            self.a_star()

    def goal_test(self, state):
        if state == self.goal:
            return 1
        return 0

    def bfs(self):
        explored = set()
        frontier = []
        frontier.append(self.initial)
        while True:
            if len(frontier) == 0:
                return None
            node = frontier[0]
            if node not in explored:
                explored.add(node)
            for action in ['up', 'down', 'right', 'left']:
                childnode = Puzzle(node).move(action)
                if (childnode not in explored) or (childnode not in frontier):
                    if self.goal_test(childnode) == 1:
                        print("Goalstate-", childnode)
                        return childnode
                    if childnode not in frontier:
                        frontier.append(childnode)
            del frontier[0]

    def dfs(self):
        explored = set()
        frontier = []   # stack
        state = self.initial
        frontier.append(state)
        while True:
            if len(frontier) == 0:
                return None
            node = frontier[-1]
            explored.add(node)
            for action in ['up', 'down', 'right', 'left']:
                childnode = Puzzle(node).move(action)
                if (childnode not in explored) or (childnode not in frontier):
                    if self.goal_test(childnode) == 1:
                        print(childnode)
                        return childnode
                    if childnode not in frontier:
                        frontier.append(childnode)
            del frontier[-1]

    def heuristics(self, state):
        count = 0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                count += 1
        return count

    def gbfs(self):
        state = self.initial
        totaldistance = 0
        actions = []
        while self.goal_test(state) != 1:
            minimum = sys.maxsize
            act = ''
            nextstate = ''
            for action in ['up', 'down', 'right', 'left']:
                childstate = Puzzle(state).move(action)
                if self.heuristics(childstate) <= minimum:
                    minimum = self.heuristics(childstate)
                    nextstate = childstate
                    act = action
            state = nextstate
            actions += [act]
            totaldistance += 1
        print("Action sequence: ", actions)
        print("No. of movements required: ", totaldistance)
        return actions

    def a_star(self):
        state = self.initial
        totaldistance = 0
        actions = []
        while self.goal_test(state) != 1:
            minimum = sys.maxsize
            act = ''
            nextstate = ''
            for action in ['up', 'down', 'right', 'left']:
                childstate = Puzzle(state).move(action)
                if self.heuristics(childstate) + (totaldistance+1) <= minimum:
                    minimum = self.heuristics(childstate) + (totaldistance+1)
                    nextstate = childstate
                    act = action
            state = nextstate
            actions += [act]
            totaldistance += 1
        print("Action sequence: ", actions)
        print("No. of movements required: ", totaldistance)
        return actions


PuzzleSol()
