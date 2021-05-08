import pygame

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
BUTTON_HEIGHT = 140
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

BASICFONT = pygame.font.Font('fonts/consola.ttf', BASICFONTSIZE)
BUTTON_FONT = pygame.font.Font('fonts/consola.ttf', BASICFONTSIZE // 2)

# at the start of every application you have to specify the width and height of the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# the title of the window that appears in title bar
pygame.display.set_caption(APPLICATION_TITLE)


class Tile:

    def __init__(self, number, tile_width, tile_height):
        self.number = number
        self.x = 0
        self.y = 0
        self.width = tile_width
        self.height = tile_height

    # returns a tuple of 4 values for the purpose of drawing
    def tileStats(self):
        return self.x, self.y, self.width, self.height


class Button:

    def __init__(self, id, bgColor, text):
        self.Rect = pygame.Rect(
            (WINDOW_WIDTH - BUTTON_AREA_WIDTH + BUTTON_MARGIN, id*BUTTON_HEIGHT + 10),     # left, top
            (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.id = id
        self.bgColor = bgColor
        self.text = text

    def drawButton(self, window):
        pygame.draw.rect(window, self.bgColor, self.Rect)
        textSurf = BUTTON_FONT  .render(self.text, True, WHITE, None)
        textRect = textSurf.get_rect()
        textRect.center = self.Rect.x + self.Rect.width // 2, self.Rect.y + self.Rect.height // 2
        window.blit(textSurf, textRect)


def newRandomState():
    # some random test state
    state = m.GameState(None, None, m.__random_game_state(), 0)
    stateStr = str(state)

    # for now for the purpose of initialization, this list will contain some tiles to draw
    numbered_tiles_list = []

    # the tile that will be left blank - represented by 0
    # initialized to silence warning
    blankTile = Tile("0", TILE_WIDTH - 2, TILE_HEIGHT - 2)

    # num is a string
    for i, num in enumerate(stateStr):

        # The tile containing zero should be left as blank!
        if num != '0':
            # Margins are left around tiles to give the appearance of
            tile = Tile(num, TILE_WIDTH - 2, TILE_HEIGHT - 2)

            # The initial x and y coordinates of the tiles. Essentially,
            # I made 'reset' the x locations after every 3 tiles,
            # and for the y location to only increase after adding 3 tiles.
            # EXAMPLE: consider the test state 012345678, We we want 3rd Tile (2) to to appear on the upper right.
            # If initial x is 0, second x is 200, then 3rd x is 400
            # This is basically 0*x, 1*x, and 2*x respectively, and we want
            # this to repeat every 3 tiles, thus I used modulo
            # Same goes for y, only I want it to increase in every time 3 tiles
            # are inserted, thus I used integer division.
            tile.x = (i % 3) * TILE_WIDTH + 1
            tile.y = (i // 3) * TILE_HEIGHT + 1

            numbered_tiles_list.append(tile)
        else:
            blankTile.x = (i % 3) * TILE_WIDTH + 1
            blankTile.y = (i // 3) * TILE_HEIGHT + 1

    return state, numbered_tiles_list, blankTile

def drawText(text, color, bgcolor, top, left):

    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return textSurf, textRect


randomStateButton = Button(0, BLUE, "Random Start")

initialState, numbered_tiles_list, blankTile = newRandomState()

running = True
while running:

    # a game loop consists of 2 main phases: update phase, and draw phase
    # in update phase we perform all modifications, then in draw phase we
    # show the effect of those modifications.
    # Hence, responding to events happens in update phase, in which we will do
    # things like restarting board, solving a problem, and so on.

    # check the event queue for events, such as quit or click
    # I noticed while learning pygame that if the program doesn't process the event queue,
    # the OS considers the app frozen and it crashes
    events = pygame.event.get()

    # Check if game quit
    for event in events:

        # when a mouse button is clicked, record its position for
        # for the purpose of checking collision
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = event.pos
            if randomStateButton.Rect.collidepoint(mousePos):
                initialState, numbered_tiles_list, blankTile = newRandomState()

        if event.type == pygame.QUIT:
            running = False
            break

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

    # draw all the buttons
    randomStateButton.drawButton(window)

    # called every loop to update visuals
    pygame.display.update()


