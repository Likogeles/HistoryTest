import pygame
import os
import time
from classes import BackgroundImage
from classes import Button
from classes import QuestionButton as QtButton
from classes import Slider, BigSlider
from classes import QuestionImage


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

        BackgroundImage("background", 0, 0, self.background_sprites)
        BackgroundImage("topiclist", 271, 10, self.background_sprites)

        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 35)

        filename = "data/TestTopics/TestsTopics.txt"
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            self.TestsTopics = [line.strip() for line in TestsTopicsFile]

        filename = "data/Results/results.txt"
        with open(filename, 'r', encoding='utf-8') as ResultFile:
            file_lines = [line.strip() for line in ResultFile]
        info = {}

        for i in file_lines:
            k = i.split()
            info[k[0][:-1]] = i.split()[1:]

        self.nums_strings = []
        for i in range(len(self.TestsTopics)):
            self.TestsTopics[i] = self.TestsTopics[i].split('*')[:-1][0]
            Button("topic" + str(i), "topicbut", 20, 85 * i + 100, self.but_sprites, text=self.TestsTopics[i])
            if str(i) in info:
                self.nums_strings.append([i, info[str(i)][0], info[str(i)][1] + "%", info[str(i)][2]])
                BackgroundImage("nums", 645,  85 * i + 100, self.background_sprites)
                Button("result" + str(i), "myanswers", 850, 85 * i + 100, self.but_sprites)
        Button("menu", "backbut", 20, 10, self.but_sprites)

    def render(self, screen, background_color):
        screen.fill(background_color)
        self.background_sprites.draw(screen)
        self.but_sprites.draw(screen)

        color = (0, 0, 255)

        for i in range(len(self.nums_strings)):

            if int(self.nums_strings[i][2][:-1]) < 40:
                color = (255, 0, 0)
            elif int(self.nums_strings[i][2][:-1]) < 60:
                color = (255, 127, 39)
            elif int(self.nums_strings[i][2][:-1]) < 80:
                color = (255, 255, 0)
            else:
                color = (0, 255, 0)

            # Результаты теста

            # w = 620 + 128 - self.font.size(self.nums_strings[i][1])[0] / 2

            w = 655
            screen.blit(self.font.render(self.nums_strings[i][1], True, (0, 0, 0)),
                        (w + 1,  85 * self.nums_strings[i][0] + 90 + 1))

            screen.blit(self.font.render(self.nums_strings[i][1], True, color), (w,  85 * self.nums_strings[i][0] + 90))

            screen.blit(self.font.render(self.nums_strings[i][2], True, (0, 0, 0)),
                        (w + 1,  85 * self.nums_strings[i][0] + 125 + 1))

            screen.blit(self.font.render(self.nums_strings[i][2], True, color), (w,  85 * self.nums_strings[i][0] + 125))

            w = w + 130 - self.font.size(self.nums_strings[i][3])[0]
            color = (0, 0, 0)
            screen.blit(self.font.render(self.nums_strings[i][3], True, color), (w + 30 + 1,  85 * self.nums_strings[i][0] + 110 + 1))
            color = (253, 253, 253)
            screen.blit(self.font.render(self.nums_strings[i][3], True, color), (w + 30,  85 * self.nums_strings[i][0] + 110))

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
        self.need_switch_scene_to_result = False
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
        self.prev_but = Button("prev", "prevquestion", 70, 629, self.prev_but_sprite, self.all_but_sprites)
        Button("result" + str(self.test_id), "finish", 468, 629, self.but_sprites, self.all_but_sprites)
        self.next_but = Button("next", "nextquestion", 866, 629, self.next_but_sprite, self.all_but_sprites)

        # self.flagbut = Button("flag", "flag", 1145, 305, self.but_sprites)

        BackgroundImage("background", 0, 0, self.background_sprites)

        BackgroundImage("topic", 270, 10, self.background_sprites)
        BackgroundImage("question", 270, 92, self.background_sprites)
        BackgroundImage("questionnum", 1030, 10, self.background_sprites)

        # BackgroundImage("slider", 20, 90, self.background_sprites)
        # BackgroundImage("dummy0", 0, 0, self.dummy_sprites)
        # BackgroundImage("dummy1", 0, 686, self.dummy_sprites)
        BackgroundImage("timer", 20, 90, self.dummy_sprites)

        self.question_font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 25)
        self.timer_font = pygame.font.Font(os.path.join('data', "Fonts/consolas.ttf"), 40)
        self.answer_font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 10)

        # Создания названия темы

        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 35)
        filename = "data/TestTopics/TestsTopics.txt"
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            tests_topics = [line.strip() for line in TestsTopicsFile]

        self.topic = tests_topics[int(test_id)].split('*')[0]
        self.topic_x = 270 + 740 / 2 - self.font.size(self.topic)[0] / 2

        # Работа с файлом вопросов

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
                tmp_answers.append([file_lines[i][2:]])
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

        # self.questions_buts = []
        # for i in range(len(self.questions)):
        #     k = QtButton(i, 30, self.questions_list_y, 345, self.questions[i],
        #     self.qtbut_sprites, self.all_but_sprites)
        #     self.questions_buts.append(k)
        #     self.questions_list_y += k.height() + 5

        # Создание кнопок ответов

        self.answer_buts = [
            Button("x", "answerbut", 35, 430, self.answer_but_sprites, self.all_but_sprites, answer_id=1),
            Button("x", "answerbut", 645, 430, self.answer_but_sprites, self.all_but_sprites, answer_id=2),
            Button("x", "answerbut", 35, 530, self.answer_but_sprites, self.all_but_sprites, answer_id=3),
            Button("x", "answerbut", 645, 530, self.answer_but_sprites, self.all_but_sprites, answer_id=4)
        ]

        # self.questions_buts[0].now = True
        # self.questions_buts[0].charge_switch((0, 0))

        # Работа со слайдером

        # self.k_of_slide = int((self.questions_list_y - 100) / (590 - 70))
        #
        # self.slider = 0
        # if self.questions_list_y > 700:
        #     self.slider = Slider(380, 100, (20, 90, 375, 594), self.slider_sprite, self.all_but_sprites)
        #     self.slider_logic = False
        #     self.slider_mouse_pos_y = 0

        # Генерация строк каждого вопроса для корректного отображения на странице

        self.strings = []

        width = 1000 / (self.question_font.size("Wa")[0] / 2)  # Кол-во символов, выделенных на ширину вопроса

        for k in range(len(self.questions)):
            string = ""
            leng = 0
            for i in self.questions[k].split():
                if leng + len(i) > width or i == '*':
                    self.strings.append([])
                    self.strings[k].append(string)
                    string = ""
                    leng = 0
                    if i == '*':
                        continue
                string += i + " "
                leng += len(i) + 1
            self.strings.append([])
            self.strings[k].append(string)

        # работа таймером

        filename = "data/TestTopics/TestsTopics.txt"
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            file_lines = [line.strip() for line in TestsTopicsFile]

        self.timer_seconds = int(file_lines[int(test_id)].split('*')[-1]) * 60

        self.start_time = time.time()

    def render(self, screen, background_color):
        screen.fill(background_color)
        self.background_sprites.draw(screen)

        # Отрисовка списка вопросов
        self.qtbut_sprites.draw(screen)
        # pygame.draw.rect(screen, (70, 54, 37), (20, 91, 375, 594), 3)

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

        # отрисовка темы
        screen.blit(self.font.render(self.topic, True, (0, 0, 0)), (self.topic_x + 1, 21))
        screen.blit(self.font.render(self.topic, True, (253, 253, 253)), (self.topic_x, 20))

        # отрисовка номера вопроса
        screen.blit(self.font.render("Вопрос:", True, (0, 0, 0)), (1071, 16))
        screen.blit(self.font.render("Вопрос:", True, (253, 253, 253)), (1070, 15))
        text = str(self.question_id + 1) + "/" + str(len(self.questions))
        screen.blit(self.font.render(text, True, (0, 0, 0)), (1116, 51))
        screen.blit(self.font.render(text, True, (253, 253, 253)), (1115, 50))

        # Отрисовка вопроса

        strings_y = 100
        for i in self.strings[self.question_id]:
            if "А. " in i or "Б. " in i:
                strings_y += 20
            screen.blit(self.question_font.render(i, True, (0, 0, 0)), (291, strings_y + 1))
            screen.blit(self.question_font.render(i, True, (0, 0, 0)), (291, strings_y - 1))
            screen.blit(self.question_font.render(i, True, (0, 0, 0)), (289, strings_y + 1))
            screen.blit(self.question_font.render(i, True, (0, 0, 0)), (289, strings_y - 1))
            screen.blit(self.question_font.render(i, True, (253, 253, 253)), (290, strings_y))
            strings_y += self.question_font.size(i)[1] - 10

        # отрисовка времени

        seconds = self.timer_seconds - int(time.time() - self.start_time)

        if seconds <= 0:
            self.need_switch_scene_to_result = True

        minutes = int(seconds / 60)
        seconds = str(seconds % 60)
        if len(seconds) == 1:
            seconds = "0" + seconds

        text = str(minutes) + ":" + seconds
        timer_x = 20 + 115 - self.timer_font.size(text)[0] / 2

        screen.blit(self.timer_font.render(text, True, (0, 0, 0)), (timer_x + 1, 125 + 1))
        if minutes < 5:
            screen.blit(self.timer_font.render(text, True, (250, 0, 0)), (timer_x, 125))
        else:
            screen.blit(self.timer_font.render(text, True, (253, 253, 253)), (timer_x, 125))

        # Отрисовка ответов:

        string_height = self.answer_font.size("К")[1] + 5
        for i in range(4):
            if self.answer_buts[i].charge_log:
                for j in range(-2, 6):
                    for k in range(len(self.answers[self.question_id][i])):
                        screen.blit(self.question_font.render(
                            self.answers[self.question_id][i][k], True, (128, 128, 128)),
                            (45 + 610 * (i % 2) + j, 430 + (100 if i == 2 or i == 3 else 0) + j + k * string_height))

            for k in range(len(self.answers[self.question_id][i])):
                screen.blit(self.question_font.render(
                    self.answers[self.question_id][i][k], True, (0, 0, 0)),
                    (45 + 610 * (i % 2) + 1, 430 + (100 if i == 2 or i == 3 else 0) + k * string_height + 1))
                screen.blit(self.question_font.render(
                    self.answers[self.question_id][i][k], True, (253, 253, 253)),
                    (45 + 610 * (i % 2), 430 + (100 if i == 2 or i == 3 else 0) + k * string_height))

    def change_question(self, x):
        # self.questions_buts[self.question_id].now = False
        # self.questions_buts[self.question_id].charge_switch((0, 0))
        self.question_id = x
        # self.questions_buts[self.question_id].now = True
        # self.questions_buts[self.question_id].charge_switch((0, 0))

        for i in self.answer_buts:
            i.now = self.nums_of_selected_answers[self.question_id] == i.answer_id
            i.charge_switch((0, 0))

    def finish(self):
        filename = "data/Results/results.txt"
        line = str(self.test_id) + ": "

        nums = 0
        for i in range(len(self.nums_of_selected_answers)):
            if int(self.nums_of_selected_answers[i]) == int(self.nums_of_right_answers[i]):
                nums += 1
        line += str(nums) + "/" + str(len(self.nums_of_right_answers)) + " "
        line += str(int((nums / len(self.nums_of_right_answers)) * 100)) + " "

        seconds = int(time.time() - self.start_time)
        minutes = str(int(seconds / 60))
        seconds = str(seconds % 60)
        if len(seconds) == 1:
            seconds = "0" + seconds
        line += minutes + ":" + seconds + " "

        n = len(self.nums_of_selected_answers)
        for i in range(n):
            line += str(self.nums_of_selected_answers[i]) + "*" + str(self.nums_of_right_answers[i])
            if i < n - 1:
                line += "_"
        line += "\n"
        with open(filename, 'a', encoding='utf-8') as ResultsFile:
            ResultsFile.write(line)

    def click(self, pos):
        if self.need_switch_scene_to_result:
            pos = (695, 635)

        for i in self.answer_but_sprites:
            x = i.click(pos)
            if x:
                if self.nums_of_selected_answers:
                    self.answer_buts[self.nums_of_selected_answers[self.question_id] - 1].now = False
                self.nums_of_selected_answers[self.question_id] = i.answer_id
                # self.questions_buts[self.question_id].complete = True
                # self.questions_buts[self.question_id].charge_switch((0, 0))
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
            elif "result" in str(x):
                self.finish()
                return x
            elif x:
                return x
        self.mouse_motion(pos)
        return "x"

    def anti_click(self):
        self.slider_logic = False

    def mouse_motion(self, pos):
        # if self.slider_logic:
        #     self.slide(pos, -(pos[1] - self.slider_mouse_pos_y) * 0.125, True)
        for i in self.all_but_sprites:
            i.charge_switch(pos)
        # self.slider_mouse_pos_y = pos[1]

    def slide(self, pos, y, mouse_logic):
        pass
        # if self.slider:
        #     x = self.slider.slide(pos, y, mouse_logic)
        #     if x:
        #         for i in self.qtbut_sprites:
        #             i.rect.y -= x * self.k_of_slide
        # for i in self.all_but_sprites:
        #     i.charge_switch(pos)


class Result:
    def __init__(self, test_id):
        self.but_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.qtim_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.backbackground_sprites = pygame.sprite.Group()
        self.slider_sprite = pygame.sprite.Group()

        BackgroundImage("background", 0, 0, self.backbackground_sprites)
        BackgroundImage("empty0", 0, 0, self.background_sprites)
        BackgroundImage("empty1", 0, 705, self.background_sprites)
        BackgroundImage("topic", 464, 10, self.background_sprites)
        BackgroundImage("nums", 260, 10, self.background_sprites)

        self.font = pygame.font.Font(os.path.join('data', "Fonts/VollkornSC-Regular.ttf"), 35)

        filename = "data/TestTopics/TestsTopics.txt"
        with open(filename, 'r', encoding='utf-8') as TestsTopicsFile:
            tests_topics = [line.strip() for line in TestsTopicsFile]

        self.topic = tests_topics[int(test_id)].split('*')[0]
        self.topic_x = 464 + 740 / 2 - self.font.size(self.topic)[0] / 2

        Button("tests", "backbut", 20, 10, self.but_sprites)

        # файл с вопросами и ответами

        filename = "data/Questions/topic" + test_id + ".txt"
        with open(filename, 'r', encoding='utf-8') as TestFile:
            file_lines = [line.strip() for line in TestFile]

        self.questions = []
        self.answers = []
        k = 0
        tmp_answers = []
        for i in range(len(file_lines)):
            if k == 0:
                self.questions.append(str(len(self.questions) + 1) + ") " + file_lines[i])
            elif k == 1 or k == 2 or k == 3 or k == 4:
                tmp_answers.append([file_lines[i][2:]])
            elif k == 5:
                self.answers.append(tmp_answers)
                tmp_answers = []
            k += 1
            if k > 5:
                k = 0

        filename = "data/Results/results.txt"
        with open(filename, 'r', encoding='utf-8') as ResultFile:
            file_lines = [line.strip() for line in ResultFile]
        info = {}
        for i in file_lines:
            k = i.split()
            info[k[0][:-1]] = i.split()[1:]

        self.info = info[test_id]

        # Генерация вопросов и ответов
        answer = self.info[3].split('_')
        self.answers_id = []
        for i in answer:
            self.answers_id.append(i.split('*'))

        self.questions_list_y = 110
        for i in range(len(self.questions)):
            k1 = QuestionImage(30, self.questions_list_y, 580, self.questions[i], self.qtim_sprites)

            right = self.answers[i][int(self.answers_id[i][0]) - 1][0] == self.answers[i][int(self.answers_id[i][1]) - 1][0]

            if int(self.answers_id[i][0]):
                k2 = QuestionImage(615, self.questions_list_y, 300, self.answers[i][int(self.answers_id[i][0]) - 1][0], self.qtim_sprites, right=right)
            else:
                k2 = QuestionImage(615, self.questions_list_y, 300, "Нет ответа", self.qtim_sprites, right=False)

            k3 = QuestionImage(920, self.questions_list_y, 300, self.answers[i][int(self.answers_id[i][1]) - 1][0], self.qtim_sprites, right=True)

            k = max([k1.height(), k2.height(), k3.height()])
            self.questions_list_y += k + 5

        # Работа со слайдером

        self.k_of_slide = int((self.questions_list_y - 100) / (590 - 70))

        self.slider = 0
        if self.questions_list_y > 700:
            self.slider = BigSlider(1230, 110, (0, 100, 1280, 600), self.slider_sprite, self.but_sprites)
            self.slider_logic = False
            self.slider_mouse_pos_y = 0

    def render(self, screen, background_color):

        self.backbackground_sprites.draw(screen)
        self.qtim_sprites.draw(screen)
        self.background_sprites.draw(screen)
        self.but_sprites.draw(screen)
        self.slider_sprite.draw(screen)

        pygame.draw.rect(screen, (70, 54, 37), (20, 100, 1250, 605), 3)

        # отрисовка темы
        screen.blit(self.font.render(self.topic, True, (0, 0, 0)), (self.topic_x + 1, 21))
        screen.blit(self.font.render(self.topic, True, (253, 253, 253)), (self.topic_x, 20))

        # отрисовка результатов

        nums = self.info[:3]
        if int(nums[1]) < 40:
            color = (255, 0, 0)
        elif int(nums[1]) < 60:
            color = (255, 127, 39)
        elif int(nums[1]) < 80:
            color = (255, 255, 0)
        else:
            color = (0, 255, 0)
        w = 270
        screen.blit(self.font.render(nums[0], True, (0, 0, 0)), (w + 1, 3))
        screen.blit(self.font.render(nums[0], True, color), (w, 2))
        screen.blit(self.font.render(nums[1] + "%", True, (0, 0, 0)), (w + 1, 36))
        screen.blit(self.font.render(nums[1] + "%", True, color), (w, 35))
        w = w + 70 - self.font.size(nums[2])[0]
        color = (0, 0, 0)
        screen.blit(self.font.render(nums[2], True, color), (w + 101, 21))
        color = (253, 253, 253)
        screen.blit(self.font.render(nums[2], True, color), (w + 100, 20))

    def click(self, pos):
        for i in self.but_sprites:
            x = i.click(pos)
            if x == "slide":
                self.slider_logic = True
            elif x:
                return x
        self.mouse_motion(pos)
        return "x"

    def anti_click(self):
        self.slider_logic = False

    def mouse_motion(self, pos):
        if self.slider_logic:
            self.slide(pos, -(pos[1] - self.slider_mouse_pos_y) * 0.125, True)
        for i in self.but_sprites:
            i.charge_switch(pos)
        self.slider_mouse_pos_y = pos[1]

    def slide(self, pos, y, mouse_logic):
        if self.slider:
            x = self.slider.slide(pos, y, mouse_logic)
            if x:
                for i in self.qtim_sprites:
                    i.rect.y -= x * self.k_of_slide
        for i in self.but_sprites:
            i.charge_switch(pos)
