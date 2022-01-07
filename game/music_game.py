import sys
import pygame
from math import *
import random
from time import *
from decimal import Decimal
#音楽ゲーム デレステ風3レーン とりあえず1曲できるところから

BPM = 153#曲のBPM
SPEED = BPM#レーンスピード できれば調整可能にしたい
OFFSET = 1#曲とのタイミング調整
syousetsu_time = 240/BPM #1小節あたりの秒数
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
        if abs(self.y-height*4//5) <= 20:
            return "perfect"
        elif abs(self.y-height*4//5) <= 40:
            return "miss"



if __name__ == '__main__':
    pygame.init()
    # Clockオブジェクトの生成
    clock = pygame.time.Clock()
    # フレームレート（1秒間に何回画面を更新するか）の設定
    clock.tick(fps)

    # メイン画面（Surface）初期化(横, 縦)
    main_surface = pygame.display.set_mode((width,height))

    pygame.display.set_caption('music game')

    pygame.mixer.init(frequency = 44100)    # 初期設定
    pygame.mixer.music.load("src/lovelyflower.wav")     # 音楽ファイルの読み込み
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(1)              # 音楽の再生回数(1回)
    #レーンごとに分けて管理
    humen = [["101","010","100","111","000","000","000","000"]]
    lane1 = []
    lane2 = []
    lane3 = []
    isflowed = [[False for j in range(len(humen[i]))] for i in range(len(humen))]
    sleep(OFFSET)
    start = perf_counter()

    while True:

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

        time = perf_counter() - start #今の時間
        if int(time/syousetsu_time) <= len(humen)-1:
            syousetsu_num = int(time/syousetsu_time)
            syousetsu = humen[syousetsu_num]#1小節に焦点を当てる
            haku = len(syousetsu) #小節が何拍か
            if modf((Decimal(time)-(Decimal(syousetsu_num)*Decimal(syousetsu_time)))/(Decimal(syousetsu_time)/Decimal(haku)))[0] <= 0.15:
                draw_haku = int(modf((Decimal(time)-(Decimal(syousetsu_num)*Decimal(syousetsu_time)))/(Decimal(syousetsu_time)/Decimal(haku)))[1])
                notes = syousetsu[draw_haku]
                if not isflowed[syousetsu_num][draw_haku]:
                    if notes[0] == '1':
                        lane1.append(Note(1,0))
                    if notes[1] == '1':
                        lane2.append(Note(2,0))
                    if notes[2] == '1':
                        lane3.append(Note(3,0))
                isflowed[syousetsu_num][draw_haku] = True

        pygame.display.update()
        for note in lane1:
            if note.y >= height:
                lane1.remove(note)
                print("miss")
            else:
                note.move()
        for note in lane2:
            if note.y >= height:
                lane2.remove(note)
                print("miss")
            note.move()
        for note in lane3:
            if note.y >= height:
                lane3.remove(note)
                print("miss")
            note.move()

        key = pygame.key.get_pressed()
        if key[pygame.K_g] and not Gispushed and lane1:
            Gispushed = True
            head,*tail = lane1
            if abs(head.y-height*4//5) <= 30:
                print(head.judge())
                lane1 = tail
        elif not key[pygame.K_g]:
            Gispushed = False

        if key[pygame.K_h] and not Hispushed and lane2:
            Hispushed = True
            head,*tail = lane2
            if abs(head.y-height*4//5) <= 30:
                print(head.judge())
                lane2 = tail

        elif not key[pygame.K_h]:
            Hispushed = False
        if key[pygame.K_j] and not Jispushed and lane3:
            Jispushed = True
            head,*tail = lane3
            if abs(head.y-height*4//5) <= 30:
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
