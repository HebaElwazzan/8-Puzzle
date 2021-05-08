import pygame
import pygame_gui

# local imports
import main as m

# width and height are not final and are subject to change as UI changes
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
TILE_AREA_WIDTH = 600
TILE_AREA_HEIGHT = 600
TILE_WIDTH = TILE_AREA_WIDTH / 3
TILE_HEIGHT = TILE_AREA_HEIGHT / 3
BUTTON_AREA_WIDTH = WINDOW_WIDTH - TILE_AREA_WIDTH
BUTTON_WIDTH = 240
BUTTON_HEIGHT = 80
BUTTON_MARGIN = (BUTTON_AREA_WIDTH - BUTTON_WIDTH) // 2

# colors
GREEN =         (  0, 204,   0)
BLUE =          (  0,   0, 204)
WHITE =         (255, 255, 255)
BLACK =         (  0,   0,   0)
DARKTURQUOISE = (  3,  54,  73)

BACKGROUND_COLOR = DARKTURQUOISE

BASICFONTSIZE = 60

APPLICATION_TITLE = "8-Puzzle"

# must initialize pygame as program start
# this is just something to be don
pygame.init()

# creating the fonts that will be used throughout the application
BASICFONT = pygame.font.Font('fonts/consola.ttf', BASICFONTSIZE)
BUTTON_FONT = pygame.font.Font('fonts/consola.ttf', BASICFONTSIZE // 2)

# at the start of every application you have to specify the width and height of the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# The UI manager handles calling the update, draw and event handling
# functions of all the UI elements we create and assign to it.
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# the title of the window that appears in title bar
pygame.display.set_caption(APPLICATION_TITLE)


# a simple class that contains Tile information
class Tile:

    def __init__(self, number, tile_width, tile_height, index_x, index_y):
        self.number = number
        self.x = 0
        self.y = 0
        self.width = tile_width
        self.height = tile_height
        self.index_x = index_x
        self.index_y = index_y

    # returns a tuple of 4 values for the purpose of drawing
    def tileStats(self):
        return self.x, self.y, self.width, self.height


# a rect object to store the information for Rects used to create buttons
# with pygame_gui
class ButtonRect:

    def __init__(self, id,):
        self.Rect = pygame.Rect(
            (WINDOW_WIDTH - BUTTON_AREA_WIDTH + BUTTON_MARGIN, id*BUTTON_HEIGHT + 10),     # left, top
            (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.id = id

# Initializes the board with a new random state.
def newRandomState():
    # some random test state
    # state = m.GameState(None, None, m.random_game_state(), 0)
    state = m.GameState(None, None, 123456870, 0)
    stateStr = str(state)

    # for now for the purpose of initialization, this list will contain some tiles to draw
    initial_tiles_list = []

    # the tile that will be left blank - represented by 0
    # initialized to silence warning
    blankTileLocal = Tile("0", TILE_WIDTH - 2, TILE_HEIGHT - 2, 0, 0)

    # num is a string
    for i, num in enumerate(stateStr):

        # I think I made a mistake, but this configuration works
        index_x = (i // 3)
        index_y = (i % 3)

        # We need a reference to the blank tile at all times for purpose of swapping
        # and drawing a blank rectangle
        if num != '0':
            # Margins are left around tiles to give the appearance of
            tile = Tile(num, TILE_WIDTH - 2, TILE_HEIGHT - 2, index_x, index_y)

            # The initial x and y coordinates of the tiles. Essentially,
            # I made 'reset' the x locations after every 3 tiles,
            # and for the y location to only increase after adding 3 tiles.
            # EXAMPLE: consider the test state 012345678, We we want 3rd Tile (2) to to appear on the upper right.
            # If initial x is 0, second x is 200, then 3rd x is 400
            # This is basically 0*x, 1*x, and 2*x respectively, and we want
            # this to repeat every 3 tiles, thus I used modulo
            # Same goes for y, only I want it to increase in every time 3 tiles
            # are inserted, thus I used integer division.
            tile.x = index_y * TILE_WIDTH + 1
            tile.y = index_x * TILE_HEIGHT + 1

            initial_tiles_list.append(tile)
        else:
            blankTileLocal.x = index_y * TILE_WIDTH + 1
            blankTileLocal.y = index_x * TILE_HEIGHT + 1
            blankTileLocal.index_x = index_x
            blankTileLocal.index_y = index_y
            initial_tiles_list.append(blankTileLocal)

    return state, initial_tiles_list, blankTileLocal


# swap blank tile and target tile
# direction the direction to which the blank tile moves
def updateBoard(direction):

    # saving the indices of blankTile for ease of use in calculating
    # index of tile in the tile list
    i, j = blankTile.index_x, blankTile.index_y

    # the tile required in list is different depending on swap direction
    if direction == 'Left':
        list_index = i*3 + (j - 1)
    elif direction == 'Up':
        list_index = (i - 1) * 3 + j
    elif direction == 'Down':
        list_index = (i + 1) * 3 + j
    elif direction == 'Right':
        list_index = i * 3 + (j + 1)

    target_tile = numbered_tiles_list[list_index]
    blankTile_list_index = i * 3 + j

    # swapping location on board and index. Need to know where the blank tile is
    # at all times
    target_tile.x, blankTile.x = blankTile.x, target_tile.x
    target_tile.y, blankTile.y = blankTile.y, target_tile.y
    target_tile.index_x, blankTile.index_x = blankTile.index_x, target_tile.index_x
    target_tile.index_y, blankTile.index_y = blankTile.index_y, target_tile.index_y

    # swap the blank tile and target tile in the tile list. Not doing so will mess
    # with later swaps as indices are no longer accurate
    numbered_tiles_list[list_index], numbered_tiles_list[blankTile_list_index] \
        = numbered_tiles_list[blankTile_list_index], numbered_tiles_list[list_index]


# This function checks the validity of a swap request, then calls updateBoard to do
# the actual swapping.
# To check if a swap is valid, the index of the clicked tile is first calculated,
# If the 'Distance' in terms of horizontal or vertical movement is exactly 1,
# this means it's a valid swap
def swapTiles(mousePosition):
    x, y = mousePosition
    index_y = x // TILE_WIDTH
    index_x = y // TILE_HEIGHT

    # distance between blank tile and target tile in terms of x and y axis
    distance = abs(blankTile.index_x - index_x) + abs(blankTile.index_y - index_y)

    # there is a valid swap move
    if distance == 1:
        if blankTile.index_y < index_y: # blank tile will move right
            updateBoard("Right")
        elif blankTile.index_y > index_y: # blank tile will move left
            updateBoard("Left")
        elif blankTile.index_x < index_x:
            updateBoard("Down")
        elif blankTile.index_x > index_x:
            updateBoard("Up")


# clicking this button generates a random board state.
randomStateButtonRect = ButtonRect(0)
randomStateButton = pygame_gui.elements.UIButton(
    relative_rect=randomStateButtonRect.Rect, text="Random Start", manager=manager
)

# Clicking this button should go through the steps required to solve the puzzle
solveButtonRect = ButtonRect(1)
solveButton = pygame_gui.elements.UIButton(
    relative_rect=solveButtonRect.Rect, text="Solve", manager=manager
)

initialState, numbered_tiles_list, blankTile = newRandomState()

# m.display_results(m.GameState(None, None, 102345678, 0))
# m.display_results(initialState)


clock = pygame.time.Clock()
running = True
while running:

    # fixing the frame rate to 60 fps
    time_delta = clock.tick(60) / 1000.0

    # a game loop consists of 2 main phases: update phase, and draw phase
    # in update phase we perform all modifications, then in draw phase we
    # show the effect of those modifications.
    # Hence, responding to events happens in update phase, in which we will do
    # things like restarting board, solving a problem, and so on.

    # check the event queue for events, such as quit or click
    # I noticed while learning pygame that if the program doesn't process the event queue,
    # the OS considers the app frozen and it crashes
    events = pygame.event.get()

    # Check all events in even queue
    for event in events:

        # specific to the UI library. all events related to pygame_gui go here
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == randomStateButton:
                    initialState, numbered_tiles_list, blankTile = newRandomState()
                elif event.ui_element == solveButton:
                    m.display_results(initialState)

        # Checking for a mouseclick on a tile
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check If the position of mouse click is whithin border of Tile Area
            # No need to do any swapping otherwise
            if x < TILE_AREA_WIDTH and y < TILE_AREA_HEIGHT:
                swapTiles(event.pos)

        if event.type == pygame.QUIT:
            running = False
            break

        manager.process_events(event)

    # specific to pygame_gui, must be called every loop to update UI
    manager.update(time_delta)

    # fill the screen with the background color before drawing anything else
    window.fill(BACKGROUND_COLOR)

    # Draw rectangles representing the tiles of the 8-puzzle except blank
    for tile in numbered_tiles_list:
        pygame.draw.rect(window, GREEN, tile.tileStats())

        # display the tile number on the tile as text
        textSurf = BASICFONT.render(tile.number, True, WHITE, GREEN)
        textRect = textSurf.get_rect()
        textRect.center = tile.x + TILE_WIDTH // 2, tile.y + TILE_HEIGHT // 2
        window.blit(textSurf, textRect)

    # the blank tile is drawn as a black rectangle
    pygame.draw.rect(window, BACKGROUND_COLOR, blankTile.tileStats())

    # called every loop to update visuals
    manager.draw_ui(window)
    pygame.display.update()

# quit application if somehow loop is escaped
pygame.quit()