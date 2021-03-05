import pygame

from classes import SceneSwitchButton as ScSwButton
from classes import QuestionSwitchButton as QtSwButton


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


class Test:
    def __init__(self, test_id):
        self.qtbut_sprites = pygame.sprite.Group()
        self.but_sprites = pygame.sprite.Group()
        self.question_id = 0

        filename = "data/Questions/Topic" + test_id + ".txt"

        self.font = pygame.font.SysFont('verdana', 30)
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            self.questions = [line.strip() for line in TestsTopicsFile]

        x = 0
        y = 0
        for i in range(len(self.questions)):
            if i % 5 == 0:
                x += 1
            if i % 25 == 0:
                y += 1
                x = 0

            QtSwButton(i, 20 + 40 * x, 20 + 50 * (y - 1), self.qtbut_sprites)
            x += 1
        for i in self.qtbut_sprites:
            i.now_logic = True
            break
        self.y = y

    def render(self, screen):
        screen.fill((220, 220, 220))
        self.qtbut_sprites.draw(screen)
        self.but_sprites.draw(screen)
        if self.questions:
            x = self.questions[self.question_id].split()
            y = self.y
            leng = 0
            pixleng = 0
            for i in x:
                if leng + len(i) > 50:
                    y += 1
                    pixleng = 0
                    leng = 0
                screen.blit(self.font.render(i + " ", 1, (30, 30, 30)), (50 + pixleng, 50 + y * 40))
                leng += len(i)
                pixleng += self.font.size(i + " ")[0]

    def click(self, pos):
        for i in self.qtbut_sprites:
            if type(i.click(pos)) == int:
                for j in self.qtbut_sprites:
                    j.now_logic = False
                self.question_id = i.click(pos)
                self.mouse_motion(pos)
                return "x"
        return "x"

    def mouse_motion(self, pos):
        for i in self.qtbut_sprites:
            i.charge_switch(pos)
