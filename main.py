import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake ni Bokni")
clock = pygame.time.Clock()
snake_speed = 10

# Fonts
font_style = pygame.font.SysFont(None, 35)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])

def draw_score(score):
    score_text = font_style.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])

def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, SCREEN_WIDTH - GRID_SIZE) / GRID_SIZE) * GRID_SIZE
        foody = round(random.randrange(0, SCREEN_HEIGHT - GRID_SIZE) / GRID_SIZE) * GRID_SIZE
        if [foodx, foody] not in snake_list:
            return foodx, foody

def game_loop():
    game_over = False
    game_close = False

    # Initial snake setup
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Initial food setup
    foodx, foody = generate_food(snake_list)

    # Initial score setup
    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message(f"You Lost! Press Q-Quit or C-Play Again. Final Score: {score}", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        game_loop()  # Restart the game
                        return  # Exit the current game_loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_change == 0:  # Prevent the snake from reversing
                        x1_change = -GRID_SIZE
                        y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change == 0:  # Prevent the snake from reversing
                        x1_change = GRID_SIZE
                        y1_change = 0
                elif event.key == pygame.K_UP:
                    if y1_change == 0:  # Prevent the snake from reversing
                        y1_change = -GRID_SIZE
                        x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if y1_change == 0:  # Prevent the snake from reversing
                        y1_change = GRID_SIZE
                        x1_change = 0

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [foodx, foody, GRID_SIZE, GRID_SIZE])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        draw_score(score)  # Draw the score
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_list)
            length_of_snake += 1
            score += 10  # Increase the score

        clock.tick(snake_speed)

game_loop()
