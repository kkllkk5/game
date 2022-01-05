import sys
import pygame
from math import *
import random
#音楽ゲーム デレステ風3レーン とりあえず1曲できるところから

BPM = 153
SPEED = BPM
radius = 20
fps = 30

width, height = 400, 400

class Note:
    def __init__(self,line,y):
        # 初期化
        self.line = line#3つのレーンのうちのどこか
        self.y = y

    def move(self):
        #上から降ってくる
        self.y = self.y + SPEED/fps

    def draw(self):
        #描画
        if self.line == 1:
            pygame.draw.circle(main_surface, (0,0,255), (width//3, self.y), radius)
        elif self.line == 2:
            pygame.draw.circle(main_surface, (0,0,255), (width//2, self.y), radius)
        elif self.line == 3:
            pygame.draw.circle(main_surface, (0,0,255), (width*2//3,self.y), radius)



if __name__ == '__main__':
    pygame.init()
    # Clockオブジェクトの生成
    clock = pygame.time.Clock()
    # メイン画面（Surface）初期化(横, 縦)
    main_surface = pygame.display.set_mode((width,height))

    pygame.display.set_caption('music game')

    pygame.mixer.init(frequency = 44100)    # 初期設定
    pygame.mixer.music.load("src/lovelyflower.wav")     # 音楽ファイルの読み込み
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(1)              # 音楽の再生回数(1回)
    note = Note(1,0)
    while True:
        # フレームレート（1秒間に何回画面を更新するか）の設定
        clock.tick(fps)

        main_surface.fill((0,0,0))
        #判定レーンの描画
        pygame.draw.circle(main_surface, (255,255,255), (width//2,height*4//5), radius, width = 2)
        pygame.draw.circle(main_surface, (255,255,255), (width//3,height*4//5), radius, width = 2)
        pygame.draw.circle(main_surface, (255,255,255), (width*2//3,height*4//5), radius, width = 2)
        note.draw()


        pygame.display.update()
        note.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pygame.mixer.music.stop()               # 再生の終了
