import pygame

# local imports
import main as m



# width and height are not final and are subject to change as UI changes
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TILE_WIDTH = WINDOW_WIDTH / 3
TILE_HEIGHT = WINDOW_HEIGHT / 3

# colors
GREEN =         (  0, 204,   0)
WHITE =         (255, 255, 255)
BLACK =         (  0,   0,   0)
DARKTURQUOISE = (  3,  54,  73)

BASICFONTSIZE = 60

APPLICATION_TITLE = "8-Puzzle"

# must initialize pygame as program start
# this is just something to be don
pygame.init()

BASICFONT = pygame.font.Font('fonts/consola.ttf', BASICFONTSIZE)

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


def drawText(text, color, bgcolor, top, left):

    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return textSurf, textRect


# some random test state
testState = m.GameState(None, None, 865023147, 0)
stateStr = str(testState)

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

        # The initial x and y coordinates of the tiles. Essentially, I made 'reset' the x locations after every 3 tiles,
        # and for the y location to only increase after adding 3 tiles.
        # EXAMPLE: consider the test state 012345678, We we want 3rd Tile (2) to to appear on the upper right.
        # If initial x is 0, second x is 200, then 3rd x is 400
        # This is basically 0*x, 1*x, and 2*x respectively, and we want this to repeat every 3 tiles, thus I used modulo
        # Same goes for y, only I want it to increase in every time 3 tiles are inserted, thus I used integer division.
        tile.x = (i % 3) * TILE_WIDTH + 1
        tile.y = (i // 3) * TILE_HEIGHT + 1

        numbered_tiles_list.append(tile)
    else:
        blankTile.x = (i % 3) * TILE_WIDTH + 1
        blankTile.y = (i // 3) * TILE_HEIGHT + 1

running = True
while running:

    # check the event queue for events, such as quit or click
    # I noticed while learning pygame that if the program doesn't process the event queue,
    # the OS considers the app frozen and it crashes
    events = pygame.event.get()

    # Draw rectangles representing the tiles of the 8-puzzle except blank
    for tile in numbered_tiles_list:
        pygame.draw.rect(window, GREEN, tile.tileStats())

        # display the tile number on the tile as text
        textSurf = BASICFONT.render(tile.number, True, WHITE, GREEN)
        textRect = textSurf.get_rect()
        textRect.center = tile.x + TILE_WIDTH // 2, tile.y + TILE_HEIGHT // 2
        window.blit(textSurf, textRect)

    # the blank tile is drawn as a black rectangle
    pygame.draw.rect(window, BLACK, blankTile.tileStats())

    # called every loop to update visuals
    pygame.display.update()

    # Check if game quit
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break

