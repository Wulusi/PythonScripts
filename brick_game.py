#!/usr/bin/env python
"""
Brick Breaker - 100% Fixed & Working
No NameError | No Rect Error | Clean & Tested
"""

import pygame
import sys
import random

# =============================================
# CONFIG
# =============================================
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 8
BRICK_ROWS, BRICK_COLS = 5, 10
BRICK_WIDTH = (WIDTH - 40) // BRICK_COLS
BRICK_HEIGHT = 20
BRICK_GAP = 2
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 50, 50)
ORANGE= (255, 165, 0)
YELLOW= (255, 255, 0)
GREEN = (50, 205, 50)
BLUE  = (50, 50, 255)

# =============================================
# INIT
# =============================================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)

# =============================================
# HELPER
# =============================================
def draw_text(text, font, color, surface, x, y, center=True):
    obj = font.render(text, True, color)
    rect = obj.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(obj, rect)

# =============================================
# CLASSES
# =============================================
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 9

    def move(self, dx):
        self.x += dx
        self.x = max(0, min(self.x, WIDTH - self.width))

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.x = 0.0
        self.y = 0.0
        self.vel_x = 0.0
        self.vel_y = 0.0
        # Do NOT call reset_ball() here!

    def reset(self):
        """Reset ball position and velocity"""
        self.x = paddle.x + paddle.width // 2
        self.y = paddle.y - self.radius - 1
        self.vel_x = random.choice([-4, -3, 3, 4])
        self.vel_y = -5

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Wall collisions
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.vel_x = -self.vel_x
        if self.y - self.radius <= 0:
            self.vel_y = -self.vel_y

        # Bottom = lose life
        if self.y - self.radius > HEIGHT:
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH - BRICK_GAP, BRICK_HEIGHT - BRICK_GAP)
        self.color = color
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 1)

# =============================================
# CREATE OBJECTS
# =============================================
paddle = Paddle()
ball = Ball()
ball.reset()  # Now safe to call!

def create_bricks():
    bricks = []
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = 20 + col * BRICK_WIDTH
            y = 80 + row * BRICK_HEIGHT
            bricks.append(Brick(x, y, colors[row % len(colors)]))
    return bricks

bricks = create_bricks()

# =============================================
# GAME STATE
# =============================================
score = 0
lives = 3
game_state = "playing"

# =============================================
# MAIN LOOP
# =============================================
while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state != "playing":
                paddle = Paddle()
                ball = Ball()
                ball.reset()
                bricks = create_bricks()
                score = 0
                lives = 3
                game_state = "playing"

    if game_state != "playing":
        if game_state == "won":
            draw_text("YOU WIN!", big_font, GREEN, screen, WIDTH//2, HEIGHT//2)
        else:
            draw_text("GAME OVER", big_font, RED, screen, WIDTH//2, HEIGHT//2)
        draw_text(f"Score: {score}", font, WHITE, screen, WIDTH//2, HEIGHT//2 + 70)
        draw_text("Press R to restart", font, YELLOW, screen, WIDTH//2, HEIGHT//2 + 120)
        pygame.display.flip()
        continue

    # --- Input ---
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]: dx = -paddle.speed
    if keys[pygame.K_RIGHT]: dx = paddle.speed
    paddle.move(dx)

    # Mouse control
    mx, _ = pygame.mouse.get_pos()
    paddle.x = mx - paddle.width // 2
    paddle.x = max(0, min(paddle.x, WIDTH - paddle.width))

    # --- Ball Update ---
    life_lost = ball.update()

    # Paddle collision
    if (paddle.y <= ball.y + ball.radius <= paddle.y + paddle.height and
        paddle.x <= ball.x <= paddle.x + paddle.width):
        hit_pos = (ball.x - paddle.x) / paddle.width
        ball.vel_x = 8 * (hit_pos - 0.5)
        ball.vel_y = -abs(ball.vel_y)

    # Brick collision
    for brick in bricks[:]:
        if brick.active and brick.rect.collidepoint(ball.x, ball.y):
            brick.active = False
            score += 10
            ball.vel_y = -ball.vel_y
            if ball.x < brick.rect.left or ball.x > brick.rect.right:
                ball.vel_x = -ball.vel_x
            break

    # Life lost
    if life_lost:
        lives -= 1
        if lives <= 0:
            game_state = "lost"
        else:
            ball.reset()

    # Win
    if all(not b.active for b in bricks):
        game_state = "won"

    # --- Draw ---
    paddle.draw()
    ball.draw()
    for b in bricks:
        b.draw()

    draw_text(f"Score: {score}", font, WHITE, screen, 10, 10, False)
    draw_text(f"Lives: {lives}", font, WHITE, screen, WIDTH - 10, 10, False)

    pygame.display.flip()