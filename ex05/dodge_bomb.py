import pygame as pg
import random
import sys
import time


class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.fight = False # 戦闘モード

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]  
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)            

    # 画像のサイズを変える
    def scale(self, size): #sizeは要素２のタプル(建て,横)
        self.sfc = pg.transform.scale(self.sfc, size)
        self.src = self.sfc.get_rect()
        self.rct.center = 900, 400
        
        
        



class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy
        self.enemy = True #敵かどうか

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)

class Item:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy
        self.used = False #使われたかどうか

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


    

    # (new)こうかとんが爆弾に触れるとGAME OVER と表示させる
    # font = pg.font.Font(None, 200)
    # text = font.render("GAME OVER", True, (255,0,0))
    # scrn_sfc.blit(text, [400, 400])


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    clock =pg.time.Clock()

    # 練習１
    scr = Screen("逃げろ！こうかとん", (1600,900), "fig/pg_bg.jpg")

    # 練習３
    kkt = Bird("fig/6.png", 2.0, (900,400))
    kkt.update(scr)

    # 練習５
    bkd = Bomb((255, 0, 0), 10, (+1, +1), scr)
    bkd.update(scr)
    
    # 爆弾を増やすraise_bomb
    bombs = []
    colors = ["red", "green", "blue", "yellow", "magenta"]

    for i in range(5):
        color = colors[i]
        vx = random.choice([-1, +1])
        vy = random.choice([-1, +1])
        bombs.append(Bomb(color, 10, (vx, vy), scr))

    # 被弾こうかとん
    end_kkt = Bird("fig/bakuhatu.png", 2.0, (900,400))
    # end_kkt.scale((500, 500)) #サイズを変えると、位置がおかしくなってしまう

    # こうかとん強化アイテム生成
    items = []

    for i in range(2):
        color = "white"
        vx = random.choice([-1, +1])
        vy = random.choice([-1, +1])
        items.append(Item(color, 10, (vx, vy), scr))
    

    kkt.update(scr)
    for bomb in bombs:
        bomb.update(scr)
        if kkt.rct.colliderect(bomb.rct):
            return

    # アイテム生成
    for item in items:
        item.update(scr)
        

    # 練習２
    while True:        
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        for bomb in bombs:
            if bomb.enemy is True:
                bomb.update(scr)
            if kkt.rct.colliderect(bomb.rct) and (kkt.fight is False) and (bomb.enemy is True): #こうかとんが非戦闘モードかつ爆弾の敵判定がTrueなら
                # こうかとんが爆弾に触れた位置で画像を切り替える
                end_kkt.rct.centerx = kkt.rct.centerx # こうかとんの位置と等しくする
                end_kkt.rct.centery = kkt.rct.centery
                end_kkt.blit(scr)
                # end_kkt.update(scr)
                pg.display.update()
                time.sleep(3)
                ##
                return
            # こうかとんが敵を倒す
            elif kkt.rct.colliderect(bomb.rct) and (kkt.fight is True): #戦闘モード時に爆弾に触れると
                bomb.enemy = False # 触れたボムの敵判定をなくす（倒した）

        # アイテムを使った時の処理
        for item in items:
            if item.used is False: #　使用済みアイテムならアップデートしない
                item.update(scr)
            if kkt.rct.colliderect(item.rct) and (item.used is False): # kktが未使用アイテムに触れたら
                kkt.fight = True # こうかとん戦闘モードに移行
                item.used = True # そのアイテムは使用済み判定に変わる



        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()