import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тир - стрельба по мишени")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройки игры
score = 0
font = pygame.font.SysFont(None, 36)


# Класс мишени
class Target:
    def __init__(self):
        self.radius = random.randint(20, 40)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Отражение от границ экрана
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Внутренние круги мишени
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius * 0.7)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius * 0.5)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius * 0.3)

    def is_hit(self, pos):
        distance = math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2)
        return distance <= self.radius


# Создание мишени
target = Target()
targets = [Target() for _ in range(3)]  # Несколько мишеней

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                for target in targets[:]:
                    if target.is_hit(event.pos):
                        targets.remove(target)
                        score += 1
                        targets.append(Target())  # Добавляем новую мишень

    # Обновление мишеней
    for target in targets:
        target.update()
        target.draw()

    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Инструкция
    instruction = font.render("Кликните по мишени, чтобы выстрелить", True, WHITE)
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()