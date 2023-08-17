import pygame

def sound(path):
    pygame.mixer.init() #初期化
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load(path) #読み込み
    # pygame.mixer.music.load("audio\\game_explosion9.mp3") #読み込み
    pygame.mixer.music.play(1) #再生
