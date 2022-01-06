import sys
import pygame
from math import *
import random
#音楽ゲーム デレステ風3レーン とりあえず1曲できるところから

BPM = 153#曲のBPM
SPEED = BPM#レーンスピード できれば調整可能にしたい
OFFSET = 0#曲とのタイミング調整
BACKGROUND = (0,0,0)
Gispushed = False
Hispushed = False
Jispushed = False
radius = 20
fps = 30
i=0

width, height = 400, 400

class Note:
    #ノーツ
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
    def judge(self):
        #判定
        if abs(self.y-height*4//5) <= 10:
            return "perfect"
        elif abs(self.y-height*4//5) <= 30:
            return "miss"



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
    lane1 = []
    lane2 = []
    lane3 = []
    lane1.append(note)
    lane3.append(Note(3,0))

    while True:
        # フレームレート（1秒間に何回画面を更新するか）の設定
        clock.tick(fps)

        main_surface.fill((0,0,0))
        #判定レーンの描画
        pygame.draw.circle(main_surface, (255,255,255), (width//2,height*4//5), radius, width = 2)
        pygame.draw.circle(main_surface, (255,255,255), (width//3,height*4//5), radius, width = 2)
        pygame.draw.circle(main_surface, (255,255,255), (width*2//3,height*4//5), radius, width = 2)
        for note in lane1:
            note.draw()
        for note in lane2:
            note.draw()
        for note in lane3:
            note.draw()

        pygame.display.update()
        for note in lane1:
            if note.y >= height:
                lane1.remove(note)
            else:
                note.move()
        for note in lane2:
            note.move()
        for note in lane3:
            note.move()

        key = pygame.key.get_pressed()
        if key[pygame.K_g] and not Gispushed:
            Gispushed = True
            head,*tail = lane1
            print(head.judge())
            lane1 = tail
        elif not key[pygame.K_g]:
            Gispushed = False

        if key[pygame.K_h] and not Hispushed:
            Hispushed = True
            head,*tail = lane2
            print(head.judge())
            lane2 = tail

        elif not key[pygame.K_h]:
            Hispushed = False
        if key[pygame.K_j] and not Jispushed:
            Jispushed = True
            head,*tail = lane3
            print(head.judge())
            lane3 = tail
        elif not key[pygame.K_j]:
            Jispushed = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pygame.mixer.music.stop()               # 再生の終了
