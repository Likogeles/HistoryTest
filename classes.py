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


class Button(pygame.sprite.Sprite):
    def __init__(self, name, imagename, x, y, *group, text='x', answer_id=0):
        super().__init__(*group)
        self.answer_id = answer_id
        self.not_charge_image = load_image("Buttons/" + imagename + ".png")
        self.image = self.not_charge_image
        self.charge_image = load_image("Buttons/" + imagename + "_charge.png")
        self.now_image = False
        self.now = False
        self.charge_lock = False

        if answer_id:
            self.now_image = load_image("Buttons/" + imagename + "_now.png")

        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y

        self.name = name
        self.charge_log = False

        # Работа с текстом
        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 30)
        self.text = text
        self.text_cords = (10, 15)
        if self.text != 'x':
            self.image.blit(self.font.render(self.text, True, (0, 0, 0)), (self.text_cords[0] + 1, self.text_cords[1] + 1))
            self.image.blit(self.font.render(self.text, True, (253, 253, 253)), self.text_cords)

    def click(self, pos):  # Возвращает True если pos находится в области кнопки, иначе возвращает False
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            return self.name
        return False

    def charge_switch(self, pos):
        if self.charge_lock:
            self.image = self.charge_image
        else:
            if not self.now:
                if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                        self.rect.y <= pos[1] <= self.rect.y + self.h:
                    self.image = self.charge_image
                    self.charge_log = True
                else:
                    self.image = self.not_charge_image
                    self.charge_log = False
            else:
                self.image = self.now_image
                self.charge_log = True

        if self.text != 'x':
            if self.charge_log:
                for i in range(-2, 6):
                    self.image.blit(self.font.render(self.text, True,
                                                     (128, 128, 128)), (self.text_cords[0] + i, self.text_cords[1] + i))
                self.image.blit(self.font.render(self.text, True, (0, 0, 0)), (self.text_cords[0] + 1, self.text_cords[1] + 1))
                self.image.blit(self.font.render(self.text, True, (253, 253, 253)), self.text_cords)


class QuestionButton(pygame.sprite.Sprite):
    def __init__(self, id, x, y, w, text, *group):
        super().__init__(*group)

        self.now = False
        self.complete = False
        self.flag = False

        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 17)

        width = (w - 10) / (self.font.size("Wa")[0] / 2)
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
        if self.now:
            self.image.fill(pygame.Color(140, 130, 40))
        else:
            if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                    self.rect.y <= pos[1] <= self.rect.y + self.h:
                self.image.fill(pygame.Color(240, 230, 140))
            else:
                self.image.fill(pygame.Color(180, 180, 180))

        if self.complete:
            pygame.draw.rect(self.image, (0, 0, 255), (0, 0, 10, self.rect.h))
        if self.flag:
            pygame.draw.polygon(self.image, (200, 0, 0),
                                ((self.rect.w - 40, 0), (self.rect.w, 0), (self.rect.w, 40)))
            pygame.draw.line(self.image, (100, 0, 0), (self.rect.w - 41, -1), (self.rect.w + 1, 41), 8)

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


class BigSlider(pygame.sprite.Sprite):
    def __init__(self, x, y, field, *group):
        super().__init__(*group)

        self.field = field
        self.image = pygame.Surface((30, 80))
        self.image.fill(pygame.Color(165, 42, 42))

        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y

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


class QuestionImage(pygame.sprite.Sprite):
    def __init__(self, x, y, w, text, *group, right=-1):
        super().__init__(*group)
        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 17)

        width = (w - 10) / (self.font.size("Wa")[0] / 2)

        self.strings = []
        leng = 0
        string = ""
        for i in text.split():
            if leng + len(i) > width or i == '*':
                self.strings.append(string)
                string = ""
                leng = 0
                if i == '*':
                    continue
            string += i + " "
            leng += len(i) + 1
        if string:
            self.strings.append(string)

        self.image = pygame.Surface((w, len(self.strings) * self.font.size("v")[1] + 10))
        if right == -1:
            self.image.fill(pygame.Color(180, 180, 180))
        elif right:
            self.image.fill(pygame.Color(0, 180, 0))
        else:
            self.image.fill(pygame.Color(180, 0, 0))

        indexplus = 0
        for i in range(len(self.strings)):
            if self.strings[i][:3] == 'А. ':
                indexplus = 10
            if self.strings[i][:3] == 'Б. ':
                indexplus = 20
            self.image.blit(self.font.render(self.strings[i], True, (30, 30, 30)),
                            (18, i * (self.font.size(self.strings[i])[1] - 3) + indexplus + 5))

        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y
        pygame.draw.rect(self.image, (70, 54, 37), (0, 0, self.rect.w, self.rect.h), 3)

    def height(self):
        return self.h
