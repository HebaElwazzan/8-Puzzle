import pygame
import sys

import main as m

# various constants that will be used throughout the application.

# width and height are not final and are subject to change as UI changes
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

APPLICATION_TITLE = "8-Puzzle"

# must initialize pygame as program start
# this is just something to be don
pygame.init()

# at the start of every application you have to specify the width and height of the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# the title of the window that appears in title bar
pygame.display.set_caption(APPLICATION_TITLE)

running = True
while running:

    # check the event queue for events, such as quit or click
    # I noticed while learning pygame that if the program doesn't process the event queue,
    # the OS considers the app frozen and it crashes
    events = pygame.event.get()

    # Check if game quit
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
