import math

# Answer tracker
goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
depth = 0
nodesVisited = 0
nodesExpanded = 0


# Game state class
class GameState:
    def __init__(self, parent, move, state):
        self.parent = parent
        self.move = move
        self.state = state


def __get__children(parent):
    index = parent.state.index(0)
    row = int(index / 3)
    column = index % 3
    children = []
    if row == 0:
        # Move down
        children.append(GameState(parent, 'Down', __move__down(parent.state)))
    elif row == 1:
        # Move up and down
        children.append(GameState(parent, 'Down', __move__down(parent.state)))
        children.append(GameState(parent, 'Up', __move__up(parent.state)))
    else:
        # Move up
        children.append(GameState(parent, 'Up', __move__up(parent.state)))
    if column == 0:
        # Move right
        children.append(GameState(parent, 'Right', __move__right(parent.state)))
    elif column == 1:
        # Move left and right
        children.append(GameState(parent, 'left', __move__left(parent.state)))
        children.append(GameState(parent, 'right', __move__right(parent.state)))
    else:
        # Move left
        children.append(GameState(parent, 'Left', __move__left(parent.state)))
    return children


def __move__down(state):
    index = state.index(0)
    temp = state.copy()
    temp[index], temp[index + 3] = temp[index + 3], temp[index]
    return temp


def __move__up(state):
    index = state.index(0)
    temp = state.copy()
    temp[index], temp[index - 3] = temp[index - 3], temp[index]
    return temp


def __move__right(state):
    index = state.index(0)
    temp = state.copy()
    temp[index], temp[index + 1] = temp[index + 1], temp[index]
    return temp


def __move__left(state):
    index = state.index(0)
    temp = state.copy()
    temp[index], temp[index - 1] = temp[index - 1], temp[index]
    return temp


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


