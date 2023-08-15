import pygame

class Move():
    def __init__(self, screen, joystick, stage, player_pos, delta):
        self.img = pygame.image.load('img\\business_eigyou_man.png')
        self.size = 100 * 1
        self.img = pygame.transform.scale(self.img, (self.size, self.size))

        self.player_pos = player_pos
        self.joystick = joystick
        self.screen = screen
        self.stage = stage
        # 移動
        self.direction_right = True
        
        self.delta = delta

    def move_action(self):
        self.player_pos.x += 100 * self.delta * self.joystick.get_axis(0)
        if self.direction_right and self.joystick.get_axis(0) < 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.direction_right = False
        elif not self.direction_right and self.joystick.get_axis(0) > 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.direction_right = True
    
    def update(self):
        self.move_action()