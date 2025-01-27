import pygame
from pygame.locals import *
from sys import exit
import os
import random

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640
ALTURA = 480
BRANCO = (255,255,255)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, "sons_death_sound.wav"))
som_colisao.set_volume(1)
som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, "sons_score_sound.wav"))
som_pontuacao.set_volume(1)
colidiu = False


escolha_obstaculo = random.choice([0, 1])

pontos = 0


velocidade_jogo = 10


def exibir_msgm(msgm, tam_fonte, cor):
    font = pygame.font.SysFont('comicsansms', tam_fonte, True, False)
    mensagem = f'{msgm}'
    texto_formatado = font.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    dino.rect.y =  ALTURA - 180
    dino.pulo = False
    dino_voador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obstaculo = random.choice([0, 1])

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, "sons_jump_sound.wav"))
        self.som_pulo.set_volume(1)
        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.pos_y_inic =  ALTURA - 180
        self.rect.center = (100, ALTURA - 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 120:
                self.pulo = False
            self.rect.y -= 30
        else:
            if self.rect.y < self.pos_y_inic:
                self.rect.y += 30
            else:
                self.rect.y = self.pos_y_inic

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =  sprite_sheet.subsurface((7*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(50, 230, 60)
        self.rect.x = random.randrange(50, 230, 60)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = random.randrange(50, 230, 40)
        
        if 50 <= self.rect.y < 100:
            self.rect.x -= 4
        elif 100 <= self.rect.y < 150:
           self.rect.x -= 6
        elif 150 <= self.rect.y < 200:
            self.rect.x -= 8
        else:
           self.rect.x -= 10

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image =  sprite_sheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 131
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
           self.rect.x = LARGURA
        self.rect.x -= 12

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =  sprite_sheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.escolha = escolha_obstaculo
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (LARGURA, ALTURA - 131)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha ==0: 
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0, 32, 32))
            img = pygame.transform.scale(img, (32 * 2.5, 32 * 3))
            self.imagens.append(img)


        self.index_lista = 0
        self.image = self.imagens[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA, 330)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 1: 
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens[int(self.index_lista)]

        

todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)
grupo_obstaculos = pygame.sprite.Group()

for i in range(6):
    nuven = Nuvens()
    todas_as_sprites.add(nuven)

for i in range(LARGURA*3//64):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cacto = Cacto()
todas_as_sprites.add(cacto)

grupo_obstaculos.add(cacto)
dino_voador = DinoVoador()
todas_as_sprites.add(dino_voador)
grupo_obstaculos.add(dino_voador)


relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inic:
                   pass 
                else:
                    dino.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = random.choice([0, 1])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
        morreu = exibir_msgm("Morreu!!", 50, (255,32,32))#Vermelho, Verde, Azul
        tela.blit(morreu, (LARGURA//2, ALTURA//2))
        reset = exibir_msgm('Pressione "R" para reiniciar', 24 , (25,25,25))
        tela.blit(reset, (LARGURA//2,ALTURA//2 + 60))

    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibir_msgm(pontos, 40, (0,0,0))
        

    if pontos % 100 == 0:

        som_pontuacao.play()
        if velocidade_jogo <= 42:
            velocidade_jogo += 1
        else:
            velocidade_jogo += 0

    tela.blit(texto_pontos, (520, 10))

    pygame.display.flip()