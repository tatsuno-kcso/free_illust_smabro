import pygame
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
        
