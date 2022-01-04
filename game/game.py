import sys
import pygame
from math import *
import random



pygame.init()
# メイン画面（Surface）初期化(横, 縦)
DISPLAYSURF = pygame.display.set_mode((400,400))

pygame.display.set_caption('Three card')

GREEN = (0, 127, 0)

width, height = 100, 144
ace1 = pygame.image.load('src/card_back.png')
card1 = pygame.transform.scale(ace1, (width, height))
card2 = pygame.transform.scale(ace1, (width, height))
card3 = pygame.transform.scale(ace1, (width, height))
pygame.mixer.init(frequency = 44100)    # 初期設定
pygame.mixer.music.load("src/lovelyflower.wav")     # 音楽ファイルの読み込み
pygame.mixer.music.play(1)              # 音楽の再生回数(1回)

while True:
    DISPLAYSURF.fill(GREEN)
    x, y = 10, 10
    DISPLAYSURF.blit(card1, (x,y))
    DISPLAYSURF.blit(card2, (x + width,y))
    DISPLAYSURF.blit(card3, (x + width * 2,y))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pygame.mixer.music.stop()               # 再生の終了
