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

    done = False
   
    while not done:
        
        screen.blit(bg, (0, 0))

        draw_input_info(screen, joystick, text_print)
        pygame.event.get()
        # 描画更新
        pygame.display.flip()

        clock.tick(30) / 1000


if __name__ == "__main__":
    main()
    pygame.quit()
