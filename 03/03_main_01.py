import pygame
import pygame.mixer
from enum import Enum
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
    pygame.mixer.music.load("audio\\game_explosion9.mp3") #読み込み
    pygame.mixer.music.play(1) #再生

def hit_sound():
    pygame.mixer.init() #初期化
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load("audio\\Hit08-1.mp3") #読み込み
    pygame.mixer.music.play(1) #再生

class BURST_DIRECTION(Enum):
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, stage):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('img\\business_eigyou_man.png')
        self.size = 100 * 1
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.img = pygame.transform.flip(self.img, True, False)
        self.player_pos = self.img.get_rect()
        self.player_pos.x = x
        self.player_pos.y = 718
        self.screen = screen

        self.damage_img = pygame.image.load('img\\energy_ha_kurau.png')
        self.damage_img = pygame.transform.scale(self.damage_img, (self.size, self.size))

        self.damage_font = pygame.font.Font(None, 200)
        self.damage = 0.0
        self.damage_frame_count = 0

        # burst
        self.burst_org_img = pygame.image.load('img\\bakuhatsu5.png')
        self.burst_org_img = pygame.transform.scale(self.burst_org_img, (self.size*3, self.size*10))

        self.burst_img = pygame.image.load('img\\bakuhatsu5.png')
        self.burst_img = pygame.transform.scale(self.burst_img, (self.size*3, self.size*10))
        self.burst_frame_count = 0
        self.burst_direction = None

        self.stage = stage

        # 重力
        self.vel = 0 # y方向の速度
        self.acc = 2 # 重力加速度

        # ふっとび
        self.kb_x_vel = 0
        self.kb_y_vel = 0
        self.kb_x_acc = 1
        self.kb_y_acc = 1
        self.damage_from_left = True
    
    def display_damage(self):
        damage = self.damage_font.render(str(self.damage), True, (0, 0, 0))
        self.screen.blit(damage, (1200, 900))

    def hit_action(self):
        if self.damage_frame_count == 5:
            self.damage += 5
            self.kb_x_vel = 3 * self.damage
            self.kb_y_vel = -3 * self.damage
            hit_sound()

        if self.damage_frame_count > 0:
            self.damage_img.set_alpha(255)
            self.img.set_alpha(0)
            self.screen.blit(self.damage_img, (self.player_pos.x, self.player_pos.y))
            self.damage_frame_count -= 1
            if self.damage_from_left:
                self.kb_x_vel -=self.kb_x_acc
                self.player_pos.x += self.kb_x_vel
            else:
                self.kb_x_vel +=self.kb_x_acc
                self.player_pos.x -= self.kb_x_vel
            # self.kb_y_vel +=self.kb_y_acc
            self.player_pos.y += self.kb_y_vel

        if self.damage_frame_count == 1:
            self.damage_frame_count -= 1
            self.img.set_alpha(255)
            self.damage_img.set_alpha(0)


    def set_damage_frame_count(self, damage_frame_count, damage_from_left):
        self.damage_frame_count = damage_frame_count
        self.damage_from_left = damage_from_left

    def fall_action(self):
        self.vel += self.acc
        self.player_pos.y += self.vel
        if self.player_pos.colliderect(self.stage):
            self.player_pos.y = self.screen.get_height() / 4 * 3 - 100 + 1 #718
            self.vel = 0
            self.jump = False
            self.jump_second = False

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
            self.damage = 0.0
            self.img.set_alpha(255)
            self.burst_img.set_alpha(0)

    def update(self):
        self.hit_action()
        self.display_damage()
        self.fall_action()
        self.burst()
        self.screen.blit(self.img, self.player_pos)

class Player():
    def __init__(self, x, y, screen, joystick, stage, enemy):
        self.img = pygame.image.load('img\\business_eigyou_man.png')
        self.size = 100 * 1
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.player_pos = self.img.get_rect()
        self.player_pos.x = x
        self.player_pos.y = y

        self.joystick = joystick
        self.screen = screen
        self.stage = stage
        self.enemy = enemy

        self.burst_org_img = pygame.image.load('img\\bakuhatsu5.png')
        self.burst_org_img = pygame.transform.scale(self.burst_org_img, (self.size*3, self.size*10))

        self.attack_img = pygame.image.load('img\\1414502.png')
        self.attack_img = pygame.transform.scale(self.attack_img, (self.size, self.size))

        # 移動
        self.direction_right = True

        # ジャンプ
        self.jump = False
        self.ground = self.screen.get_height() / 4 * 3
        self.vel = 0 # y方向の速度
        self.acc = 2 # 重力加速度
        self.jump_second = False

        # burst
        self.burst_frame_count = 0
        self.burst_direction = None

        # 攻撃
        self.attack_frame_count = 0

        self.delta = 60/1000
            
    def move_action(self):
        self.player_pos.x += 300 * self.delta * self.joystick.get_axis(0)
        if self.direction_right and self.joystick.get_axis(0) < 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.attack_img = pygame.transform.flip(self.attack_img, True, False)
            self.direction_right = False
        elif not self.direction_right and self.joystick.get_axis(0) > 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.attack_img = pygame.transform.flip(self.attack_img, True, False)
            self.direction_right = True

    def jump_action(self, events):
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                if not self.jump and self.player_pos.colliderect(self.stage):
                    self.jump = True
                    self.vel = -30
                    print("ジャンプしました")
                elif not self.jump_second:
                    self.jump_second = True
                    self.vel = -30
                    print("二段ジャンプしました")

    def fall_action(self):
        self.vel += self.acc
        self.player_pos.y += self.vel
        if self.player_pos.colliderect(self.stage):
            self.player_pos.y = self.screen.get_height() / 4 * 3 - 100 + 1
            self.vel = 0
            self.jump = False
            self.jump_second = False

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

    def attack_action(self, events):
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0 and self.attack_frame_count == 0:
                self.img.set_alpha(0)
                self.attack_frame_count = 10
            
        if self.attack_frame_count > 0:
            self.screen.blit(self.attack_img, self.player_pos)
            self.attack_frame_count -= 1
            if self.direction_right:
                rect = pygame.Rect(self.player_pos.x+70, self.player_pos.y, 50, 50)
                pygame.draw.rect(self.screen, (255,0,0), rect, 1)
                if self.hit_enemy(rect):
                    self.enemy.set_damage_frame_count(5, True)
            else:
                rect = pygame.Rect(self.player_pos.x-20, self.player_pos.y, 50, 50)
                pygame.draw.rect(self.screen, (255,0,0), rect, 1)
                if self.hit_enemy(rect):
                    self.enemy.set_damage_frame_count(5, False)
        
        if self.attack_frame_count == 1:
            self.img.set_alpha(255)

    def hit_enemy(self, rect):
        return rect.colliderect(self.enemy.player_pos)
    
    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.move_action()
        self.jump_action(events)
        self.attack_action(events)
        self.fall_action()
        self.burst()
        self.screen.blit(self.img, self.player_pos)

#################################################################################
# main関数
#################################################################################
def main():
    screen = pygame.display.set_mode((1920, 1080))
    bg = pygame.image.load("img\\bg_dote.jpg")
    bg = pygame.transform.scale(bg, (1920, 1080))
    
    clock = pygame.time.Clock()
    
    text_print = TextPrint()
    joystick = pygame.joystick.Joystick(0)

    left_side = screen.get_width() / 5
    stage_len = screen.get_width() / 5 * 3
    center = screen.get_width() / 2
    ground = screen.get_height() / 4 * 3

    stage = pygame.Rect(left_side, ground, stage_len, 10)

    enemy = Enemy(
            center+100,
            ground,
            screen,
            stage)

    player = Player(center-100,
                    ground,
                    screen,
                    joystick,
                    stage,
                    enemy)
    done = False
   
    while not done:
        
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, (0,0,0), stage, 0)

        draw_input_info(screen, joystick, text_print)
        
        # 操作キャラクターを更新
        player.update()
        enemy.update()

        # 描画更新
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
