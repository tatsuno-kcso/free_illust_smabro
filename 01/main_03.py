import pygame

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

class Player():
    def __init__(self, x, y, screen, joystick):
        self.img = pygame.image.load('business_eigyou_man.png')
        self.size = 100 * 1
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.player_pos = self.img.get_rect()
        self.player_pos.x = x
        self.player_pos.y = y

        self.joystick = joystick
        self.screen = screen

        # 移動
        self.direction_right = True

        self.delta = 60/1000
            
    def move_action(self):
        self.player_pos.x += 900 * self.delta * self.joystick.get_axis(0)
        if self.direction_right and self.joystick.get_axis(0) < 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.direction_right = False
        elif not self.direction_right and self.joystick.get_axis(0) > 0:
            self.img = pygame.transform.flip(self.img, True, False)
            self.direction_right = True


    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        self.move_action()
        self.screen.blit(self.img, self.player_pos)

#################################################################################
# main関数
#################################################################################
def main():
    screen = pygame.display.set_mode((1920, 1080))
    bg = pygame.image.load("bg_dote.jpg")
    bg = pygame.transform.scale(bg, (1920, 1080))
    
    clock = pygame.time.Clock()
    
    text_print = TextPrint()
    joystick = pygame.joystick.Joystick(0)

    center = screen.get_width() / 2
    ground = screen.get_height() / 4 * 3

    player = Player(center-100,
                    ground,
                    screen,
                    joystick)
    done = False
   
    while not done:
        
        screen.blit(bg, (0, 0))

        draw_input_info(screen, joystick, text_print)
        
        player.update()
        # 描画更新
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
