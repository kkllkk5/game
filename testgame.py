import sys
import pygame
from math import *
import random

height = 400
width = 420

time = 0

START, PLAY, GAMEOVER = (0, 1, 2)
game_state = PLAY

class Complex:
    #複素数
    def __init__(self, x,y):
        # 初期化
        self.x = x
        self.y = y
    def add(self,c):
        return Complex(self.x+c.x,self.y+c.y)
    def mult(self,c):
        return Complex(self.x*c.x-self.y*c.y,self.x*c.y+self.y*c.x)
    def minus(self,c):
        return Complex(self.x-c.x,self.y-c.y)

class Ball:
    def __init__(self,x,y,omega):
        # 初期化
        self.x = x
        self.y = y
        self.omega = omega#角速度

    def move(self):
        global width,height
        #回る
        position = Complex(self.x,self.y)
        center = Complex(width//2,height//2)
        position = center.add(position.minus(center).mult(Complex(cos(radians(self.omega)),sin(radians(self.omega)))))
        self.x = position.x
        self.y = position.y

class Enemy:
    def __init__(self,x,y):
        # 初期化
        self.x = x
        self.y = y
    def move(self):
        global width,height
        center = (width//2,height//2)
        direction = (center[0]-self.x,center[1]-self.y)
        norm = sqrt(direction[0]**2+direction[1]**2)
        self.x = self.x + direction[0]*3/norm
        self.y = self.y + direction[1]*3/norm



def main():
    global time,game_state,PLAY,GAMEOVER
    # pygameの初期化
    pygame.init()
    # メイン画面（Surface）初期化(横, 縦)
    main_surface = pygame.display.set_mode((width,height))
    # メイン画面のタイトル
    pygame.display.set_caption("Pygame Sample 2")
    # Clockオブジェクトの生成
    clock = pygame.time.Clock()

    radius = 100

    #ボールのy座標
    x = width//2
    y = height//2 - radius
    omega = 5
    ball = Ball(x,y,omega)#角速度
    r = 20#直径
    # ループを続けるかのフラグ
    isover = False
    enemy_list =[]
    score = 0
    font = pygame.font.Font(None, 40)
    text = font.render("Score", True, (0,0,0))
    # 終了イベント発生までループをまわす
    while True:
        if game_state == PLAY:
            time = (time+1)%60
            # イベントを取得
            for event in pygame.event.get():
                # 終了イベント（画面の×ボタン押下など）の場合、
                # ループを抜ける
                if event.type == pygame.QUIT:
                    # 終了処理
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        ball.omega = omega
                    if event.key == pygame.K_LEFT:
                        ball.omega = -omega

            # メイン画面の初期化
            main_surface.fill((255, 255, 255))
            pygame.draw.circle(main_surface, (1,0,0), (width//2, height//2), radius,width=3)

            # ボールの座標を更新
            # ボールの描画
            pygame.draw.circle(main_surface, (255,0,0), (ball.x,ball.y), r)

            if (time % 10) == 1:
                score = score + 10
                pos = random.randint(0,(width+height)*2)
                if 0 <= pos <= width:
                    #上の端に設置
                    enemy_list.append(Enemy(pos,0))
                elif pos <= width+height:
                    #右の端に設置
                    enemy_list.append(Enemy(width,pos-(width)))
                elif pos <= 2*width+height:
                    #下の端に設置
                    enemy_list.append(Enemy(width-(pos-(width+height)),height))
                else:
                    #左の端に設置
                    enemy_list.append(Enemy(0,pos-(width*2+height)))
            for enemy in enemy_list:
                pygame.draw.circle(main_surface, (0,255,0), (enemy.x,enemy.y), 5)
                enemy.move()
                if (enemy.x-ball.x)**2 + (enemy.y-ball.y)**2 <= r**2:
                    game_state = GAMEOVER

            enemy_list = list(filter(lambda enemy: sqrt((enemy.x-width//2)**2+(enemy.y-height//2)**2) > 2,enemy_list))
            ball.move()

            # メイン画面の更新
            text2 = font.render(str(score), True, (0,0,0))
            main_surface.blit(text, (250, 10))
            main_surface.blit(text2, (280, 40))
            pygame.display.update()
            # フレームレート（1秒間に何回画面を更新するか）の設定
            clock.tick(20)
        elif game_state == GAMEOVER:
            main_surface.fill((220, 220, 220))
            gameover_text = font.render("GAME OVER", True, (255,0,0))
            main_surface.blit(gameover_text, (120, 160))
            score_text = font.render("YOUR SCORE:" + str(score), True, (0,0,0))
            main_surface.blit(score_text, (100, 200))
            pygame.display.update()
            for event in pygame.event.get():
                # 終了イベント（画面の×ボタン押下など）の場合、
                # ループを抜ける
                if event.type == pygame.QUIT:
                    # 終了処理
                    pygame.quit()
                    sys.exit()



if __name__ == '__main__':
    main()
