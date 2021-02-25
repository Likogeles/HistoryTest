import pygame

from functions import load_image


class SceneSwitchButton(pygame.sprite.Sprite):
    def __init__(self, name, imagename, x, y, *group):
        super().__init__(*group)
        self.not_charge_image = load_image("Buttons/" + imagename + ".png")
        self.image = self.not_charge_image
        self.charge_image = load_image("Buttons/" + imagename + "_charge.png")
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y
        self.name = name

    def click(self, pos):  # Возвращает True если pos находится в области кнопки, иначе возвращает False
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            return True
        return False

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image = self.charge_image
            return
        self.image = self.not_charge_image
