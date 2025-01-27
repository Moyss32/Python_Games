import pygame
import numpy as np
import tensorflow as tf

# Configuração do jogo
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
FPS = 10

# Criando o mapa do jogo
MAP_WIDTH = WIDTH // BLOCK_SIZE
MAP_HEIGHT = HEIGHT // BLOCK_SIZE

class SnakeGame:
    def __init__(self):
        self.pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.snake = [(100, 100), (120, 100), (140, 100)]
        self.direction = "RIGHT"
        self.food = (200, 200)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"

            # Atualizando a posição da cobra
            head_x, head_y = self.snake[-1]
            if self.direction == "UP":
                new_head = (head_x, head_y - BLOCK_SIZE)
            elif self.direction == "DOWN":
                new_head = (head_x, head_y + BLOCK_SIZE)
            elif self.direction == "LEFT":
                new_head = (head_x - BLOCK_SIZE, head_y)
            elif self.direction == "RIGHT":
                new_head = (head_x + BLOCK_SIZE, head_y)

            # Verificando se a cobra colidiu com as paredes ou consigo mesma
            if (new_head[0] < 0 or new_head[0] >= MAP_WIDTH * BLOCK_SIZE or
                    new_head[1] < 0 or new_head[1] >= MAP_HEIGHT * BLOCK_SIZE or
                    new_head in self.snake[:-1]):
                print("Game Over!")
                running = False

            # Atualizando a comida
            if np.linalg.norm(np.array(self.food) - np.array(new_head)) < BLOCK_SIZE:
                self.food = (np.random.randint(0, MAP_WIDTH * BLOCK_SIZE),
                             np.random.randint(0, MAP_HEIGHT * BLOCK_SIZE))

            # Adicionando a nova posição da cobra à lista
            self.snake.append(new_head)

            # Removendo a última posição da cobra se necessário
            if len(self.snake) > 10:
                self.snake.pop(0)

            # Desenhando o mapa do jogo
            self.screen.fill((0, 0, 0))
            for pos in self.snake:
                pygame.draw.rect(self.screen, (255, 255, 255), (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, (0, 255, 0), (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

            # Atualizando a tela
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
