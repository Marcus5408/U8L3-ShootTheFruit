﻿import pygame
import random
import json
from datetime import datetime
from apple import Apple
from enemy import Enemy


# set up pygame modules
pygame.init()
pygame.font.init()
my_font = pygame.font.Font("u8l3_shootthefruit/DUBAI-REGULAR.TTF", 15)
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

# -------- Pre-Program Prep -----------
score = 0
run, game_end, instant_fail = True, False, False
time_started = datetime.now()
randomize_position(a)
randomize_position(e)
ENEMY_MOVE_EVENT = pygame.USEREVENT
pygame.time.set_timer(ENEMY_MOVE_EVENT, 1000)

# check for high score json
data_file = f"{__file__.replace('__init__.py', '')}data.json"
try:
    with open(data_file, "r") as file:
        data = json.load(file)
        high_score_date = data["date"]
        high_score = data["high_score"]
except FileNotFoundError:
    with open(data_file, "w") as file:
        data = {
            "date": datetime.now().strftime("%m/%d/%Y %H:%M"),
            "high_score": 0
        }
        json.dump(data, file)
    with open(data_file, "r") as file:
        data = json.load(file)
        high_score_date = data["date"]
        high_score = data["high_score"]

# The loop will carry on until the user exits the game (e.g. clicks the close button).
# -------- Main Program Loop -----------
while run:
    # --- Main event loop ---
    ## ----- NO BLIT ZONE START ----- ##
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        if not game_end:
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
                        score = score - 1
                if not instant_fail:
                    if score < 0 or score == 10:
                        game_end = True
                randomize_position(a)
            if event.type == ENEMY_MOVE_EVENT:
                randomize_position(e)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_end = False
                    score = 0
                    time_started = datetime.now()
                    randomize_position(a)
                    randomize_position(e)
    ##  ----- NO BLIT ZONE END  ----- ##
    
    ## FILL SCREEN, and BLIT here ##
    screen.fill((r, g, b))
    if not game_end:
        time_elapsed = datetime.now() - time_started
        add_text_to_screen(f"Click the fruit to score! Current score: {score}", (0, 0))
        add_text_to_screen(f"High score: {high_score} (Achieved {high_score_date})", (0, 15))
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
    ## END OF WHILE LOOP ##

if score > high_score:
    with open(data_file, "w") as file:
        file.truncate(0)
        data = {
            "date": datetime.now().strftime("%m/%d/%Y %H:%M"),
            "high_score": score
        }
        json.dump(data, file)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
