import random

import pygame
from ball import Ball
from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 14)

balls = []
last_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_time) / 100.0
    last_time = current_time

    clock.tick(FPS)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:
                # Создание нового мяча
                radius = 20
                position = (WIDTH // 2, radius)
                ball = Ball(radius, position)
                ball.set_acceleration((0, 0))
                ball.set_velocity((0, 0))
                balls.append(ball)

            elif event.key == pygame.K_r:
                # Создание нового мяча
                radius = 20
                position = (WIDTH // 2, radius)
                ball = Ball(radius, position, 0, 1)
                ball.set_acceleration((0, 0))
                ball.set_velocity((0, 0))
                balls.append(ball)

            elif event.key == pygame.K_SPACE:
                for ball in balls:
                    ball.apply_bounce(30)
            elif event.key == pygame.K_a:
                for ball in balls:
                    ball.apply_force(random.randint(-10, 0))
            elif event.key == pygame.K_d:
                for ball in balls:
                    ball.apply_force(random.randint(0, 10))

    # Обновление и проверка столкновений мячей
    for i, ball in enumerate(balls):
        ball.update(delta_time)
        for other_ball in balls[i + 1:]:
            ball.detect_collision(other_ball)
        ball.draw(screen)

    pygame.display.flip()

pygame.quit()
