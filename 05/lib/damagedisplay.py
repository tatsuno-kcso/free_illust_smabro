import pygame

class DisplayDamage():
    def __init__(self, screen, x):
        pygame.font.init()
        self.damage_font = pygame.font.Font(None, 100)
        self.damage = 0.0
        self.damage_counter_x = x
        self.screen = screen

    def display_damage(self):
        damage = self.damage_font.render(str(self.damage) + "%", True, (0, 0, 0))
        self.screen.blit(damage, (self.damage_counter_x, 550))
    def add_damage(self, d):
        self.damage += d