import pygame
import os
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
            Button("result" + str(i), "myanswers", 887, 85 * i + 150, self.but_sprites)
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
        self.answer_but_sprites = pygame.sprite.Group()

        self.test_id = test_id

        self.slider_sprite = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.dummy_sprites = pygame.sprite.Group()
        self.question_id = 0
        self.questions_list_y = 100

        Button("tests", "backbut", 20, 10, self.but_sprites, self.all_but_sprites)
        self.prev_but = Button("prev", "prevquestion", 410, 629, self.prev_but_sprite, self.all_but_sprites)
        Button("result" + str(self.test_id), "finish", 690, 629, self.but_sprites, self.all_but_sprites)
        self.next_but = Button("next", "nextquestion", 970, 629, self.next_but_sprite, self.all_but_sprites)

        self.flagbut = Button("flag", "flag", 1145, 305, self.but_sprites)

        BackgroundImage("background", 0, 0, self.background_sprites)
        BackgroundImage("question", 410, 13, self.background_sprites)
        BackgroundImage("topicimage" + str(self.test_id), 527, 188, self.background_sprites)
        BackgroundImage("slider", 20, 90, self.background_sprites)
        BackgroundImage("dummy0", 0, 0, self.dummy_sprites)
        BackgroundImage("dummy1", 0, 686, self.dummy_sprites)
        BackgroundImage("timer", 117, 10, self.dummy_sprites)

        self.question_font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 25)
        self.answer_font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 15)

        # Работа с файлом новая

        filename = "data/Questions/topic" + test_id + ".txt"
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            file_lines = [line.strip() for line in TestsTopicsFile]

        self.answers = []
        self.questions = []
        self.nums_of_right_answers = []
        k = 0
        tmp_answers = []
        for i in range(len(file_lines)):
            if k == 0:
                self.questions.append(str(len(self.questions) + 1) + ") " + file_lines[i])
            elif k == 1 or k == 2 or k == 3 or k == 4:
                tmp_answers.append([file_lines[i][3:]])
            elif k == 5:
                self.answers.append(tmp_answers)
                tmp_answers = []
                self.nums_of_right_answers.append(file_lines[i].split("&")[-1])
            k += 1
            if k > 5:
                k = 0

        # Строки ответов

        answer_string_w = 300 / (self.answer_font.size("Wa")[0] / 2)
        for i in range(len(self.answers)):
            for j in range(len(self.answers[i])):
                answer_words = self.answers[i][j][0].split()
                strings = []
                string = ""
                leng = 0
                for k in answer_words:
                    if leng + len(k) > answer_string_w:
                        strings.append(string[:-1])
                        leng = 0
                        string = ""
                    string += k + " "
                    leng += len(k) + 1
                strings.append(string[:-1])

                self.answers[i][j] = strings

        self.nums_of_selected_answers = [0 for i in range(len(self.answers))]

        # Создание кнопок списка вопросов

        self.questions_buts = []
        for i in range(len(self.questions)):
            k = QtButton(i, 30, self.questions_list_y, 345, self.questions[i], self.qtbut_sprites, self.all_but_sprites)
            self.questions_buts.append(k)
            self.questions_list_y += k.height() + 5

        # Создание кнопок ответов

        self.answer_buts = [
            Button("x", "answerbut", 430, 420, self.answer_but_sprites, self.all_but_sprites, answer_id=1),
            Button("x", "answerbut", 830, 420, self.answer_but_sprites, self.all_but_sprites, answer_id=2),
            Button("x", "answerbut", 430, 520, self.answer_but_sprites, self.all_but_sprites, answer_id=3),
            Button("x", "answerbut", 830, 520, self.answer_but_sprites, self.all_but_sprites, answer_id=4)
        ]

        self.questions_buts[0].now = True
        self.questions_buts[0].charge_switch((0, 0))
        # Работа со слайдером

        self.k_of_slide = int((self.questions_list_y - 100) / (590 - 70))

        self.slider = 0
        if self.questions_list_y > 700:
            self.slider = Slider(380, 100, (20, 90, 375, 594), self.slider_sprite, self.all_but_sprites)
            self.slider_logic = False
            self.slider_mouse_pos_y = 0

        # Генерация строк каждого вопроса для корректного отображения на странице

        self.strings = []

        width = 1100 / (self.question_font.size("Wa")[0] / 2)  # Кол-во символов, выделенных на ширину вопроса

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

        self.answer_but_sprites.draw(screen)
        self.but_sprites.draw(screen)
        self.slider_sprite.draw(screen)

        # Отрисовка вопроса

        strings_y = 30
        for i in self.strings[self.question_id]:
            screen.blit(self.question_font.render(i, True, (0, 0, 0)), (430, strings_y))
            strings_y += self.question_font.size(i)[1]

        # Отрисовка ответов:

        string_height = self.answer_font.size("К")[1] + 2
        for i in range(4):
            if self.answer_buts[i].charge_log:
                for j in range(-2, 6):
                    for k in range(len(self.answers[self.question_id][i])):
                        screen.blit(self.question_font.render(
                            self.answers[self.question_id][i][k], True, (128, 128, 128)),
                            (440 + 400 * (i % 2) + j, 425 + (100 if i == 2 or i == 3 else 0) + j + k * string_height))

            for k in range(len(self.answers[self.question_id][i])):
                screen.blit(self.question_font.render(
                    self.answers[self.question_id][i][k], True, (253, 253, 253)),
                    (440 + 400 * (i % 2), 425 + (100 if i == 2 or i == 3 else 0) + k * string_height))

    def change_question(self, x):
        self.questions_buts[self.question_id].now = False
        self.questions_buts[self.question_id].charge_switch((0, 0))
        self.question_id = x
        self.questions_buts[self.question_id].now = True
        self.questions_buts[self.question_id].charge_switch((0, 0))

        self.flagbut.charge_lock = self.questions_buts[self.question_id].flag
        self.flagbut.charge_switch((0, 0))

        for i in self.answer_buts:
            i.now = self.nums_of_selected_answers[self.question_id] == i.answer_id
            i.charge_switch((0, 0))

    def finish(self):
        filename = "data/Results/results.txt"
        line = str(self.test_id) + ": "

        n = len(self.nums_of_selected_answers)
        for i in range(n):
            line += str(self.nums_of_selected_answers[i]) + "*" + str(self.nums_of_right_answers[i])
            if i < n - 1:
                line += "_"
        line += "\n"

        with open(filename, 'a', encoding='utf-8') as ResultsFile:
            ResultsFile.write(line)

    def click(self, pos):
        if self.flagbut.click(pos):
            self.questions_buts[self.question_id].flag = not self.questions_buts[self.question_id].flag
            self.flagbut.charge_lock = not self.flagbut.charge_lock
            self.flagbut.charge_switch((0, 0))
            self.questions_buts[self.question_id].charge_switch((0, 0))
            self.mouse_motion(pos)
            return "x"

        for i in self.answer_but_sprites:
            x = i.click(pos)
            if x:
                if self.nums_of_selected_answers:
                    self.answer_buts[self.nums_of_selected_answers[self.question_id] - 1].now = False
                self.nums_of_selected_answers[self.question_id] = i.answer_id
                self.questions_buts[self.question_id].complete = True
                self.questions_buts[self.question_id].charge_switch((0, 0))
                for j in self.answer_but_sprites:
                    j.now = False
                i.now = True
            i.charge_switch((0, 0))

        for i in self.all_but_sprites:
            x = i.click(pos)
            if type(x) == int:
                self.change_question(x)
            elif x == "prev":
                if self.question_id > 0:
                    self.change_question(self.question_id - 1)
            elif x == "next":
                if self.question_id < len(self.questions) - 1:
                    self.change_question(self.question_id + 1)
            elif x == "slide":
                self.slider_logic = True
            elif "results" in str(x):
                self.finish()
                return x
            elif x:
                return x
        self.mouse_motion(pos)
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


class Result:
    def __init__(self, test_id):
        self.but_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()

        filename = "data/TestTopics/TestsTopics.txt"
        BackgroundImage("background", 0, 0, self.background_sprites)
        BackgroundImage("topic", 345, 10, self.background_sprites)

        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 35)

        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            tests_topics = [line.strip() for line in TestsTopicsFile]

        self.topic = tests_topics[int(test_id)]
        self.topic_x = 345 + 590 / 2 - self.font.size(self.topic)[0] / 2
        Button("tests", "backbut", 20, 10, self.but_sprites)

        # for i in range(len(self.TestsTopics)):
        #     Button("topic" + str(i), "topicbut", 20, 85 * i + 150, self.but_sprites, text=self.TestsTopics[i])

    def render(self, screen, background_color):
        screen.fill(background_color)
        self.background_sprites.draw(screen)
        self.but_sprites.draw(screen)

        screen.blit(self.font.render(self.topic, True, (253, 253, 253)), (self.topic_x, 27))

    def click(self, pos):
        for i in self.but_sprites:
            if i.click(pos):
                return i.name
        return "x"

    def mouse_motion(self, pos):
        for i in self.but_sprites:
            i.charge_switch(pos)
