import heapq
import math
import time
from queue import Queue, PriorityQueue
import random

"""
Karim Elsayed ID.6023
Ahmed Saad ID.6060
Heba Elwazzan ID.6521
Youssef Nawar ID.6602
"""

# Answer tracker
goalState = 12345678
maxDepth = 0
nodesExpanded = 1
isFound = False
runTime = 0


# Game state class
class GameState:
    def __init__(self, parent, move, state, depth, cost=0):
        self.parent = parent
        self.move = move
        self.state = state
        self.depth = depth
        self.cost = cost + self.depth

    def __eq__(self, another):
        return self.state == another.state

    def __str__(self):
        stateStr = str(self.state)  # Convert Parent state from integer to string
        # if 0 is first element it will add it to the string
        stateStr = stateStr if len(stateStr) > 8 else "0" + "".join(stateStr)
        return stateStr

    def __hash__(self):
        return hash(self.__str__())

    def __lt__(self, other):
        return self.cost < other.cost


def __get__children(parent):
    """
    :param parent : Parent's node
    :return :Array of all parent's children
    """
    stateStr = parent.__str__()
    index = stateStr.index("0")  # get the index of the zero (Blank Space)
    row = int(index / 3)  # get  the row in which the blank space lies
    column = index % 3  # get  the column in which the blank space lies
    children = []
    if row == 0:
        # Move down only as first row elements can't go up the board
        children.append(GameState(parent, 'Down', __move__down(stateStr), parent.depth + 1))
    elif row == 1:
        # Move up and down
        children.append(GameState(parent, 'Down', __move__down(stateStr), parent.depth + 1))
        children.append(GameState(parent, 'Up', __move__up(stateStr), parent.depth + 1))
    else:
        # Move up only as first row elements can't down up the board
        children.append(GameState(parent, 'Up', __move__up(stateStr), parent.depth + 1))

    if column == 0:
        # Move right as as the element is at the far left
        children.append(GameState(parent, 'Right', __move__right(stateStr), parent.depth + 1))
    elif column == 1:
        # Move left and right
        children.append(GameState(parent, 'Left', __move__left(stateStr), parent.depth + 1))
        children.append(GameState(parent, 'Right', __move__right(stateStr), parent.depth + 1))
    else:
        # Move left as the element is at the far right
        children.append(GameState(parent, 'Left', __move__left(stateStr), parent.depth + 1))
    return children


def __move__down(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index + 3] = x[index + 3], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


def __move__up(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index - 3] = x[index - 3], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


def __move__right(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index + 1] = x[index + 1], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


def __move__left(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index - 1] = x[index - 1], x[index]
    temp = "".join(x)  # Converting the list back to string
    return int(temp)


# Heuristic function that calculate the manhattan distance and euclidean distance
# for a given state
def __heuristic__(state):
    manhattan_distance = 0
    euclid_distance = 0
    stateStr = str(state)
    stateStr = stateStr if len(stateStr) > 8 else "0" + "".join(stateStr)
    res = [int(x) for x in stateStr]
    for i in res:
        curr_row = res[i] // 3
        curr_column = res[i] % 3
        proj_row = i // 3
        proj_column = i % 3
        x = abs(curr_row - proj_row) + abs(curr_column - proj_column)
        manhattan_distance += x
        y = math.sqrt(((curr_row - proj_row) ** 2) + (curr_column - proj_column) ** 2)
        euclid_distance += y
    return manhattan_distance, euclid_distance


# Reset all global variables
def __reset__():
    global nodesExpanded, maxDepth, runTime, isFound
    maxDepth = 0
    nodesExpanded = 1
    isFound = False
    runTime = 0


# dfs
def __dfs__(root):
    start_time = time.time()
    global nodesExpanded, maxDepth, runTime, isFound
    __reset__()
    explored = set()
    frontier = [root]
    expanded = set()
    expanded.add(root)
    while frontier:
        node = frontier.pop()
        explored.add(node)
        if node.state == goalState:
            isFound = True
            end_time = time.time()
            runTime = end_time - start_time
            return node
        children = __get__children(node)
        children.reverse()
        for child in children:
            if child not in expanded:
                frontier.append(child)
                expanded.add(child)
                nodesExpanded += 1
                maxDepth = maxDepth if maxDepth > child.depth else child.depth
    isFound = False
    end_time = time.time()
    runTime = end_time - start_time
    return


# Breadth first search
def __bfs__(root):
    # start the timer
    start_time = time.time()
    # create a set for the explored and a queue containing the frontier states
    global nodesExpanded, maxDepth, isFound, runTime
    __reset__()
    explored = set()
    frontier = Queue()
    frontier.put(root)
    expanded = set()
    expanded.add(root)
    # iterate over frontier until goal is found or the tree is exhausted
    while not frontier.empty():
        node = frontier.get()
        explored.add(node)  # start exploring current state
        if node.state == goalState:
            isFound = True
            end_time = time.time()
            runTime = end_time - start_time
            return node  # if goal is found, exit and return state
        # else, start expanding by getting its children and enqueuing them
        children = __get__children(node)
        for child in children:
            if child not in expanded:
                frontier.put(child)
                expanded.add(child)
                nodesExpanded += 1
                maxDepth = maxDepth if maxDepth > child.depth else child.depth
    isFound = False
    end_time = time.time()
    runTime = end_time - start_time
    return


def print_data(answer, type_of_search):
    print(type_of_search + ":")
    if answer is not None:  # condition for unreachable goal state
        print(f"Cost of path: {answer.depth}")
        print(f"Nodes expanded: {nodesExpanded}")
        print(f"Search depth: {maxDepth}")
        print(f"Running time: {runTime}")

        status = "Cost of path: " + str(answer.depth) + "   Nodes expanded: " + str(
            nodesExpanded) + "   Search depth: " + str(maxDepth) + "   Running time: " + str(runTime)

        ## We don't need to print the path in console anymore
        # path_to_goal = iterative_get_path_(answer)
        # for game_state in path_to_goal:
        #     if game_state:
        #         if game_state.move:
        #             print(game_state.move)
        #         print(game_state)
    else:
        print("No solution exists!")
        print(f"Running time: {runTime}")
        print(f"Nodes expanded: {nodesExpanded}")
        print(f"Maximum depth: {maxDepth}")

        status = "No solution exists!   Running time: " + str(runTime) + \
                 "   Nodes expanded: " + str(nodesExpanded) + "  Maximum depth: " + str(maxDepth)

    return status


# recursive function to extract path from game state and its parents
# becomes obsolete if path is too large so we will use an iterative approach instead
# def get_path_to_goal(game_state):
#     path = []
#     path = _get_path(game_state, path)
#     path.reverse()
#     return path
#
#
# def _get_path(game_state, path):
#     try:
#         if game_state.move is not None:
#             path.append(game_state.move)
#             _get_path(game_state.parent, path)
#     except RecursionError:
#         print("Path is too large to display fully!")
#
#     return path


# saves iteratively the path into a list in order to display path in correct (non reversed) order
def iterative_get_path_(game_state):
    if game_state is not None:
        path = [game_state]
        i = 0
        while path[i].parent:
            path.append(path[i].parent)
            i += 1
        path.reverse()
        return path
    return False


# This functions creates a random game state by shuffling a list of 9 numbers: 0-8
# and returns an integer representing the state
def random_game_state():
    str_var = list("123456780")
    random.shuffle(str_var)
    state = int(''.join(str_var))
    return state


# A star algorithm
def __aStar__(root, type="manhattan"):
    start_time = time.time()
    global nodesExpanded, maxDepth, isFound, runTime
    __reset__()
    explored = set()
    frontier = PriorityQueue()
    frontier.put(root)
    expanded = dict()  # Frontier union Explored
    h, e = __heuristic__(root.state)
    cost = h if type == "manhattan" else e
    root.cost = cost
    expanded[root.state] = cost
    while not frontier.empty() and explored.__len__() != 181441:
        node = frontier.get()
        explored.add(node)
        if node.state == goalState:
            isFound = True
            end_time = time.time()
            runTime = end_time - start_time
            return node
        children = __get__children(node)
        for child in children:
            h, e = __heuristic__(child.state)
            cost = h if type == "manhattan" else e
            child.cost = cost + child.depth
            if child.state not in expanded:
                frontier.put(child)
                expanded[child.state] = child.cost
                nodesExpanded += 1
                maxDepth = maxDepth if maxDepth > child.depth else child.depth

            if ((child not in explored) and (child.state in expanded)) and expanded.get(
                    child.state) > child.cost:  # child is in frontier and has a cost more than current child
                frontier.put(child)
                expanded[child.state] = child.cost
    isFound = False
    end_time = time.time()
    runTime = end_time - start_time
    return


def solve(gameState, algorithm):
    answer = None
    if algorithm == 'BFS':
        answer = __bfs__(gameState)
    elif algorithm == 'DFS':
        answer = __dfs__(gameState)
    elif algorithm == 'A* Manhattan':
        answer = __aStar__(gameState)
    elif algorithm == 'A* Euclid':
        answer = __aStar__(gameState, 'Euclid')

    if isFound:
        return answer
    else:
        return None
