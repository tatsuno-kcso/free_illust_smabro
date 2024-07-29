import pygame

pygame.init()


#################################################################################
# main関数
#################################################################################
def main():
    screen = pygame.display.set_mode((1920, 1080))
    bg = pygame.image.load("01\\img\\bg_dote.jpg")
    bg = pygame.transform.scale(bg, (1920, 1080))
    
    clock = pygame.time.Clock()
    
    done = False
   
    while not done:
        
        screen.blit(bg, (0, 0))

        # 描画更新
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
