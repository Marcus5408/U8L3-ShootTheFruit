import pygame
import random
import time
from apple import Apple


# set up pygame modules
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 15)
pygame.display.set_caption("Shoot the Fruit!")


# set up variables for the display
SCREEN_HEIGHT = 370
SCREEN_WIDTH = 530
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)




r = 50
g = 0
b = 100


# render the text for later
message = "Click the fruit to score!"
display_message = my_font.render(message, True, (255, 255, 255))




# Instantiate the apple
a = Apple(40, 40)


# The loop will carry on until the user exits the game (e.g. clicks the close button).
run = True


# -------- Main Program Loop -----------
while run:




    # --- Main event loop
    ## ----- NO BLIT ZONE START ----- ##
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if a.rect.collidepoint(event.pos):
                a.move(a.x + 3, a.y + 3)
    ##  ----- NO BLIT ZONE END  ----- ##


    ## FILL SCREEN, and BLIT here ##
    screen.fill((r, g, b))
    screen.blit(display_message, (0, 0))
    screen.blit(a.image, a.rect)
    pygame.display.update()
    ## END OF WHILE LOOP


# Once we have exited the main program loop we can stop the game engine:
pygame.quit()