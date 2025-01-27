
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

# Definindo as variáveis globais necessárias
MAP_WIDTH = 10  # Exemplo de largura do mapa
MAP_HEIGHT = 10  # Exemplo de altura do mapa
BLOCK_SIZE = 1  # Tamanho do bloco

class SnakeModel:
    def __init__(self):
        self.model = Sequential([
            Flatten(input_shape=(MAP_WIDTH * MAP_HEIGHT,)),
            Dense(64, activation="relu"),
            Dense(4)
        ])
        self.model.compile(optimizer="adam", loss="mse")

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, epochs=100)

# Código para gerar os dados de treinamento
X = []
y = []

for _ in range(10000):
    game_state = np.zeros((MAP_WIDTH * MAP_HEIGHT,))
    
    # Definindo a posição da cabeça da cobra
    head_x = np.random.randint(0, MAP_WIDTH)
    head_y = np.random.randint(0, MAP_HEIGHT)
    
    snake_pos = [(head_x + i * BLOCK_SIZE, head_y) for i in range(5)]
    food_pos = (np.random.randint(0, MAP_WIDTH), np.random.randint(0, MAP_HEIGHT))

    game_state = np.array([1 if (x, y) in snake_pos else 0 for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT)])

    # Gerando a próxima posição da cobra
    move_x, move_y = np.random.choice([-1, 0, 1], size=2)  # Move em uma direção aleatória
    next_head_x = (head_x + move_x) % MAP_WIDTH
    next_head_y = (head_y + move_y) % MAP_HEIGHT
    next_snake_pos = [(next_head_x + i * BLOCK_SIZE, next_head_y) for i in range(5)]

    next_game_state = np.array([1 if (x, y) in next_snake_pos else 0 for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT)])

    X.append(game_state)
    y.append(next_game_state)

X_train = np.array(X)
y_train = np.array(y)

model = SnakeModel()
model.train(X_train, y_train)
