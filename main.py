import pygame
import sqlite3
import sys
from scenes import Menu, TestsList, Test, Result
from functions import terminate

# Ссылка на Github: https://github.com/Likogeles/HistoryTest

# Для создания exe приложения использовать:
# pyinstaller -F -w -i "E:\PyCharm Projects\HistoryTest\data\icon.ico" main.py
# Не забудь! Файл data не добавляется в exe, а значит он должен находится в одной директории с приложением!
# Иначе не запустится!

pygame.init()

pygame.display.set_caption("Тесты по истории России")
pygame.display.set_icon(pygame.image.load("data/Sprites/icon.png"))
screen = pygame.display.set_mode((1280, 720))

background_color = (237, 238, 243)
scenename = "menu"
oldscenename = scenename
Scene = Menu()

TIMEEVENT = 30
pygame.time.set_timer(TIMEEVENT, 10)
mouse_pos = (0, 0)
while True:
    if scenename == "x":
        scenename = oldscenename
    if scenename != oldscenename:
        print("Смена сцены на", scenename)
        if scenename == "menu":
            Scene = Menu()
        elif scenename == "tests":
            Scene = TestsList()
        elif scenename[:5] == "topic":
            Scene = Test(scenename[5:])
        elif scenename[:6] == "result":
            Scene = Result(scenename[6:])
        else:
            print("Сцена '" + scenename + "' не найдена")
            terminate()
        oldscenename = scenename

    if scenename[:5] == "topic":
        if Scene.need_switch_scene_to_result:
            scenename = Scene.click((0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Программа завершена по инициативе пользователя")
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                scenename = Scene.click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and (scenename[:5] == "topic" or scenename[:6] == "result"):
                Scene.anti_click()

        elif event.type == pygame.MOUSEMOTION:
            Scene.mouse_motion(event.pos)
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEWHEEL:
            if scenename[:5] == "topic" or scenename[:6] == "result":
                Scene.slide(mouse_pos, event.y, False)

        Scene.render(screen, background_color)
    pygame.display.flip()
