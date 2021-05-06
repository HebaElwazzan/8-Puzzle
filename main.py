import math

# Answer tracker
goalState = 12345678
maxDepth = 0
nodesVisited = 0
nodesExpanded = 1


# Game state class
class GameState:
    def __init__(self, parent, move, state, depth):
        self.parent = parent
        self.move = move
        self.state = state
        self.depth = depth

    def __eq__(self, another):
        return self.state == another.state

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.__str__())


def __get__children(parent):
    stateStr = str(parent.state)
    stateStr = stateStr if len(stateStr) > 8 else "0" + "".join(stateStr)
    index = stateStr.index("0")
    row = int(index / 3)
    column = index % 3
    children = []
    if row == 0:
        # Move down
        children.append(GameState(parent, 'Down', __move__down(stateStr), parent.depth + 1))
    elif row == 1:
        # Move up and down
        children.append(GameState(parent, 'Down', __move__down(stateStr), parent.depth + 1))
        children.append(GameState(parent, 'Up', __move__up(stateStr), parent.depth + 1))
    else:
        # Move up
        children.append(GameState(parent, 'Up', __move__up(stateStr), parent.depth + 1))

    if column == 0:
        # Move right
        children.append(GameState(parent, 'Right', __move__right(stateStr), parent.depth + 1))
    elif column == 1:
        # Move left and right
        children.append(GameState(parent, 'left', __move__left(stateStr), parent.depth + 1))
        children.append(GameState(parent, 'right', __move__right(stateStr), parent.depth + 1))
    else:
        # Move left
        children.append(GameState(parent, 'Left', __move__left(stateStr), parent.depth + 1))
    return children


def __move__down(state):
    index = state.index('0')
    temp = state
    x = list(temp)
    x[index], x[index + 3] = x[index + 3], x[index]
    temp = "".join(x)
    return int(temp)


def __move__up(state):
    index = state.index('0')
    temp = state
    x = list(temp)
    x[index], x[index - 3] = x[index - 3], x[index]
    temp = "".join(x)
    return int(temp)


def __move__right(state):
    index = state.index('0')
    temp = state
    x = list(temp)
    x[index], x[index + 1] = x[index + 1], x[index]
    temp = "".join(x)
    return int(temp)


def __move__left(state):
    index = state.index('0')
    temp = state
    x = list(temp)
    x[index], x[index - 1] = x[index - 1], x[index]
    temp = "".join(x)
    return int(temp)


# Heuristic function
def __heuristic__(state):
    manhattan_distance = 0
    euclid_distance = 0
    for i in state:
        curr_row = int(state[i] / 3)
        curr_column = state[i] % 3
        proj_row = int(i / 3)
        proj_column = i % 3
        x = abs(curr_row - proj_row) + abs(curr_column - proj_column)
        manhattan_distance += x
        y = math.sqrt(((curr_row - proj_row) ** 2) + (curr_column - proj_column) ** 2)
        euclid_distance += y
    return manhattan_distance, euclid_distance


# dfs
def __dfs__(root):
    global nodesExpanded
    explored = set()
    frontier = [root]
    while frontier:
        node = frontier.pop()
        explored.add(node)
        if node.state == goalState:
            return node
        children = reversed(__get__children(node))
        for child in children:
            if child not in explored:
                frontier.append(child)
                explored.add(child)
                nodesExpanded += 1
    return


answer = __dfs__(GameState(0, "Up", 123456078, 0))
print(answer.depth)
print(nodesExpanded)

