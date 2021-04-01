import pygame
from classes import BackgroundImage
from classes import Button
from classes import QuestionButton as QtButton
from classes import Slider


class Menu:
    def __init__(self):
        self.but_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        BackgroundImage("background", 0, 0, self.background_sprites)
        BackgroundImage("welcome_menu", 0, 0, self.background_sprites)
        Button("tests", "testsbut", 423, 500, self.but_sprites)

    def render(self, screen, background_color):
        screen.fill(background_color)
        self.background_sprites.draw(screen)
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
        self.background_sprites = pygame.sprite.Group()

        filename = "data/TestTopics/TestsTopics.txt"
        BackgroundImage("background", 0, 0, self.background_sprites)
        BackgroundImage("topiclist", 271, 10, self.background_sprites)

        self.font = pygame.font.Font(None, 30)

        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            self.TestsTopics = [line.strip() for line in TestsTopicsFile]

        for i in range(len(self.TestsTopics)):
            Button("topic" + str(i), "topicbut", 20, 85 * i + 150, self.but_sprites, text=self.TestsTopics[i])
        Button("menu", "backbut", 20, 10, self.but_sprites)

    def render(self, screen, background_color):
        screen.fill(background_color)
        self.background_sprites.draw(screen)
        self.but_sprites.draw(screen)

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
        self.all_but_sprites = pygame.sprite.Group()
        self.prev_but_sprite = pygame.sprite.Group()
        self.next_but_sprite = pygame.sprite.Group()

        self.slider_sprite = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.dummy_sprites = pygame.sprite.Group()
        self.question_id = 0
        self.questions_list_y = 100

        Button("tests", "backbut", 20, 10, self.but_sprites, self.all_but_sprites)
        self.prev_but = Button("prev", "prevquestion", 410, 629, self.prev_but_sprite, self.all_but_sprites)
        Button("tests", "finish", 690, 629, self.but_sprites, self.all_but_sprites)
        self.next_but = Button("next", "nextquestion", 970, 629, self.next_but_sprite, self.all_but_sprites)

        BackgroundImage("background", 0, 0, self.background_sprites)
        BackgroundImage("question", 410, 13, self.background_sprites)
        BackgroundImage("slider", 20, 90, self.background_sprites)
        BackgroundImage("dummy0", 0, 0, self.dummy_sprites)
        BackgroundImage("dummy1", 0, 686, self.dummy_sprites)
        BackgroundImage("timer", 117, 10, self.dummy_sprites)

        self.font = pygame.font.SysFont('verdana', 20)

        # Работа с файлом старая
        #
        # filename = "data/Questions/Topic" + test_id + ".txt"
        # with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
        #     self.questions = [line.strip() for line in TestsTopicsFile]
        # self.answers = []
        # self.nums_of_right_answers = []
        # self.nums_of_selected_answers = [0 for i in range(len(self.questions))]
        # for i in range(len(self.questions)):
        #     self.answers.append(self.questions[i].split("&")[1:5])
        #     self.nums_of_right_answers.append(self.questions[i].split("&")[-1])
        #     self.questions[i] = str(i + 1) + ") " + self.questions[i].split("&")[0]

        # Работа с файлом новая

        filename = "data/Questions/topic" + test_id + ".txt"
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            file_lines = [line.strip() for line in TestsTopicsFile]

        self.answers = []
        self.questions = []
        self.nums_of_right_answers = []
        self.nums_of_selected_answers = [0 for i in range(len(file_lines))]
        k = 0
        for i in range(len(file_lines)):
            if k == 0:
                self.questions.append(str(len(self.questions) + 1) + ") " + file_lines[i])
            elif k == 1 or k == 2 or k == 3 or k == 4:
                self.answers.append(file_lines[i])
            elif k == 5:
                self.nums_of_right_answers.append(file_lines[i].split("&")[-1])
            k += 1
            if k > 5:
                k = 0

        # Создание кнопок списка вопросов

        self.questions_buts = []
        for i in range(len(self.questions)):
            k = QtButton(i, 30, self.questions_list_y, 345, self.questions[i], self.qtbut_sprites, self.all_but_sprites)
            self.questions_buts.append(k)
            self.questions_list_y += k.height() + 5
        self.questions_buts[0].now = True
        self.questions_buts[0].charge_switch((0, 0))
        # Работа со слайдером

        # self.k_of_slide = int((self.questions_list_y - 100) / (596 - 70))

        self.k_of_slide = int((self.questions_list_y - 100) / (590 - 70))

        self.slider = 0
        if self.questions_list_y > 700:
            self.slider = Slider(380, 100, (20, 90, 375, 594), self.slider_sprite, self.all_but_sprites)
            self.slider_logic = False
            self.slider_mouse_pos_y = 0

        # Генерация строк каждого вопроса для корректного отображения на странице

        self.strings = []

        width = 1100 / (self.font.size("Wa")[0] / 2)  # Кол-во символов, выделенных на ширину вопроса

        for k in range(len(self.questions)):
            string = ""
            leng = 0
            for i in self.questions[k].split():
                if leng + len(i) > width:
                    self.strings.append([])
                    self.strings[k].append(string)
                    string = ""
                    leng = 0
                string += i + " "
                leng += len(i) + 1
            self.strings.append([])
            self.strings[k].append(string)

    def render(self, screen, background_color):
        screen.fill(background_color)
        self.background_sprites.draw(screen)

        # Отрисовка списка вопросов
        self.qtbut_sprites.draw(screen)
        pygame.draw.rect(screen, (70, 54, 37), (20, 91, 375, 594), 3)

        # Отрисовка заглушек для списка вопросов
        self.dummy_sprites.draw(screen)

        # Отрисовка экрана и кнопок
        if self.question_id > 0:
            self.prev_but_sprite.draw(screen)
        if self.question_id < len(self.questions) - 1:
            self.next_but_sprite.draw(screen)

        self.but_sprites.draw(screen)
        self.slider_sprite.draw(screen)

        # Отрисовка вопроса

        strings_y = 30
        for i in self.strings[self.question_id]:
            screen.blit(self.font.render(i, True, (0, 0, 0)), (430, strings_y))
            strings_y += self.font.size(i)[1]

    def click(self, pos):

        for i in self.all_but_sprites:
            x = i.click(pos)
            if type(x) == int:
                self.questions_buts[self.question_id].now = False
                self.questions_buts[self.question_id].charge_switch(pos)
                self.question_id = x
                self.questions_buts[self.question_id].now = True
                self.questions_buts[self.question_id].charge_switch(pos)
            elif x == "slide":
                self.slider_logic = True
            elif x == "prev":
                if self.question_id > 0:
                    self.questions_buts[self.question_id].now = False
                    self.questions_buts[self.question_id].charge_switch(pos)
                    self.question_id -= 1
                    self.questions_buts[self.question_id].now = True
                    self.questions_buts[self.question_id].charge_switch(pos)
            elif x == "next":
                if self.question_id < len(self.questions) - 1:
                    self.questions_buts[self.question_id].now = False
                    self.questions_buts[self.question_id].charge_switch(pos)
                    self.question_id += 1
                    self.questions_buts[self.question_id].now = True
                    self.questions_buts[self.question_id].charge_switch(pos)
            elif x:
                return x
        return "x"

    def anti_click(self):
        self.slider_logic = False

    def mouse_motion(self, pos):
        if self.slider_logic:
            self.slide(pos, -(pos[1] - self.slider_mouse_pos_y) * 0.125, True)
        for i in self.all_but_sprites:
            i.charge_switch(pos)
        self.slider_mouse_pos_y = pos[1]

    def slide(self, pos, y, mouse_logic):
        if self.slider:
            x = self.slider.slide(pos, y, mouse_logic)
            if x:
                for i in self.qtbut_sprites:
                    i.rect.y -= x * self.k_of_slide
        for i in self.all_but_sprites:
            i.charge_switch(pos)
