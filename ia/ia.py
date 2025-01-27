import pygame
import random

# Configurações principais do jogo
TELA_LARGURA = 500
TELA_ALTURA = 800
COR_BRANCO = (255, 255, 255)
GRAVIDADE = 0.5

class Passaro:
    IMGS = [pygame.image.load("img/bird1.png"), pygame.image.load("img/bird2.png"), pygame.image.load("img/bird3.png")]
    ROTACAO_MAX = 25
    ROTACAO_VELOCIDADE = 20
    VELOCIDADE_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.img_contador = 0
        self.img = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = self.velocidade * self.tempo + 0.5 * GRAVIDADE * self.tempo ** 2

        if deslocamento >= 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y = self.y + deslocamento

        if deslocamento < 0 or self.y < self.altura + 50:
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.ROTACAO_VELOCIDADE

    def desenhar(self, tela):
        self.img_contador += 1
        self.img = self.IMGS[self.img_contador // self.VELOCIDADE_ANIMACAO % len(self.IMGS)]

        tela.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.topo = 0
        self.base = 0
        self.CANO_TOPO = pygame.image.load("pipe_top.png")
        self.CANO_BASE = pygame.image.load("pipe_bottom.png")
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.topo = self.altura - self.CANO_TOPO.get_height()
        self.base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.topo))
        tela.blit(self.CANO_BASE, (self.x, self.base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        topo_offset = (self.x - passaro.x, self.topo - round(passaro.y))
        base_offset = (self.x - passaro.x, self.base - round(passaro.y))

        b_point = passaro_mask.overlap(base_mask, base_offset)
        t_point = passaro_mask.overlap(topo_mask, topo_offset)

        if b_point or t_point:
            return True
        return False
