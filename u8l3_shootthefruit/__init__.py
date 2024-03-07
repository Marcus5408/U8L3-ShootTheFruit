import pygame
import random
from datetime import datetime
from apple import Apple
from enemy import Enemy
import time
import asyncio


# set up pygame modules
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("Arial", 15)
pygame.display.set_caption("Shoot the Fruit!")


# set up variables for the display
SCREEN_HEIGHT = 370
SCREEN_WIDTH = 530
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)


r = 50
g = 0
b = 100

# Instantiate the apple and enemy
a = Apple(40, 40)
e = Enemy(40, 40)


def add_text_to_screen(text: str, position: tuple) -> None:
    text = my_font.render(text, True, (255, 255, 255))
    screen.blit(text, position)


def randomize_position(entity:object) -> None:
    entity.move(
        random.randint(0, SCREEN_WIDTH - a.image_size[0]),
        random.randint(0, SCREEN_HEIGHT - a.image_size[1]),
    )

# The loop will carry on until the user exits the game (e.g. clicks the close button).
score = 0
run, game_end, instant_fail = True, False, False
time_started = datetime.now()
randomize_position(a)
randomize_position(e)
ENEMY_MOVE_EVENT = pygame.USEREVENT
pygame.time.set_timer(ENEMY_MOVE_EVENT, 1000)
# -------- Main Program Loop -----------
while run:
    # --- Main event loop ---
    ## ----- NO BLIT ZONE START ----- ##
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if a.rect.collidepoint(event.pos):
                if (
                    a.image.get_at((event.pos[0] - a.rect.x, event.pos[1] - a.rect.y))[3]
                    != 0
                ):
                    score = score + 1 if score < 11 else score
            else:
                if e.rect.collidepoint(event.pos):
                    if (
                        e.image.get_at((event.pos[0] - e.rect.x, event.pos[1] - e.rect.y))[3]
                        != 0
                    ):
                        game_end = True
                        instant_fail = True
                else:
                    score = score - 1 if score > 0 else score
            if not instant_fail:
                game_end = True if score == 0 else False
                game_end = True if score == 10 else False
            randomize_position(a)
        if event.type == ENEMY_MOVE_EVENT:
            randomize_position(e)
    ##  ----- NO BLIT ZONE END  ----- ##
    
    ## FILL SCREEN, and BLIT here ##
    screen.fill((r, g, b))
    if not game_end:
        time_elapsed = datetime.now() - time_started
        add_text_to_screen(f"Click the fruit to score! Current score: {score}", (0, 0))
        screen.blit(a.image, a.rect)
        screen.blit(e.image, e.rect)
    else:
        time_elapsed = time_elapsed
        add_text_to_screen(f"Current score: {score}", (0, 0))
        message = "Thanks for playing!" if score > 0 else "Game over! You lose!"
        display_message = my_font.render(message, True, (255, 255, 255))
        screen.blit(
            display_message,
            (
                SCREEN_WIDTH // 2 - display_message.get_width() // 2,
                SCREEN_HEIGHT // 2 - display_message.get_height() // 2,
            ),
        )
    message = f"Time elapsed: {time_elapsed.seconds}.{time_elapsed.microseconds // 1000} seconds"
    display_message = my_font.render(message, True, (255, 255, 255))
    screen.blit(display_message, (0, SCREEN_HEIGHT - display_message.get_height()))
    pygame.display.update()
    ## END OF WHILE LOOP


# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
