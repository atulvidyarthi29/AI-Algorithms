from pprint import pprint
import sys


class RouteFinding:

    def __init__(self, filename):
        self.adjlist = self.readFile(filename)
        self.heuristics = self.read_heuristics()

        self.initial = input('Enter Source:')
        while self.initial not in self.adjlist:
            self.initial = input('City does not Exist.Enter Source Again:')

        self.goal = input('Enter Destination:')
        while self.goal not in self.adjlist:
            self.goal = input('City does not Exist.Enter Destination Again:')

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

    def readFile(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        adjlist = {}
        for line in lines:
            listelement = line[:-1].split(',')
            try:
                adjlist[listelement[0]].append(
                    (listelement[1], int(listelement[2])))
            except:
                adjlist[listelement[0]] = [
                    (listelement[1], int(listelement[2]))]
            try:
                adjlist[listelement[1]].append(
                    (listelement[0], int(listelement[2])))
            except:
                adjlist[listelement[1]] = [
                    (listelement[0], int(listelement[2]))]
        pprint(adjlist)
        return adjlist

    def read_heuristics(self):
        f = open('Bangalore_distance.csv', 'r', encoding='utf-8')
        lines = f.readlines()
        heuristics = {}
        for line in lines:
            list_element = line[:-1].split(',')
            # print(list_element[0],list_element[2])
            heuristics[list_element[0]] = float(list_element[2])
        return heuristics

    def goal_test(self, state):
        if state == self.goal:
            return 1
        return 0

    def goal_test_heuristic(self, state):
        if state == 'Bangalore':
            return 1
        return 0

    def bfs(self):
        explored = set()
        frontier = []
        path = []
        frontier.append(self.initial)
        while True:
            if len(frontier) == 0:
                return None
            node = frontier[0]
            if node not in explored:
                path += [node]
                explored.add(node)
            for city in self.adjlist[node]:
                if (city[0] not in explored) or (city[0] not in frontier):
                    if self.goal_test(city[0]):
                        path += [self.goal]
                        print(path)
                        return path
                    if city[0] not in frontier:
                        frontier.append(city[0])
            del frontier[0]

    def dfs(self):
        explored = set()
        frontier = []   # stack
        path = []
        state = self.initial
        frontier.append(state)
        while True:
            if len(frontier) == 0:
                return None
            node = frontier[-1]
            if node not in explored:
                path += [node]
            explored.add(node)
            for city in self.adjlist[node]:
                if (city[0] not in explored) or (city[0] not in frontier):
                    if self.goal_test(city[0]):
                        path += [self.goal]
                        print(path)
                        return path
                    if city[0] not in frontier:
                        frontier.append(city[0])
            del frontier[-1]


    def gbfs(self):
        state = self.initial
        path = [state]
        totaldistance = 0
        while self.goal_test_heuristic(state) != 1:
            minimum = sys.maxsize
            mincity = ''
            for city in self.adjlist[state]:
                print(city[0], self.heuristics[city[0]])
                if self.heuristics[city[0]] <= minimum:
                    minimum = self.heuristics[city[0]]
                    mincity = city
            state = mincity[0]
            totaldistance = mincity[1]
            path.append(state)
        print(path)
        return path

    def a_star(self):
        state = self.initial
        path = [state]
        totaldistance = 0
        while self.goal_test_heuristic(state) != 1:
            minimum = sys.maxsize
            mincity = ''
            for city in self.adjlist[state]:
                if self.heuristics[city[0]] + city[1] <= minimum:
                    minimum = self.heuristics[city[0]] + city[1]
                    mincity = city[0]
                    mindist = city[1]
            state = mincity
            totaldistance += mindist
            path.append(state)
        print(path)
        print("Total Distance=", totaldistance)
        return path


RouteFinding('NS_Dataset_1.csv',)
