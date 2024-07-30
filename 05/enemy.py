import pygame
import pygame.mixer
from enum import Enum
import time
from charactorimage import CharactorImage
from action.enemy_jump import EnemyJump
from lib.textprint import TextPrint
from lib.textprint import draw_input_info
from lib.sound import sound
import random


class BURST_DIRECTION(Enum):
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3

class WINDOW_SIZE():
    WIDTH = 1280
    HIGHT = 720
class JoyStickMock():
    def __init__(self, player_pos):
        self.player_pos = player_pos
        self.axis_0 = random.randint(-100,100)/100
        self.can_move = True
    
    def get_axis(self, axis):
        print("get_axis",self.can_move)
        if not self.can_move:
            return 0
        else:
            if self.player_pos.x < 200:
                self.axis_0 = 1
            elif self.player_pos.x > WINDOW_SIZE.WIDTH - 200:
                self.axis_0 = -1

        return self.axis_0
    
    def set_move(self, true_or_false):
        self.can_move = true_or_false

from dataclasses import dataclass
@dataclass
class EnemyEvent:
    type: int
    instance_id: int
    button: int


class Enemy():
    def __init__(self, x, y, screen, joystick, stage, enemy):
        # self.ci.img = pygame.image.load('05\\img\\business_eigyou_man.png')
        # self.ci.size = 100 * 1
        # self.ci.img = pygame.transform.scale(self.ci.img, (self.ci.size, self.ci.size))
        # self.player_pos = self.ci.img.get_rect()
        # self.player_pos.x = x
        # self.player_pos.y = y
        # self.direction_right = True

        # self.ci.damage_img = pygame.image.load('05\\img\\energy_ha_kurau.png')
        # self.ci.damage_img = pygame.transform.scale(self.ci.damage_img, (self.ci.size, self.ci.size))

        # self.ci.attack_img = pygame.image.load('05\\img\\1414502.png')
        # self.ci.attack_img = pygame.transform.scale(self.ci.attack_img, (self.ci.size, self.ci.size))

        # self.ci.burst_org_img = pygame.image.load('05\\img\\bakuhatsu5.png')
        # self.ci.burst_org_img = pygame.transform.scale(self.ci.burst_org_img, (self.ci.size*3, self.ci.size*10))

        self.ci = CharactorImage(x, y, CharactorImage.ENEMY_IMAGE)
        self.damage_counter_x = x

        self.joystick = JoyStickMock(self.ci.player_pos) # joystick
        self.screen = screen
        self.stage = stage
        self.enemy = enemy
        self.delta = 60/1000

        self.jump_obj = EnemyJump(screen, joystick, stage, self.ci.player_pos)

        
        self.damage_font = pygame.font.Font(None, 100)
        self.damage = 0.0
        self.damage_frame_count = 0


        self.burst_frame_count = 0
        self.burst_direction = None

        # 移動
        

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

        self.after_damage_frame_count = 0

            
    def move_action(self):
        self.ci.player_pos.x += 200 * self.delta * self.joystick.get_axis(0)
        if self.ci.direction_right and self.joystick.get_axis(0) < 0 and self.ci.player_pos.colliderect(self.stage):
            self.ci.img = pygame.transform.flip(self.ci.img, True, False)
            self.ci.attack_img = pygame.transform.flip(self.ci.attack_img, True, False)
            self.ci.direction_right = False
        elif not self.ci.direction_right and self.joystick.get_axis(0) > 0 and self.ci.player_pos.colliderect(self.stage):
            self.ci.img = pygame.transform.flip(self.ci.img, True, False)
            self.ci.attack_img = pygame.transform.flip(self.ci.attack_img, True, False)
            self.ci.direction_right = True

    def burst(self):
        if self.ci.player_pos.y > WINDOW_SIZE.HIGHT and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.BOTTOM
            self.ci.burst_img = self.ci.burst_org_img
            sound("05\\audio\\game_explosion9.mp3")

        if self.ci.player_pos.x < 0 and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.LEFT
            self.ci.burst_img = pygame.transform.rotate(self.ci.burst_org_img, -90)
            sound("05\\audio\\game_explosion9.mp3")

        if self.ci.player_pos.x > WINDOW_SIZE.WIDTH and self.burst_frame_count == 0:
            self.burst_frame_count = 10
            self.burst_direction = BURST_DIRECTION.RIGHT
            self.ci.burst_img = pygame.transform.rotate(self.ci.burst_org_img, 90)
            sound("05\\audio\\game_explosion9.mp3")

        if self.burst_frame_count > 0:
            self.ci.burst_img.set_alpha(255)
            if self.burst_direction == BURST_DIRECTION.BOTTOM:
                self.screen.blit(self.ci.burst_img, (self.ci.player_pos.x, 180))
            elif self.burst_direction == BURST_DIRECTION.LEFT:
                self.screen.blit(self.ci.burst_img, (self.ci.player_pos.x, self.ci.player_pos.y))
            else:
                self.screen.blit(self.ci.burst_img, (self.ci.player_pos.x - self.ci.size*10, self.ci.player_pos.y))
            self.burst_frame_count -= 1
            self.ci.img.set_alpha(0)

        if self.burst_frame_count == 1:
            self.burst_frame_count -= 1
            self.ci.player_pos.x = self.screen.get_width() / 2
            self.ci.player_pos.y = self.screen.get_height() / 4 *3 - 100
            self.damage = 0.0
            self.ci.img.set_alpha(255)
            self.ci.burst_img.set_alpha(0)

    def display_damage(self):
        damage = self.damage_font.render(str(self.damage) + "%", True, (0, 0, 0))
        self.screen.blit(damage, (self.damage_counter_x, 550))

    def hit_action(self):
        if self.damage_frame_count == 5:
            self.damage += 5
            self.kb_x_vel = 3 * self.damage
            self.kb_y_vel = -3 * self.damage
            sound("05\\audio\\Hit08-1.mp3")

        if self.damage_frame_count > 0:
            self.ci.damage_img.set_alpha(255)
            self.ci.img.set_alpha(0)
            self.screen.blit(self.ci.damage_img, (self.ci.player_pos.x, self.ci.player_pos.y))
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
            self.ci.img.set_alpha(255)
            self.ci.damage_img.set_alpha(0)
            self.after_damage_frame_count = 20
            self.joystick.set_move(False)

        if self.after_damage_frame_count > 0:
            self.after_damage_frame_count -= 1
        if self.after_damage_frame_count == 1:
            self.joystick.set_move(True)

    def set_damage_frame_count(self, damage_frame_count, damage_from_left):
        self.damage_frame_count = damage_frame_count
        self.damage_from_left = damage_from_left
        self.joystick.set_move(False)

    def attack_action(self, events):
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.instance_id == 1 and event.button == 0 and self.attack_frame_count == 0:
            # if event == 'ATTACK':
                self.ci.img.set_alpha(0)
                self.attack_frame_count = 10
            
        if self.attack_frame_count > 0:
            self.screen.blit(self.ci.attack_img, self.ci.player_pos)
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
        
        if self.attack_frame_count == 1:
            self.ci.img.set_alpha(255)

    def hit_enemy(self, rect):
        return rect.colliderect(self.enemy.ci.player_pos)

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        rand = random.randint(0,10)
        event = EnemyEvent(pygame.JOYBUTTONDOWN, 1, rand)
        events.append(event)
        event = EnemyEvent(pygame.JOYBUTTONDOWN, 1, rand)
        events.append(event)
        
        self.hit_action()
        self.display_damage()
        if self.joystick:
            self.move_action()
        self.jump_obj.update(events)

        self.attack_action(events)
        self.burst()
        self.screen.blit(self.ci.img, self.ci.player_pos)