import pygame
import pygame.mixer
from enum import Enum
import time

pygame.init()

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

def draw_input_info(screen, joystick, text_print):
    text_print.reset()
    axes = joystick.get_numaxes()
    text_print.tprint(screen, f"Number of axes: {axes}")
    text_print.indent()

    for i in range(axes):
        axis = joystick.get_axis(i)
        text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
    text_print.unindent()
    buttons = joystick.get_numbuttons()
    text_print.tprint(screen, f"Number of buttons: {buttons}")
    text_print.indent()

    for i in range(buttons):
        button = joystick.get_button(i)
        text_print.tprint(screen, f"Button {i:>2} value: {button}")
    text_print.unindent()

def sound():
    pygame.mixer.init() #初期化
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load("02\\audio\\game_explosion9.mp3") #読み込み
    pygame.mixer.music.play(1) #再生

class BURST_DIRECTION(Enum):
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3


class Player():
    def __init__(self, x, y, screen, joystick, stage):
        self.img = pygame.image.load('02\\img\\business_eigyou_man.png')
        self.size = 100 * 1
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.player_pos = self.img.get_rect()
        self.player_pos.x = x
        self.player_pos.y = y

        self.joystick = joystick
        self.screen = screen
        self.stage = stage

        self.burst_org_img = pygame.image.load('02\\img\\bakuhatsu5.png')
        self.burst_org_img = pygame.transform.scale(self.burst_org_img, (self.size*3, self.size*10))

        # 移動
        self.direction_right = True

        # ジャンプ
        self.jumping = False
        self.ground = self.screen.get_height() / 4 * 3
        self.vel = 0 # y方向の速度
        self.acc = 1 # 重力加速度
        self.jump_second = False
        
        self.before_jump_frame_count = 0
        self.jump_frame_count = None
        self.short_jump_flg = False
        self.VEL_CONST = 15
        self.ACC_CONST = 2

        # burst
        self.burst_frame_count = 0
        self.burst_direction = None

        self.delta = 60/1000
            
    def move_action(self):
        self.player_pos.x += 100 * self.delta * self.joystick.get_axis(0)
        if self.direction_right and self.joystick.get_axis(0) < 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.direction_right = False
        elif not self.direction_right and self.joystick.get_axis(0) > 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.direction_right = True
    
    def jump_input(self, events):
        # print(self.before_jump_frame_count)
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                print("pygame.JOYBUTTONDOWN")
                # flg初期化
                self.short_jump_flg = False
                if not self.jumping and self.player_pos.colliderect(self.stage):
                    self.before_jump_frame_count = 4
                elif not self.jump_second:
                    self.jump_second = True
                    self.jump_frame_count = 0
                    print("二段ジャンプしました")
            # ショートジャンプ入力受付
            if event.type == pygame.JOYBUTTONUP and event.button == 5 and 1 <= self.before_jump_frame_count and self.before_jump_frame_count <= 4:
                self.short_jump_flg = True
                print("pygame.JOYBUTTONUP")
        if self.joystick.get_axis(1) > 0.9 and self.vel > 0:
            self.vel = 1 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
            print("急降下")
        
        # ジャンプ踏切フレーム
        if 1 <= self.before_jump_frame_count:
            self.before_jump_frame_count -= 1
            self.jump_frame_count = 0
            return 
        
        # ジャンプ中フレーム
        if self.jump_frame_count == None:
            return
        self.jump_frame_count+=1
        if self.short_jump_flg:
            self.set_short_jump_param()
        else:
            self.set_jump_param()

    def set_short_jump_param(self):
        if 0 == self.jump_frame_count:
            self.jumping = True
            self.vel = -1.35 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 1 == self.jump_frame_count:
            self.vel = -0.72 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 2 == self.jump_frame_count:
            self.vel = -0.69 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 3 == self.jump_frame_count:
            self.vel = -0.69 * self.VEL_CONST
            self.acc = 0.4 * self.ACC_CONST
        elif 4 <= self.jump_frame_count:
            if 0.6 * self.VEL_CONST < self.vel:
                self.acc = 0

    def set_jump_param(self):
        if 0 == self.jump_frame_count:
            self.jumping = True
            self.vel = -2 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 1 == self.jump_frame_count:
            self.vel = -3 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 2 == self.jump_frame_count:
            self.vel = -2 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 3 == self.jump_frame_count:
            self.vel = -1.6 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 4 == self.jump_frame_count:
            self.vel = -1.05 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 5 == self.jump_frame_count:
            self.vel = -0.75 * self.VEL_CONST
            self.acc = 0.4 * self.ACC_CONST
        elif 6 <= self.jump_frame_count:
            if 0.6 * self.VEL_CONST < self.vel:
                self.acc = 0

    def fall_action(self):
        self.vel += self.acc
        self.player_pos.y += self.vel
        if self.player_pos.colliderect(self.stage):
            self.player_pos.y = self.screen.get_height() / 4 * 3 - 100 + 1
            self.vel = 0
            self.acc = 1
            self.jumping = False
            self.jump_second = False
        if self.vel >= 20:
            self.acc = 0


    def burst(self):
        if self.player_pos.y > 1080 and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.BOTTOM
            self.burst_img = self.burst_org_img
            sound()

        if self.player_pos.x < 0 and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.LEFT
            self.burst_img = pygame.transform.rotate(self.burst_org_img, -90)
            sound()

        if self.player_pos.x > 1920 and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.RIGHT
            self.burst_img = pygame.transform.rotate(self.burst_org_img, 90)
            sound()

        if self.burst_frame_count > 0:
            self.burst_img.set_alpha(255)
            if self.burst_direction == BURST_DIRECTION.BOTTOM:
                self.screen.blit(self.burst_img, (self.player_pos.x, 180))
            elif self.burst_direction == BURST_DIRECTION.LEFT:
                self.screen.blit(self.burst_img, (self.player_pos.x, self.player_pos.y))
            else:
                self.screen.blit(self.burst_img, (self.player_pos.x - self.size*10, self.player_pos.y))
            self.burst_frame_count -= 1
            self.img.set_alpha(0)

        if self.burst_frame_count == 1:
            self.burst_frame_count -= 1
            self.player_pos.x = self.screen.get_width() / 2
            self.player_pos.y = self.screen.get_height() / 4 *3 - 100
            self.img.set_alpha(255)
            self.burst_img.set_alpha(0)

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.move_action()
        self.jump_input(events)
        self.fall_action()
        self.burst()
        self.screen.blit(self.img, self.player_pos)

#################################################################################
# main関数
#################################################################################
def main():
    screen = pygame.display.set_mode((1920, 1080))
    bg = pygame.image.load("02\\img\\bg_dote.jpg")
    bg = pygame.transform.scale(bg, (1920, 1080))
    
    clock = pygame.time.Clock()
    
    text_print = TextPrint()
    joystick = pygame.joystick.Joystick(0)

    left_side = screen.get_width() / 5
    stage_len = screen.get_width() / 5 * 3
    center = screen.get_width() / 2
    ground = screen.get_height() / 4 * 3

    stage = pygame.Rect(left_side, ground, stage_len, 10)

    player = Player(center-100,
                    ground,
                    screen,
                    joystick,
                    stage)
    done = False
   
    while not done:
        
        # screen.blit(bg, (0, 0))
        screen.fill("white")
        pygame.draw.rect(screen, (0,0,0), stage, 0)

        draw_input_info(screen, joystick, text_print)
        
        player.update()
        # 描画更新
        pygame.display.flip()

        # time.sleep(0.2)
        # time.sleep(1)
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
