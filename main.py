goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
depth = 0
nodesVisited = 0
nodesExpanded = 0


class GameState:
    def __init__(self, parent, move):
        self.parent = parent
        self.move = move
        
