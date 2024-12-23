import pygame
import random
from constants import *


class Ball:
    def __init__(self, radius, position, gm=9.8, elasticity=0.8):
        self.radius = radius
        self.position = list(position)  # (x, y)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Случайный цвет
        self.x_velocity = random.randint(-4, 4)  # не работает(
        self.y_velocity = 0
        self.x_acceleration = 0
        self.y_acceleration = 0
        self.gm = gm
        self.elasticity = elasticity

    def set_acceleration(self, acceleration):
        self.x_acceleration, self.y_acceleration = acceleration

    def set_velocity(self, velocity):
        self.x_velocity, self.y_velocity = velocity

    def apply_bounce(self, force):
        self.y_velocity -= force  # Подбрасывание

    def apply_force(self, force):
        self.x_velocity += force
        # print(self.x_velocity, self.y_velocity)

    def update(self, delta_time):
        # Обновление скорости
        self.y_velocity += self.gm * delta_time
        self.x_velocity += self.x_acceleration * delta_time
        self.y_velocity += self.y_acceleration * delta_time

        # Обновление позиции
        self.position[0] += self.x_velocity * delta_time
        self.position[1] += self.y_velocity * delta_time

        # Проверка на столкновение с границами
        if self.position[0] - self.radius < 0:  # Левый край
            self.position[0] = self.radius
            self.x_velocity = -self.x_velocity * self.elasticity
        elif self.position[0] + self.radius > WIDTH:  # Правый край
            self.position[0] = WIDTH - self.radius
            self.x_velocity = -self.x_velocity * self.elasticity

        if self.position[1] - self.radius < 0:  # Верхний край
            self.position[1] = self.radius
            self.y_velocity = -self.y_velocity * self.elasticity
        elif self.position[1] + self.radius > HEIGHT:  # Нижний край
            self.position[1] = HEIGHT - self.radius
            self.y_velocity = -self.y_velocity * self.elasticity

    def detect_collision(self, other):
        # Проверка расстояния между центрами мячей
        dx = self.position[0] - other.position[0]
        dy = self.position[1] - other.position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.radius + other.radius:
            # Упругое столкновение
            normal_x = dx / distance
            normal_y = dy / distance

            relative_velocity_x = self.x_velocity - other.x_velocity
            relative_velocity_y = self.y_velocity - other.y_velocity

            dot_product = (relative_velocity_x * normal_x + relative_velocity_y * normal_y)

            if dot_product > 0:
                return

            restitution = min(self.elasticity, other.elasticity)

            self.x_velocity -= dot_product * normal_x * restitution
            self.y_velocity -= dot_product * normal_y * restitution
            other.x_velocity += dot_product * normal_x * restitution
            other.y_velocity += dot_product * normal_y * restitution

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)
