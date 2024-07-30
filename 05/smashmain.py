import pygame
from lib.textprint import TextPrint

class WINDOW_SIZE():
    WIDTH = 1280
    HIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE.WIDTH, WINDOW_SIZE.HIGHT))
bg = pygame.image.load("05\\img\\bg_dote.jpg")
bg = pygame.transform.scale(bg, (WINDOW_SIZE.WIDTH, WINDOW_SIZE.HIGHT))
clock = pygame.time.Clock()
text_print = TextPrint()
left_side = screen.get_width() / 5
stage_len = screen.get_width() / 5 * 3
center = screen.get_width() / 2
ground = screen.get_height() / 4 * 3
stage = pygame.Rect(0, ground, WINDOW_SIZE.WIDTH, 10)

class Player() :
    def __init__(self, x, y, screen, joystick, stage, speed, enemy) :
        # 画像と大きさ
        self.size = 100 * 1 # 大きさ
        self.img = pygame.image.load('05\\img\\business_eigyou_man.png')
        self.img = pygame.transform.scale(self.img, (self.size, self.size)) # 大きさ調整
        self.direction_right = True # 右向き
        # 描画する場所(座標)
        self.player_pos = self.img.get_rect()
        self.player_pos.x = x
        self.player_pos.y = y - self.size
        # 操作するコントローラー情報
        self.joystick = joystick
        self.joystickid = joystick.get_instance_id()
        # スピード
        self.speed = speed / 1000 # 標準は60 / 1000
        # 画面やステージ情報も持たせておく
        self.screen = screen
        self.stage = stage

        self.enemy = enemy
        

def main():
    # コントローラーを認識
    if pygame.joystick.get_count() >= 1 :
        joy1 = pygame.joystick.Joystick(0)
    if pygame.joystick.get_count() >= 2 :
        joy2 = pygame.joystick.Joystick(1)
    # プレイヤーを生成
    p1 = Player(center, ground, screen, joy1, stage, 60, None)
    jumping = False
    jumpframe = 0
    # ゲームのメイン処理ループ
    while True: 
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, (0xFF,0,0), stage, 0)

        # イベントを処理する
        for event in pygame.event.get() :
            # ゲーム終了処理
            if event.type == pygame.QUIT:
                pygame.quit()
            # ジャンプボタン
            if event.type == pygame.JOYBUTTONDOWN \
                and event.button == 5 \
                and p1.joystickid == event.instance_id:
                jumping = True

        # 移動＆ジャンプ
        p1.player_pos.x += 200 * p1.speed * p1.joystick.get_axis(0)
        if jumping :
            jumpframe += 1
            if jumpframe <= 10 :
                p1.player_pos.y -= 10
            elif jumpframe <= 20 :
                p1.player_pos.y += 10
                if jumpframe >= 20 :
                    jumpframe = 0
                    jumping = False
        # プレイヤー描画
        screen.blit(p1.img, p1.player_pos)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()

