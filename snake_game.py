import pygame
import random
import time

pygame.init()

# Screen size
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Advanced Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 150, 255)

# Snake settings
block = 10
speed = 9

clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("comicsansms", 25)

# Score display
def show_score(score):
    value = font.render("Score: " + str(score), True, white)
    screen.blit(value, [10, 10])

# Timer display
def show_timer(seconds_left):
    value = font.render("Time Left: " + str(seconds_left), True, white)
    screen.blit(value, [400, 10])

# Draw snake
def draw_snake(snake_body):
    for part in snake_body:
        pygame.draw.rect(screen, green, [part[0], part[1], block, block])

# Main game function
def gameLoop():
    game_over = False
    game_close = False

    # Initial snake position
    x = width // 2
    y = height // 2

    dx = 0
    dy = 0

    snake_body = []
    snake_length = 1

    # Food position
    foodx = random.randrange(0, width, block)
    foody = random.randrange(0, height, block)

    # Food timer (60 sec rule)
    last_eat_time = time.time()

    while not game_over:

        while game_close:
            screen.fill(black)
            msg = font.render("Game Over! Press C to Restart or Q to Quit", True, red)
            screen.blit(msg, [80, 180])
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -block
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = block

        # Update position
        x += dx
        y += dy

        # ✅ Wrap Around Boundary (Teleport Effect)
        if x >= width:
            x = 0
        elif x < 0:
            x = width - block

        if y >= height:
            y = 0
        elif y < 0:
            y = height - block

        # Background
        screen.fill(blue)

        # Draw food
        pygame.draw.rect(screen, red, [foodx, foody, block, block])

        # Snake movement
        head = [x, y]
        snake_body.append(head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # ✅ Game Over if snake cuts itself
        for part in snake_body[:-1]:
            if part == head:
                game_close = True

        # ✅ Food timer rule
        time_since_eat = int(time.time() - last_eat_time)
        time_left = 60 - time_since_eat

        if time_left <= 0:
            game_close = True

        # Draw snake + score + timer
        draw_snake(snake_body)
        show_score(snake_length - 1)
        show_timer(time_left)

        pygame.display.update()

        # ✅ Eat food resets timer
        if x == foodx and y == foody:
            foodx = random.randrange(0, width, block)
            foody = random.randrange(0, height, block)
            snake_length += 1
            last_eat_time = time.time()  # Reset timer

        clock.tick(speed)

    pygame.quit()
    quit()

# Run game
gameLoop()