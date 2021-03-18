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
            return self.name
        return False

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image = self.charge_image
            return
        self.image = self.not_charge_image


class QuestionSwitchButton(pygame.sprite.Sprite):
    def __init__(self, id, x, y, *group):
        super().__init__(*group)
        self.charge_image = load_image("Buttons/questionbut_charge.png")
        self.not_charge_image = load_image("Buttons/questionbut.png")
        self.now_image = load_image("Buttons/questionbut_now.png")
        self.choised_image = load_image("Buttons/questionbut_choised.png")

        self.image = self.not_charge_image
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y
        self.id = id
        self.choise_logic = False

        if id == 0:
            self.now_logic = True
            self.image = self.now_image
        else:
            self.now_logic = False

    def click(self, pos):  # Возвращает свой id если pos находится в области кнопки, иначе возвращает False
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:

            self.now_logic = True

            return self.id
        return False

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image = self.charge_image
        elif self.now_logic:
            self.image = self.now_image
        elif self.choise_logic:
            self.image = self.choised_image
        else:
            self.image = self.not_charge_image

    def choise_switch(self):
        self.image = self.choised_image
        self.choise_logic = True


class QuestionButton(pygame.sprite.Sprite):
    def __init__(self, id, x, y, w, text, *group):
        super().__init__(*group)

        self.text_width = 300

        self.font = pygame.font.SysFont("verdana", 16)

        width = w / self.font.size("0")[0]
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
        self.id = id

    def higth(self):
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

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image.fill(pygame.Color(184, 134, 11))
        else:
            self.image.fill(pygame.Color(165, 42, 42))

    def slide(self, pos, y, mouse_logic):
        if (self.field[0] <= pos[0] <= self.field[0] + self.field[2] and
                self.field[1] <= pos[1] <= self.field[1] + self.field[3]) or mouse_logic:
            if self.field[1] + 5 >= self.rect.y + y * -8:
                self.rect.y = self.field[1] + 10
            elif self.rect.y + y * -8 + self.rect.h >= self.field[1] + self.field[3] - 5:
                self.rect.y = self.field[1] + self.field[3] - 85
            else:
                self.rect.y += y * -8
                return y * -8
        self.charge_switch(pos)

    def click(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            return "slide"


class AnswerSwitchButton(pygame.sprite.Sprite):
    def __init__(self, id, x, y, *group):
        super().__init__(*group)
        self.not_charge_image = load_image("Buttons/answerbut.png", colorkey=True)
        self.charge_image = load_image("Buttons/answerbut_charge.png", colorkey=True)
        self.now_image = load_image("Buttons/answerbut_now.png", colorkey=True)

        self.image = self.not_charge_image
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect.x = x
        self.rect.y = y
        self.id = id

        if id == 0:
            self.now_logic = True
            self.image = self.now_image
        else:
            self.now_logic = False

    def click(self, pos):  # Возвращает свой id если pos находится в области кнопки, иначе возвращает False
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:

            self.now_logic = True

            return self.id
        return False

    def charge_switch(self, pos):
        if self.rect.x <= pos[0] <= self.rect.x + self.w and \
                self.rect.y <= pos[1] <= self.rect.y + self.h:
            self.image = self.charge_image
        elif self.now_logic:
            self.image = self.now_image
        else:
            self.image = self.not_charge_image
