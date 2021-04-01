import pygame
import os

from functions import load_image


class BackgroundImage(pygame.sprite.Sprite):
    def __init__(self, imagename, x, y, *group, color_key=0):
        super().__init__(*group)
        self.image = load_image("Sprites/" + imagename + ".png", color_key)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class SceneSwitchButton(pygame.sprite.Sprite):
    def __init__(self, name, imagename, x, y, *group, text='x'):
        super().__init__(*group)
        self.not_charge_image = load_image("Buttons/" + imagename + ".png")
        self.image = self.not_charge_image
        self.charge_image = load_image("Buttons/" + imagename + "_charge.png")

        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y

        self.name = name
        self.charge_log = False

        # Работа с текстом
        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 30)
        self.text = text
        self.text_cords = (20, 20)
        if self.text != 'x':
            self.image.blit(self.font.render(self.text, True, (253, 253, 253)), self.text_cords)

    def click(self, pos):  # Возвращает True если pos находится в области кнопки, иначе возвращает False
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            return self.name
        return False

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image = self.charge_image
            self.charge_log = True
        else:
            self.image = self.not_charge_image
            self.charge_log = False

        if self.text != 'x':
            if self.charge_log:
                for i in range(-2, 6):
                    self.image.blit(self.font.render(self.text, True,
                                                     (128, 128, 128)), (self.text_cords[0] + i, self.text_cords[1] + i))
                self.image.blit(self.font.render(self.text, True, (253, 253, 253)), self.text_cords)


class QuestionButton(pygame.sprite.Sprite):
    def __init__(self, id, x, y, w, text, *group):
        super().__init__(*group)

        # self.font = pygame.font.SysFont("verdana", 16)

        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 17)

        width = w / (self.font.size("Wa")[0] / 2)
        self.strings = []
        leng = 0
        string = ""
        for i in text.split():
            if leng + len(i) > width:
                self.strings.append(string)
                string = ""
                leng = 0
            string += i + " "
            leng += len(i) + 1
        if string:
            self.strings.append(string)

        self.image = pygame.Surface((w, len(self.strings) * self.font.size("v")[1] + 10))
        self.image.fill(pygame.Color(180, 180, 180))

        self.render_qt()

        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y

        pygame.draw.rect(self.image, (70, 54, 37), (0, 0, self.rect.w, self.rect.h), 3)

        self.id = id

    def height(self):
        return self.h

    def click(self, pos):  # Возвращает свой id если pos находится в области кнопки, иначе возвращает False
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            return self.id
        return False

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image.fill(pygame.Color(240, 230, 140))
        else:
            self.image.fill(pygame.Color(180, 180, 180))
        pygame.draw.rect(self.image, (70, 54, 37), (0, 0, self.rect.w, self.rect.h), 3)

        self.render_qt()

    def render_qt(self):
        for i in range(len(self.strings)):
            self.image.blit(self.font.render(self.strings[i], True, (30, 30, 30)),
                            (18, i * (self.font.size(self.strings[i])[1]) + 5))


class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, field, *group):
        super().__init__(*group)

        self.field = field
        self.image = pygame.Surface((10, 80))
        self.image.fill(pygame.Color(165, 42, 42))

        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y
        self.id = id

        pygame.draw.rect(self.image, (70, 54, 37), (0, 0, self.rect.w, self.rect.h), 3)

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            # self.image.fill(pygame.Color(184, 134, 11))
            self.image.fill(pygame.Color(163, 73, 164))
        else:
            self.image.fill(pygame.Color(165, 42, 42))
        pygame.draw.rect(self.image, (70, 54, 37), (0, 0, self.rect.w, self.rect.h), 3)

    def slide(self, pos, y, mouse_logic):
        if (self.field[0] <= pos[0] <= self.field[0] + self.field[2] and
                self.field[1] <= pos[1] <= self.field[1] + self.field[3]) or mouse_logic:
            if (self.field[1] + 10 == self.rect.y and y > 0) or\
                    (self.field[1] + self.field[3] - 85 == self.rect.y and y < 0):
                return 0
            k = self.rect.y
            if self.field[1] + 10 >= self.rect.y + y * -8:
                self.rect.y = self.field[1] + 10
            elif self.rect.y + y * -8 + self.rect.h >= self.field[1] + self.field[3] - 5:
                self.rect.y = self.field[1] + self.field[3] - 85
            else:
                self.rect.y += y * -8
            k = abs(k - self.rect.y)
            if y > 0:
                k *= -1
            return k

    def click(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            return "slide"

