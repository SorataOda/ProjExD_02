import random
import sys
import pygame as pg



WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_RIGHT:(+5,0),
    pg.K_LEFT:(-5,0)
}
def check_bound(rect:pg.Rect) -> tuple[bool,bool]:
    """
    こうかとんRectと爆弾Rectが画面外 or 画面内かを判定する関数
    引数：こうかとんRectか爆弾Rect
    戻り値:横方向・縦方向の真理値タプル
    """
    yoko,tate = True,True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_rot = {
        (0, 0): kk_img,
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 1),
        (5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1),
        (5, 0): pg.transform.flip(kk_img, True, False),
        (5, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1),
        (0, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90, 1),
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1),
        (-5, 0): kk_img,
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1)
    }
    kk_rect = kk_img.get_rect() #練習３
    kk_rect.center = 900,400
    bd_img = pg.Surface((20,20))  #練習１
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    bd_rect = bd_img.get_rect()
    #爆弾rectの中心座標を乱数指定する
    bd_rect.center = x,y 
    

    clock = pg.time.Clock()
    tmr = 0
    vx,vy = +5,+5 #練習２

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if kk_rect.colliderect(bd_rect):  # 練習５
                print("ゲームオーバー")
                return   # ゲームオーバー 
        key_list = pg.key.get_pressed()#練習３
        sum_mv = [0,0]
        for k, mv in delta.items():
            if key_list[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        sum_mv_tuple = tuple(sum_mv)
        kk_rot_img = kk_rot[sum_mv_tuple]

        kk_rect.move_ip(sum_mv)
        if check_bound(kk_rect) != (True,True):
            kk_rect.move_ip(-sum_mv[0],-sum_mv[1])
        print(sum_mv)

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_rot_img, kk_rect)
        bd_rect.move_ip(vx,vy) #練習２
        yoko,tate = check_bound(bd_rect)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bd_img,bd_rect)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()