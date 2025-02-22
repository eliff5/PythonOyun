import pygame
import random


pygame.init()


GENISLIK = 800
YUKSEKLIK = 600
screen = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Balıkçı Oyunu")


import os
catch_sound = pygame.mixer.Sound("sounds/catch.wav")
wrong_sound = pygame.mixer.Sound("sounds/mixkit-player-jumping-in-a-video-game-2043.wav")
start_sound = pygame.mixer.Sound("sounds/mixkit-winning-a-coin-video-game-2069.wav")


BEYAZ = (255, 255, 255)
MAVI = (0, 0, 255)


class Balik(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tip):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tip = tip


class Balikci(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.can = 3

    def ciz(self):
        screen.blit(self.image, self.rect)


class Oyun:
    def __init__(self):
        self.balikci = Balikci(350, 500, pygame.image.load("images/balikci.png"))
        self.balik_grup = pygame.sprite.Group()
        self.hedef_balik_goruntu = None
        self.balik_liste_index_no = None
        self.yeni_balIk_ekle()
        self.hedef_yenile()
        start_sound.play()

    def yeni_balIk_ekle(self):
        for _ in range(5):
            balik_tip = random.randint(0, 3)
            balik = Balik(random.randint(0, GENISLIK - 32), random.randint(0, YUKSEKLIK - 32), pygame.image.load(f"images/balik1{balik_tip}.png"), balik_tip)
            self.balik_grup.add(balik)

    def hedef_yenile(self):
        if self.balik_grup:
            hedef_balik = random.choice(self.balik_grup.sprites())
            self.hedef_balik_goruntu = hedef_balik.image
            self.balik_liste_index_no = hedef_balik.tip

    def temas(self):
        temas_oldumu = pygame.sprite.spritecollideany(self.balikci, self.balik_grup)
        if temas_oldumu:
            if temas_oldumu.tip == self.balik_liste_index_no:
                catch_sound.play()
                self.balik_grup.remove(temas_oldumu)
                if self.balik_grup:
                    self.hedef_yenile()
                else:
                    self.yeni_balIk_ekle()
                    self.hedef_yenile()
            else:
                wrong_sound.play()
                self.balikci.can -= 1
                if self.balikci.can == 0:
                    print("Game Over!")
                    pygame.quit()
                    exit()

    def ciz(self):
        self.balikci.ciz()
        self.balik_grup.draw(screen)
        if self.hedef_balik_goruntu:
            screen.blit(self.hedef_balik_goruntu, (10, 10))

#Dongu
oyun = Oyun()
clock = pygame.time.Clock()
calisiyor = True
while calisiyor:
    screen.fill(BEYAZ)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calisiyor = False
    
    oyun.temas()
    oyun.ciz()
    pygame.display.update()
    clock.tick(30)

pygame.quit()
