import pygame
import pygame.mixer
from enum import Enum
import time
from charactorimage import CharactorImage
from action.jump import Jump
from action.move import Move
from lib.textprint import TextPrint
from lib.textprint import draw_input_info
from lib.sound import sound
from enemy import Enemy
from lib.damagedisplay import DisplayDamage

pygame.init()

class BURST_DIRECTION(Enum):
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3
class WINDOW_SIZE():
    WIDTH = 1280
    HIGHT = 720

class Player():
    def __init__(self, x, y, screen, joystick, stage, enemy):
        self.size = 100 * 1
        self.ci = CharactorImage(x, y, CharactorImage.PLAYER_IMAGE)

        self.joystick = joystick
        self.joystickid = joystick.get_instance_id()
        self.screen = screen
        self.stage = stage
        self.enemy = enemy
        self.delta = 60/1000

        
        self.jump_obj = Jump(screen, joystick, stage, self.ci)
        self.move_obj = Move(screen, joystick, stage, self.ci, self.delta)
        self.display_damage = DisplayDamage(screen, x)

        self.damage_frame_count = 0

        self.burst_frame_count = 0
        self.burst_direction = None

        # 移動
        self.direction_right = True

        # burst
        self.burst_frame_count = 0
        self.burst_direction = None

        # 攻撃
        self.attack_frame_count = 0

        # ふっとび
        self.kb_x_vel = 0
        self.kb_y_vel = 0
        self.kb_x_acc = 1
        self.kb_y_acc = 1
        self.damage_from_left = True

    def burst(self):
        if self.ci.player_pos.y > WINDOW_SIZE.HIGHT and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.BOTTOM
            self.burst_img = self.ci.burst_org_img
            sound("05\\audio\\game_explosion9.mp3")

        if self.ci.player_pos.x < 0 and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.LEFT
            self.burst_img = pygame.transform.rotate(self.ci.burst_org_img, -90)
            sound("05\\audio\\game_explosion9.mp3")

        if self.ci.player_pos.x > WINDOW_SIZE.WIDTH and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.RIGHT
            self.burst_img = pygame.transform.rotate(self.ci.burst_org_img, 90)
            sound("05\\audio\\game_explosion9.mp3")

        if self.burst_frame_count > 0:
            self.burst_img.set_alpha(255)
            if self.burst_direction == BURST_DIRECTION.BOTTOM:
                self.screen.blit(self.burst_img, (self.ci.player_pos.x, 180))
            elif self.burst_direction == BURST_DIRECTION.LEFT:
                self.screen.blit(self.burst_img, (self.ci.player_pos.x, self.ci.player_pos.y))
            else:
                self.screen.blit(self.burst_img, (self.ci.player_pos.x - self.size*10, self.ci.player_pos.y))
            self.burst_frame_count -= 1
            self.ci.img.set_alpha(0)

        if self.burst_frame_count == 1:
            self.burst_frame_count -= 1
            self.ci.player_pos.x = self.screen.get_width() / 2
            self.ci.player_pos.y = self.screen.get_height() / 4 *3 - 100
            self.display_damage.damage = 0.0
            self.ci.img.set_alpha(255)
            self.burst_img.set_alpha(0)

    def hit_action(self):
        if self.damage_frame_count == 5:
            self.display_damage.add_damage(5)
            self.kb_x_vel = 3 * self.display_damage.damage
            self.kb_y_vel = -3 * self.display_damage.damage
            sound("05\\audio\\Hit08-1.mp3")

        if self.damage_frame_count > 0:
            self.ci.img = self.ci.damage_img
            self.damage_frame_count -= 1
            if self.damage_from_left:
                self.kb_x_vel -=self.kb_x_acc
                self.ci.player_pos.x += self.kb_x_vel
            else:
                self.kb_x_vel +=self.kb_x_acc
                self.ci.player_pos.x -= self.kb_x_vel
            # self.kb_y_vel +=self.kb_y_acc
            self.ci.player_pos.y += self.kb_y_vel

        if self.damage_frame_count == 1:
            self.damage_frame_count -= 1
            self.ci.set_default_img()

    def set_damage_frame_count(self, damage_frame_count, damage_from_left):
        self.damage_frame_count = damage_frame_count
        self.damage_from_left = damage_from_left

    def attack_action(self, events):
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.instance_id == self.joystickid:
                    if event.button == 0 and self.attack_frame_count == 0:
                        self.ci.img = self.ci.attack_img
                        self.attack_frame_count = 10
            
        if self.attack_frame_count > 0:
            self.attack_frame_count -= 1
            if self.ci.direction_right:
                rect = pygame.Rect(self.ci.player_pos.x+70, self.ci.player_pos.y, 50, 50)
                pygame.draw.rect(self.screen, (255,0,0), rect, 1)
                if self.hit_enemy(rect):
                    self.enemy.set_damage_frame_count(5, True)
            else:
                rect = pygame.Rect(self.ci.player_pos.x-20, self.ci.player_pos.y, 50, 50)
                pygame.draw.rect(self.screen, (255,0,0), rect, 1)
                if self.hit_enemy(rect):
                    self.enemy.set_damage_frame_count(5, False)
        
        if self.attack_frame_count <= 1:
            self.ci.set_default_img()

    def hit_enemy(self, rect):
        return rect.colliderect(self.enemy.ci.player_pos)

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.hit_action()
        self.display_damage.display_damage()
        if self.joystick:
            self.move_obj.update()
        self.jump_obj.update(events)
        self.attack_action(events)
        self.burst()
        self.screen.blit(self.ci.img, self.ci.player_pos)

#################################################################################
# main関数
#################################################################################
def main():
    screen = pygame.display.set_mode((WINDOW_SIZE.WIDTH, WINDOW_SIZE.HIGHT))
    bg = pygame.image.load("05\\img\\bg_dote.jpg")
    bg = pygame.transform.scale(bg, (WINDOW_SIZE.WIDTH, WINDOW_SIZE.HIGHT))
    
    clock = pygame.time.Clock()
    
    text_print = TextPrint()
    if pygame.joystick.get_count() >= 1 :
        joystick = pygame.joystick.Joystick(0)
    if pygame.joystick.get_count() >= 2 :
        joystick2 = pygame.joystick.Joystick(1)

    left_side = screen.get_width() / 5
    stage_len = screen.get_width() / 5 * 3
    center = screen.get_width() / 2
    ground = screen.get_height() / 4 * 3

    stage = pygame.Rect(left_side, ground, stage_len, 10)

    
    # enemy = Enemy(center+200,
    #                     ground,
    #                     screen,
    #                     None,
    #                     stage,
    #                     None)
    player = Player(center - 200,
                    ground,
                    screen,
                    joystick,
                    stage,
                    None)
    player2 = Player(center + 200,
                    ground,
                    screen,
                    joystick2,
                    stage,
                    player)
    player.enemy = player2
    # enemy.enemy = player
    done = False
   
    while not done:
        
        screen.blit(bg, (0, 0))
        # screen.fill("white")
        pygame.draw.rect(screen, (0,0,0), stage, 0)

        draw_input_info(screen, joystick, text_print)
        events = pygame.event.get()
        
        player.update(events)
        player2.update(events)
        # enemy.update([])
        # 描画更新
        pygame.display.flip()

        # time.sleep(0.2)
        # time.sleep(1)
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
