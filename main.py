import pygame
import sqlite3
import sys
from scenes import Menu, TestsList, Test
from functions import terminate

# Для создания exe приложения использовать:
# pyinstaller -F -w -i "E:\PyCharm Projects\HistoryTest\data\icon.ico" main.py
# Не забудь! Файл data не добавляется в exe, а значит он должен находится в одной директории с приложением!
# Иначе не запустится!


pygame.init()

pygame.display.set_caption("Тесты по истории России")
pygame.display.set_icon(pygame.image.load("data/Sprites/icon.png"))
screen = pygame.display.set_mode((1280, 720))

scenename = "menu"
oldscenename = scenename
Scene = Menu()

TIMEEVENT = 30
pygame.time.set_timer(TIMEEVENT, 10)
while True:
    if scenename != oldscenename:
        print("Смена сцены на", scenename)
        if scenename == "menu":
            Scene = Menu()
        elif scenename == "tests":
            Scene = TestsList()
        elif scenename[:5] == "topic":
            Scene = Test(scenename[5:])
        else:
            print("Сцена '" + scenename + "' не найдена")
            terminate()
        oldscenename = scenename

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Программа завершена по инициативе пользователя")
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            scenename = Scene.click(event.pos)
            if scenename == "x":
                scenename = oldscenename
        if event.type == pygame.MOUSEMOTION:
            Scene.mouse_motion(event.pos)
        Scene.render(screen)
    pygame.display.flip()
