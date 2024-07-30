import pygame

class CharactorImage():
    PLAYER_IMAGE = 1
    ENEMY_IMAGE = 2
    def __init__(self, x, y, imageType):
        if imageType == CharactorImage.PLAYER_IMAGE:
            self.img = pygame.image.load('05\\img\\business_eigyou_man.png')
            self.size = 100 * 1
            self.img = pygame.transform.scale(self.img, (self.size, self.size))
            self.player_pos = self.img.get_rect()
            self.player_pos.x = x
            self.player_pos.y = y
            self.direction_right = True

            self.default_img = pygame.image.load('05\\img\\business_eigyou_man.png')
            self.default_img = pygame.transform.scale(self.default_img, (self.size, self.size))

            self.damage_img = pygame.image.load('05\\img\\energy_ha_kurau.png')
            self.damage_img = pygame.transform.scale(self.damage_img, (self.size, self.size))

            self.attack_img = pygame.image.load('05\\img\\1414502.png')
            self.attack_img = pygame.transform.scale(self.attack_img, (self.size, self.size))

            self.burst_org_img = pygame.image.load('05\\img\\bakuhatsu5.png')
            self.burst_org_img = pygame.transform.scale(self.burst_org_img, (self.size*3, self.size*10))
        elif imageType == CharactorImage.ENEMY_IMAGE :
            self.img = pygame.image.load('05\\img\\business_eigyou_man.png')
            self.size = 100 * 1
            self.img = pygame.transform.scale(self.img, (self.size, self.size))
            self.player_pos = self.img.get_rect()
            self.player_pos.x = x
            self.player_pos.y = y
            self.direction_right = True

            self.damage_img = pygame.image.load('05\\img\\energy_ha_kurau.png')
            self.damage_img = pygame.transform.scale(self.damage_img, (self.size, self.size))

            self.attack_img = pygame.image.load('05\\img\\1414502.png')
            self.attack_img = pygame.transform.scale(self.attack_img, (self.size, self.size))

            self.burst_org_img = pygame.image.load('05\\img\\bakuhatsu5.png')
            self.burst_org_img = pygame.transform.scale(self.burst_org_img, (self.size*3, self.size*10))

    def set_default_img(self):
        if self.direction_right:
            self.img = self.default_img
        else:
            self.img = pygame.transform.flip(self.default_img, True, False)
