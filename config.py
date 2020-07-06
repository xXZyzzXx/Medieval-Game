# Название: наука требуемая для постройки, время постройки в сек, стоимость в ресурсах [дерево = > ]
import buildings as build
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MUSIC_VOLUME = 0.5
buildings_in_menu = 5  # Сколько зданий показывать
house1 = 2  # Уровень здания
account_buildings = []
current_tab_choice = 'Все'

buildings = {'Хижина': [[None], 100, [60, 40, 0, 5], r"/images/house.png", 'Социальные'],
             'Землянка': [['Колесо', 'Дома'], 40, [30, 0, 5, 0], r"/images/building_found.png", 'Социальные'],
             'Казармы': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Мастерская': [['Обработка дерева'], 20, [7400, 2200, 500, 388], r"/images/building_found.png",
                            'Производственные'],
             'Казармы1': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Казармы2': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Казармы3': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Казармы4': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],

             }

b = []  # Временные здания, доступные для постройки

for o in range(10):

    h = [build.Building_House(), build.Building_Barracks(),  build.Building_Granary(), build.Building_Masterskaya()]
    b.append(random.choice(h))

categories = {'Социальные': r"/images/wood.png", 'Военные': r"/images/clay.png",
              'Производственные': r"/images/money.png", 'Все': r"/images/iron.png"}


class Player:
    def __init__(self):
        self.list_buildings = []


"""
'Казармы6': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Казармы7': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Казармы8': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
             'Казармы9': [['Военное дело'], 60, [20, 30, 400, 50], r"/images/barracks.png", 'Военные'],
"""

current_technologies = ['Военное дело', 'Колесо', 'Дома']

player = {'Город': [6, 1]}

resourses = {'Древесина': [4000, 20, r"/images/wood.png"],
             'Железо': [70000, 0, r"/images/iron.png"],
             'Еда': [600, 0.2, r"/images/food.png"],
             'Глина': [20, 9970, r"/images/clay.png"],
             'Деньги': [1550, 5550, r"/images/money.png"]}

b_house = {'1': [0.2, 60, 40, 0, 5],
           '2': [0.4, 120, 40, 0, 5],
           '3': [1, 200, 100, 10, 0]}


class HouseBuilding:
    def __init__(self):
        self.b_house = b_house
