import pygame

class Move():
    def __init__(self, screen, joystick, stage, ci, delta):
        self.ci = ci
        self.player_pos = self.ci.player_pos
        self.joystick = joystick
        self.joystickid = joystick.get_instance_id()
        self.screen = screen
        self.stage = stage
        # 移動
        self.direction_right = True
        
        self.delta = delta

    def move_action(self):
        self.player_pos.x += 200 * self.delta * self.joystick.get_axis(0) 
        if self.ci.direction_right and self.joystick.get_axis(0) < 0 and self.ci.player_pos.colliderect(self.stage):
            self.ci.img = pygame.transform.flip(self.ci.img, True, False)
            self.ci.attack_img = pygame.transform.flip(self.ci.attack_img, True, False)
            self.ci.direction_right = False
        elif not self.ci.direction_right and self.joystick.get_axis(0) > 0 and self.ci.player_pos.colliderect(self.stage):
            self.ci.img = pygame.transform.flip(self.ci.img, True, False)
            self.ci.attack_img = pygame.transform.flip(self.ci.attack_img, True, False)
            self.ci.direction_right = True
    
    def update(self):
        self.move_action()