import pgzrun
import time
import string
from pgzero.actor import Actor
from pgzero.clock import schedule_interval
from pgzero.builtins import *


WIDTH = 1000
HEIGHT = 600
TITLE = "Кликер"


kosmos = Actor("kosmos")
fon1 = Actor("fon1 (3)",(503, 300))# фон для кликера
con = Actor("krasa5", (500,325))  # крыса
money = Actor("money1", (382, 100))  # деньги
molni = Actor("molni", (462, 30))  # молния
moln = Actor("molni3", (345, 490))  # молния 2
meny = Actor("menu")  # меню
play = Actor("play3")  # играть
nazad = Actor("nazad3", (500, 585))  # кнопка назад
nazad2 = Actor("nazad4", (500, 581))  # кнопка назад для магазина
nazad3 = Actor("nazad4", (500, 581))  # кнопка назад для магазина
avtor = Actor("avtor3", (150, 200))  # автор
shop = Actor("shop (2)", (625, 564))  # магазин
shop_2 = Actor("shop_2", (525, 564))
menu_shop = Actor("menu_magaza2", size=(WIDTH, HEIGHT))  # меню магазина1
menu_shop_2 = Actor("menu_magaza4", size=(WIDTH, HEIGHT))  # меню магазина2
menu_shop_3 = Actor("menu_magaza4", size=(WIDTH, HEIGHT))  # меню магазина3
avtori = Actor("avtori2")  # расказ о автора
sell = Actor("sell (1)", (94, 293))  # продажа
sell_2 = Actor("sell (1)", (297, 293))  # продажа2
sell_3 = Actor("sell (1)", (497, 293))  # продажа3
sell_4 = Actor("sell (1)", (697, 293))  # продажа4
sell_5 = Actor("sell (1)", (697, 293))  # продажа5
sell_6 = Actor("sell (1)", (697, 293))  # продажа6
sell_7 = Actor("sell (1)", (697, 293))  # продажа7
sell_8 = Actor("sell (1)", (697, 293))  # продажа8
bonys = Actor("bonys (3)", (97, 200))  # бонус1
bonys_2 = Actor("bonys2 (1)", (300, 200))  # бонус2
bonys_3 = Actor("bonys3 (1)", (500, 200))  # бонус3
bonys_4 = Actor("bonys3 (1)", (700, 200))  # бонус4
nazat = Actor("nazat (1)", (50, 557))
vpered= Actor("vpered (1)", (950, 557))
# переменные
energe = 5
max_energe = 5
energe_recovery_time = 2
can_click = True
energy = 100
count = 100
animals = []
mode = "menu"
price = 500
price_2 = 20
price_3 = 100
price_4 = 20


# отрисовка картин
def draw():
    if mode == "menu":
        meny.draw()
        play.draw()
        avtor.draw()
    if mode == "avtori":
        avtori.draw()
        nazad.draw()
    if mode == "shop":
        menu_shop.draw()
        nazad2.draw()
        sell.draw()
        sell_2.draw()
        sell_3.draw()
        sell_4.draw()
        bonys.draw()
        bonys_2.draw()
        bonys_3.draw()
        bonys_4.draw()
        vpered.draw()
        screen.draw.text("монеты", center=(40, 60), color="white", fontsize=20)
        screen.draw.text("энергия", center=(40, 10), color="white", fontsize=20)
        screen.draw.text(str(energy), center=(100, 10), color="white", fontsize=20)
        screen.draw.text(str(count), center=(100, 60), color="white", fontsize=20)
        screen.draw.text("+5 монет за клик", center=(300, 200), color="white", fontsize=20)
        screen.draw.text("+5 энергии за клик", center=(700, 230), color="white", fontsize=18)
        screen.draw.text("X2", center=(150, 130), color="white", fontsize=40)
        screen.draw.text("100 стамины", center=(500, 230), color="white", fontsize=20)
        screen.draw.text("ЦЕНА:" + str(price) + "монеток", center=(100, 260), color="orange", fontsize=18)
        screen.draw.text("ЦЕНА:" + str(price_2) + "монеток", center=(300, 260), color="orange", fontsize=18)
        screen.draw.text("ЦЕНА:" + str(price_3) + "энергии", center=(500, 260), color="orange", fontsize=18)
        screen.draw.text("ЦЕНА:" + str(price_4) + "энергии", center=(700, 260), color="orange", fontsize=18)
    if mode == "menu_shop_2":
        menu_shop_2.draw()
        nazat.draw()
        screen.draw.text("монеты", center=(40, 60), color="white", fontsize=20)
        screen.draw.text("энергия", center=(40, 10), color="white", fontsize=20)
        screen.draw.text(str(energy), center=(100, 10), color="white", fontsize=20)
        screen.draw.text(str(count), center=(100, 60), color="white", fontsize=20)
    if mode == "shop_2":
        menu_shop_3.draw()
        nazad2.draw()
        screen.draw.text("монеты", center=(40, 60), color="white", fontsize=20)
        screen.draw.text("энергия", center=(40, 10), color="white", fontsize=20)
        screen.draw.text(str(energy), center=(100, 10), color="white", fontsize=20)
        screen.draw.text(str(count), center=(100, 60), color="white", fontsize=20)
    if mode == "play":
        kosmos.draw()
        fon1.draw()
        con.draw()
        money.draw()
        molni.draw()
        moln.draw()
        shop.draw()
        shop_2.draw()
        screen.draw.text(str(count), center=(460, 100), color="white", fontsize=28)
        screen.draw.text(str(energy), center=(510, 30), color="white", fontsize=27)
        screen.draw.text(str(energe), center=(378, 490), color="white", fontsize=18)
        if not can_click:
            screen.draw.text("Энергия нет! ", center=(378, 450), color="white", fontsize=16)


# Функции бонусов
def for_bonus_1():
    global count
    count += 500


def for_bonus_2():
    global can_click, count
    count += 20


def for_bonus_3():
    global max_energe
    max_energe += 100


def for_bonus_4():
    global energy
    energy += 20


def update(dt):
    global energe, can_click
    if not can_click:
        # Проверяем, прошло ли время восстановления энергии
        if time.time() - recovery_start >= energe_recovery_time:
            energe = max_energe  # Восстанавливаем энергию
            can_click = True  # Разрешаем кликать




def on_mouse_down(button, pos):
    global energe, can_click, recovery_start
    global count
    global energy
    global mode
    global price, price_2, price_3, price_4
    global max_energe
    if mode == "play":
        if button == mouse.LEFT:
            if shop.collidepoint(pos):
                mode = "shop"
            elif shop_2.collidepoint(pos):
                mode = "shop_2"
            if con.collidepoint(pos):
                count += can_click
                energy += can_click
                if can_click:
                    if energe > 0:
                        energe -= 1  # Уменьшаем энергию на 1 при клике
                        if energe == 0:
                            can_click = False  # Запретить клики
                            recovery_start = time.time()  # Забыть время начала восстановлени
# Режим меню
    elif mode == "menu" and button == mouse.LEFT:
        if play.collidepoint(pos):
            mode = "play"
        elif avtor.collidepoint(pos):
            mode = "avtori"
    elif mode == "avtori" and button == mouse.LEFT:
        if nazad.collidepoint(pos):
            mode = "menu"

# кнопка в игре в магазин временный
    elif mode == "shop_2" and button == mouse.LEFT:
        if nazad3.collidepoint(pos):
            mode = "play"
# кнопка в игре
    elif mode == "shop" and button == mouse.LEFT:
        if nazad2.collidepoint(pos):
            mode = "play"
        # кнопки для магазина
        elif sell.collidepoint(pos):
            if count >= price:
                schedule_interval(for_bonus_1, 2)
                count -= price
                price *= 2
        elif sell_2.collidepoint(pos):
            if count >= price_2:
                can_click += 4
                count -= price_2
                price_2 *= 2
        elif sell_3.collidepoint(pos):
            if energy >= price_3:
                max_energe += 100
                energy -= price_3
                price_3 *= 2
        elif sell_4.collidepoint(pos):
            if energy >= price_4:
                can_click += 4
                energy -= price_4
                price_4 *= 2
#2 окно в магазине
        elif vpered.collidepoint(pos):
            mode = "menu_shop_2"
    elif mode == "menu_shop_2" and button == mouse.LEFT:
        if nazat.collidepoint(pos):
            mode = "shop"
pgzrun.go()

