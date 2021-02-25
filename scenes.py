import pygame

from classes import SceneSwitchButton as ScSwButton


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

    def mouseMotion(self, pos):
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

    def mouseMotion(self, pos):
        for i in self.but_sprites:
            i.charge_switch(pos)
