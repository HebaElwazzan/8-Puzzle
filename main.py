import math

# Answer tracker
goalState = 12345678
maxDepth = 0
nodesVisited = 0
nodesExpanded = 1
isFound = False


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
    """
    :param parent : Parent's node
    :return :Array of all parent's children
    """
    stateStr = str(parent.state)  # Convert Parent state from integer to string
    stateStr = stateStr if len(stateStr) > 8 else "0" + "".join(stateStr)  # if 0 is first element it will add it to
    # th string
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
    temp = "".join(x)   # Converting the list back to string
    return int(temp)


def __move__right(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index + 1] = x[index + 1], x[index]
    temp = "".join(x)   # Converting the list back to string
    return int(temp)


def __move__left(state):
    index = state.index('0')  # get the index of the zero (Blank Space)
    temp = state
    x = list(temp)  # Converting String to list for easier swap
    x[index], x[index - 1] = x[index - 1], x[index]
    temp = "".join(x)   # Converting the list back to string
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
    global nodesExpanded, nodesVisited, maxDepth, isFound
    explored = set()
    frontier = [root]
    while frontier:
        node = frontier.pop()
        explored.add(node)
        if node.state == goalState:
            isFound = True
            return node
        children = __get__children(node)
        children.reverse()
        for child in children:
            if child not in explored:
                frontier.append(child)
                explored.add(child)
                nodesExpanded += 1
                maxDepth = maxDepth if maxDepth > child.depth else child.depth
    isFound = False
    return


answer = __dfs__(GameState(0, "Up", 312045678, 0))
print(nodesExpanded)
print(maxDepth)
print(answer.depth)
