import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Game settings
gravity = 0.4
jump_force = -6
pipe_width = 60
pipe_gap = 150
pipe_speed = 2
player_radius = 20
player_x = 50
player_y = HEIGHT // 2
player_velocity = 0

# Level settings
level = 1
max_level = 3
pipes = []
pipe_count = 0
immune = False  # Flag for immunity (power-up effect)
immune_time = 0  # Timer for immunity effect
IMMUNITY_DURATION = 7 * 60  # 15 seconds at 60 FPS

# Slow power-up settings
slow_effect = False
slow_time = 0
pipe_slow_duration = 5 * 60  # Duration of the pipe slow power-up (in frames)

# High Scores (will be loaded from the file)
high_scores = {1: 0, 2: 0, 3: 0}  # Default high scores for each level

# Fonts
font = pygame.font.SysFont('Arial', 32, bold=True)
button_font = pygame.font.SysFont('Arial', 24, bold=True)
blue_ball_font = pygame.font.SysFont('Arial', 50, bold=True)


# File for storing high scores
high_score_file = "high_scores.txt"

# Function to load high scores from a file
def load_high_scores():
    global high_scores
    try:
        with open(high_score_file, "r") as file:
            lines = file.readlines()
            for i in range(3):
                high_scores[i + 1] = int(lines[i].strip())  # Load each level's high score
    except FileNotFoundError:
        # If the file doesn't exist, create a new one with default scores
        save_high_scores()

# Function to save high scores to a file
def save_high_scores():
    with open(high_score_file, "w") as file:
        for i in range(1, 4):
            file.write(f"{high_scores[i]}\n")

# Function to create a new pipe (golden, red, or regular)
def create_pipe():
    height = random.randint(100, HEIGHT - pipe_gap - 100)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - (height + pipe_gap))

    # Randomly decide if the pipe should be golden (9% chance), red (0.05% chance), blue (0.01% chance), or regular
    is_gold = random.random() < 0.09
    is_red = random.random() < 0.08  # 0.05% chance for red pipe
    is_blue = random.random() < 0.0001  # 0.01% chance for blue pipe

    return top_pipe, bottom_pipe, is_gold, is_red, is_blue


# Function to reset the game
# Function to reset the game
def reset_game():
    global player_y, player_velocity, pipes, pipe_count, immune, immune_time, slow_effect, slow_time, pipe_speed, player_radius
    player_y = HEIGHT // 2
    player_velocity = 0
    pipes = []
    pipe_count = 0
    immune = False
    immune_time = 0
    slow_effect = False
    slow_time = 0
    pipe_speed = 2  # Set the default pipe speed to the base speed (adjust this as needed)
    player_radius = 20  # Reset player size (ensure this matches the default player size)


# Draw text on the screen
def draw_text(text, x, y, color=BLACK, font_type=font):
    label = font_type.render(text, True, color)
    screen.blit(label, (x, y))

# Draw buttons on the screen
def draw_button(text, x, y, width, height, color, text_color=BLACK):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, x + (width - button_font.size(text)[0]) // 2, y + (height - button_font.get_height()) // 2, text_color, button_font)

# Function to load the background image

def load_background():
    try:
        background = pygame.image.load ('BackgroundPy.jpg')  # Replace with the correct image file path
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale it to fit the screen size
        return background
    except pygame.error:
        print("Background image not found!")
        return None

# Main menu screen with background
def main_menu():
    global level
    background = load_background()  # Load the background image

    while True:
        # Fill the screen with the background image
        if background:
            screen.blit(background, (0, 0))  # Draw the background image
        else:
            screen.fill(WHITE)  # If no background, fill with white color

        draw_text("Blue Ball", WIDTH // 4.5, HEIGHT // 4, BLUE, blue_ball_font)

        # Center the buttons horizontally
        button_width = 100
        button_height = 50
        button_gap = 20
        total_width = button_width * 3 + button_gap * 2
        start_x = (WIDTH - total_width) // 2
        start_y = HEIGHT // 2

        # Draw level selection buttons
        draw_button("Level 1", start_x, start_y, button_width, button_height, WHITE)
        draw_button("Level 2", start_x + button_width + button_gap, start_y, button_width, button_height, WHITE)
        draw_button("Level 3", start_x + 2 * (button_width + button_gap), start_y, button_width, button_height, WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_x <= mouse_x <= start_x + button_width and start_y <= mouse_y <= start_y + button_height:
                    level = 1
                    return
                elif start_x + button_width + button_gap <= mouse_x <= start_x + 2 * (button_width + button_gap) and start_y <= mouse_y <= start_y + button_height:
                    level = 2
                    return
                elif start_x + 2 * (button_width + button_gap) <= mouse_x <= start_x + 3 * (button_width + button_gap) and start_y <= mouse_y <= start_y + button_height:
                    level = 3
                    return

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# Function to display game over dialog
def game_over():
    # Display "Game Over!" centered
    game_over_text = "Game Over!"
    text_width = font.size(game_over_text)[0]
    draw_text(game_over_text, (WIDTH - text_width) // 2, HEIGHT // 3, RED, font)
    
    # Display "Press any key to continue" centered
    press_key_text = "Press any key to continue"
    text_width = font.size(press_key_text)[0]
    draw_text(press_key_text, (WIDTH - text_width) // 2, HEIGHT // 2, BLACK, font)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_input = False

# Main game loop
# Main game loop update
def game_loop():
    global level, pipe_count, pipes, player_y, player_velocity, gravity, jump_force, pipe_speed, high_scores, immune, immune_time, player_radius, slow_effect, slow_time

    # Reset game variables
    reset_game()

    # Adjust game settings based on selected level
    if level == 1:
        pipe_speed = 2
    elif level == 2:
        pipe_speed = 5
    elif level == 3:
        pipe_speed = 7

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_velocity = jump_force

        # Update player position
        player_velocity += gravity
        player_y += player_velocity

        # Create new pipes when needed
        if len(pipes) == 0 or pipes[-1][0].x < WIDTH - 300:
            pipes.append(create_pipe())

        # Move pipes
        for pipe in pipes:
            pipe[0].x -= pipe_speed
            pipe[1].x -= pipe_speed

        # Remove pipes that are off-screen
        pipes = [pipe for pipe in pipes if pipe[0].x + pipe_width > 0]

        # Check for collisions
        player_rect = pygame.Rect(player_x, player_y, player_radius * 2, player_radius * 2)
        for top_pipe, bottom_pipe, is_gold, is_red, is_blue in pipes:
            if player_rect.colliderect(top_pipe) or player_rect.colliderect(bottom_pipe):
                if not immune:  # Only trigger game over if not immune
                    print("Game Over!")
                    # Update high score if needed
                    if pipe_count > high_scores[level]:
                        high_scores[level] = pipe_count
                    save_high_scores()  # Save the high scores to the file
                    game_over()  # Show game over dialog
                    reset_game()
                    main_menu()
                    return

            # Check if player has passed the pipes and collected a power-up from golden pipes
            if top_pipe.x + pipe_width < player_x and not top_pipe.colliderect(player_rect):
                pipe_count += 1
                if is_gold:
                    immune = True
                    immune_time = IMMUNITY_DURATION  # Activate immunity for 15 seconds
                    player_radius = 10  # Reduce player size
                elif is_red:
                    # Apply slow effect
                    slow_effect = True
                    slow_time = pipe_slow_duration  # Set how long the slow effect lasts
                    pipe_speed = max(1, pipe_speed - 1)  # Slow down the pipes (min 1 speed)
                elif is_blue:
                    # Add 1000 points for passing a blue pipe
                    pipe_count += 1000  # Increase score by 1000 points

        # Update immunity timer
        if immune:
            immune_time -= 1
            if immune_time <= 0:
                immune = False
                player_radius = 20  # Restore player size after power-up ends

        # Update slow effect timer
        if slow_effect:
            slow_time -= 1
            if slow_time <= 0:
                slow_effect = False
                pipe_speed = 2 if level == 1 else 5 if level == 2 else 7  # Restore original pipe speed

        # Draw player
        pygame.draw.circle(screen, BLUE, (player_x + player_radius, int(player_y)), player_radius)

        # Draw pipes
        for top_pipe, bottom_pipe, is_gold, is_red, is_blue in pipes:
            if is_gold:
                pygame.draw.rect(screen, GOLD, top_pipe)
                pygame.draw.rect(screen, GOLD, bottom_pipe)
            elif is_red:
                pygame.draw.rect(screen, RED, top_pipe)
                pygame.draw.rect(screen, RED, bottom_pipe)
            elif is_blue:
                pygame.draw.rect(screen, BLUE, top_pipe)
                pygame.draw.rect(screen, BLUE, bottom_pipe)
            else:
                pygame.draw.rect(screen, GREEN, top_pipe)
                pygame.draw.rect(screen, GREEN, bottom_pipe)

        # Draw level and score
        draw_text(f"Level: {level}", 10, 10)
        draw_text(f"Score: {pipe_count}", 10, 40)

        # Draw high score for the current level
        draw_text(f"High Score: {high_scores[level]}", 10, 70)

        # Check if the player has fallen off-screen
        if player_y > HEIGHT - player_radius * 2 or player_y < 0:
            print("Game Over!")
            if pipe_count > high_scores[level]:
                high_scores[level] = pipe_count
            save_high_scores()  # Save the high scores to the file
            game_over()  # Show game over dialog
            reset_game()
            main_menu()

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# Start the game
load_high_scores()
while True:
   main_menu()
   game_loop()
