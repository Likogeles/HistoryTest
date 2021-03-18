import pygame

from classes import SceneSwitchButton as ScSwButton
from classes import QuestionSwitchButton as QtSwButton
from classes import QuestionButton as QtButton
from classes import AnswerSwitchButton as AnSwButton
from classes import Slider


class Menu:
    def __init__(self):
        self.but_sprites = pygame.sprite.Group()
        ScSwButton("tests", "testsbut", 336, 360, self.but_sprites)

    def render(self, screen):
        screen.fill((220, 220, 220))
        self.but_sprites.draw(screen)

    def click(self, pos):
        for i in self.but_sprites:
            if i.click(pos):
                return i.name
        return "menu"

    def mouse_motion(self, pos):
        for i in self.but_sprites:
            i.charge_switch(pos)


class TestsList:
    def __init__(self):
        self.but_sprites = pygame.sprite.Group()

        filename = "data/TestTopics/TestsTopics.txt"

        self.font = pygame.font.Font(None, 30)

        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            self.TestsTopics = [line.strip() for line in TestsTopicsFile]

        for i in range(len(self.TestsTopics)):
            ScSwButton("topic" + str(i), "topicbut", 80, 70 * i + 150, self.but_sprites)
        ScSwButton("menu", "menubut", 80, 80, self.but_sprites)

    def render(self, screen):
        screen.fill((220, 220, 220))
        self.but_sprites.draw(screen)
        if self.TestsTopics:
            for i in range(len(self.TestsTopics)):
                screen.blit(self.font.render(self.TestsTopics[i], 1,
                                             (0, 0, 0)), (100, 70 * i + 170))

    def click(self, pos):
        for i in self.but_sprites:
            if i.click(pos):
                return i.name
        return "tests"

    def mouse_motion(self, pos):
        for i in self.but_sprites:
            i.charge_switch(pos)


class Test1:
    def __init__(self, test_id):
        self.qtbut_sprites = pygame.sprite.Group()
        self.anbut_sprites = pygame.sprite.Group()
        self.but_sprites = pygame.sprite.Group()
        self.question_id = 0
        self.y1 = 23

        ScSwButton("tests", "backbut", 20, 20, self.but_sprites)

        filename = "data/Questions/Topic" + test_id + ".txt"

        self.font = pygame.font.SysFont('verdana', 30)
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            self.questions = [line.strip() for line in TestsTopicsFile]

        self.answers = []
        self.nums_of_right_answers = []
        self.nums_of_selected_answers = [0 for i in range(len(self.questions))]
        for i in range(len(self.questions)):
            self.answers.append(self.questions[i].split("&")[1:5])
            self.nums_of_right_answers.append(self.questions[i].split("&")[-1])
            self.questions[i] = str(i + 1) + ") " + self.questions[i].split("&")[0]

        x = 0
        y = 1
        for i in range(len(self.questions)):
            if i % 5 == 0:
                x += 1
            if i % 25 == 0:
                y += 1
                x = 0

            QtSwButton(i, 20 + 40 * x, self.y1 + 50 * (y - 1), self.qtbut_sprites)
            x += 1

        self.y = y

        AnSwButton(1, 40, self.y1 + 50 * y, self.anbut_sprites)
        AnSwButton(2, 40, self.y1 + 50 * (y + 1), self.anbut_sprites)
        AnSwButton(3, 40, self.y1 + 50 * (y + 2), self.anbut_sprites)
        AnSwButton(4, 40, self.y1 + 50 * (y + 3), self.anbut_sprites)

    def render(self, screen):
        screen.fill((220, 220, 220))
        self.qtbut_sprites.draw(screen)
        self.but_sprites.draw(screen)
        if not self.questions:
            return

        # Прорисовка вопроса
        x = self.questions[self.question_id].split()
        y = self.y
        leng = 0
        pixleng = 0
        for i in x:
            if leng + len(i) > 50:
                y += 1
                pixleng = 0
                leng = 0
            screen.blit(self.font.render(i + " ", 1, (30, 30, 30)), (50 + pixleng, self.y1 + 40 + y * 40))
            leng += len(i)
            pixleng += self.font.size(i + " ")[0]

        # Прорисовка вариантов ответа, кнопок выбора ответа и редактирование координат кнопок выбора ответа

        y += 1
        k = 0
        for i in self.anbut_sprites:
            y += 1
            x = self.answers[self.question_id][k]
            leng = 0
            pixleng = 0
            i.rect.y = self.y1 + 25 + y * 40
            for j in x.split():
                if leng + len(j) > 50:
                    y += 1
                    pixleng = 0
                    leng = 0
                screen.blit(self.font.render(j + " ", 1, (30, 30, 30)), (90 + pixleng, self.y1 + 20 + y * 40))

                leng += len(j)
                pixleng += self.font.size(j + " ")[0]
            k += 1

        self.anbut_sprites.draw(screen)

    def click(self, pos):
        for i in self.but_sprites:
            if i.click(pos):
                return i.name

        for i in self.qtbut_sprites:
            if type(i.click(pos)) == int:
                for j in self.qtbut_sprites:
                    j.now_logic = False
                self.question_id = i.click(pos)
                for j in self.anbut_sprites:
                    if j.id != self.nums_of_selected_answers[self.question_id]:
                        j.now_logic = False
                    else:
                        j.now_logic = True
                self.mouse_motion(pos)
                return "x"

        for i in self.anbut_sprites:
            temp = i.click(pos)
            if type(temp) == int:
                for j in self.anbut_sprites:
                    j.now_logic = False
                self.nums_of_selected_answers[self.question_id] = i.click(pos)
                for j in self.qtbut_sprites:
                    if j.id == self.question_id:
                        j.choise_switch()
                        break

                self.mouse_motion(pos)
                return "x"
        return "x"

    def mouse_motion(self, pos):
        for i in self.qtbut_sprites:
            i.charge_switch(pos)
        for i in self.anbut_sprites:
            i.charge_switch(pos)
        for i in self.but_sprites:
            i.charge_switch(pos)


class Test:
    def __init__(self, test_id):
        self.qtbut_sprites = pygame.sprite.Group()
        self.anbut_sprites = pygame.sprite.Group()
        self.but_sprites = pygame.sprite.Group()
        self.all_but_sprites = pygame.sprite.Group()
        self.slider_sprite = pygame.sprite.Group()
        self.question_id = 0
        self.questions_list_y = 75

        ScSwButton("tests", "backbut", 20, 10, self.but_sprites, self.all_but_sprites)

        self.slider = Slider(335, 75, (20, 65, 330, 642), self.slider_sprite, self.all_but_sprites)
        self.slider_logic = False
        self.slider_mouse_pos_y = 0

        filename = "data/Questions/Topic" + test_id + ".txt"

        self.font = pygame.font.SysFont('verdana', 16)
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            self.questions = [line.strip() for line in TestsTopicsFile]

        self.answers = []
        self.nums_of_right_answers = []
        self.nums_of_selected_answers = [0 for i in range(len(self.questions))]
        for i in range(len(self.questions)):
            self.answers.append(self.questions[i].split("&")[1:5])
            self.nums_of_right_answers.append(self.questions[i].split("&")[-1])
            self.questions[i] = str(i + 1) + ") " + self.questions[i].split("&")[0]

        for i in range(len(self.questions)):
            k = QtButton(i, 30, self.questions_list_y, 300, self.questions[i], self.qtbut_sprites, self.all_but_sprites)
            self.questions_list_y += k.higth() + 5

    def render(self, screen):
        screen.fill((220, 220, 220))
        self.all_but_sprites.draw(screen)
        pygame.draw.rect(screen, (220, 220, 220), (20, 714, 330, 5), 5)
        pygame.draw.rect(screen, (100, 100, 100), (20, 65, 330, 645), 5)

    def click(self, pos):
        for i in self.all_but_sprites:
            x = i.click(pos)
            if type(x) == int:
                self.question_id = x
            elif x == "slide":
                self.slider_logic = True
            elif x:
                return x
        return "x"

    def anti_click(self, pos):
        self.slider_logic = False

    def mouse_motion(self, pos):
        for i in self.all_but_sprites:
            i.charge_switch(pos)

        if self.slider_logic:
            self.slide(pos, -(pos[1] - self.slider_mouse_pos_y) * 0.125, True)
        self.slider_mouse_pos_y = pos[1]

    def slide(self, pos, y, mouse_logic):
        x = self.slider.slide(pos, y, mouse_logic)
        if x:
            self.questions_list_y += x
