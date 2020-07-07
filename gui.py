import arcade
import themes
import config
import os
import gui_advanced as ga
import iso


class MenuBox:
    def __init__(self, x, y, width, height, color=None, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.current_place = None
        self.button_list = []
        self.text_list = []
        self.icon_list = []
        self.rect_list = []
        self.scroll_list = []
        self.tabs_list = []
        self.tab_icon_list = []
        self.theme = theme
        self.how_scrolling = 0
        self.scroll = 0
        self.my_scroll = 0  # Чтоб обновлялись кнопки только если было вращение
        self.current_tab_choice = 'Все'
        self.building_list = None
        self.global_butt_list = None
        self.global_dialog_list = None
        if self.theme:
            self.texture = self.theme.dialogue_box_texture

    def update(self):
        self.update_building_content()  # Нужен перерасчёт building_list, поэтому дублируется обновление
        if self.how_scrolling < 0:  # Если скролл уходит за границы
            self.how_scrolling = 0
        if self.how_scrolling >= len(self.building_list) - config.buildings_in_menu:
            self.how_scrolling = len(self.building_list) - config.buildings_in_menu
        self.delete_dialoguebox_content()
        self.create_building_content()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.how_scrolling -= scroll_y  # Пролистать вниз/вверх
        self.scroll = scroll_y  # Текущее значение скролла
        self.update()

    def on_draw(self):
        if self.active:
            if self.theme:
                arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
            else:
                arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
            for icon in self.icon_list:
                icon.draw()
            for button in self.button_list:
                button.draw()
            for text in self.text_list:
                text.draw()
            for rect in self.rect_list:
                rect.draw()
            for scroll in self.scroll_list:
                scroll.draw()
            for tab in self.tabs_list:
                tab.draw()
            for tab_icon in self.tab_icon_list:
                tab_icon.draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_press(x, y)
        for tab in self.tabs_list:
            tab.check_mouse_press(x, y)
        for tab in self.scroll_list:
            tab.check_mouse_press(x, y)

    def on_mouse_release(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_release(x, y)
        for tab in self.tabs_list:
            tab.check_mouse_release(x, y)
        for tab in self.scroll_list:
            tab.check_mouse_release(x, y)

    def delete_dialoguebox_content(self):
        self.text_list.clear()
        self.button_list.clear()
        self.icon_list.clear()
        self.scroll_list.clear()
        self.rect_list.clear()
        self.tabs_list.clear()
        self.tab_icon_list.clear()

    def update_building_content(self):
        all_buildings = config.b  # Все здания
        self.building_list = []  # Здания по категориям
        for b in all_buildings:
            if b.building_type == self.current_tab_choice:
                self.building_list.append(b)

        if self.current_tab_choice == 'Все':  # Если выбрана категория "Все"
            self.building_list = all_buildings

    def create_building_content(self):  # Добавить обновление только для скролла и зданий
        self.delete_dialoguebox_content()
        self.update_building_content()
        list_buildings_to_create = self.building_list[int(0 + float(self.how_scrolling)):int(
            config.buildings_in_menu + float(self.how_scrolling))]  # Срез для отображения фиксированного кол-ва зданий

        top_text = arcade.gui.TextLabel('Меню строительства', self.x, self.y + self.height / 2.4,
                                        arcade.color.DARK_JUNGLE_GREEN, font_size=20, font_name='calibri',
                                        bold=True, align='center')
        scroll_line = arcade.Sprite(filename=os.getcwd() + r"/images/scroll_line.png",
                                    center_x=self.x - self.width / 2.5,
                                    center_y=self.y + 6, image_height=366, image_width=9)
        rope = arcade.Sprite(filename=os.getcwd() + r"/images/rope.png", scale=1,
                             center_x=self.x + self.width / 2.62,
                             center_y=self.y + 7, image_height=374, image_width=9)
        small_height = 120  # Чтоб скролл ездил по меньшей высоте
        scroll_line_top = scroll_line.center_y - small_height / 2 + scroll_line.height / 2

        if len(self.building_list) > config.buildings_in_menu:
            shag = (int(scroll_line.height - small_height)) / (
                    len(self.building_list) - config.buildings_in_menu)  # Шаг скролла

            gde = (scroll_line_top - shag * self.how_scrolling)  # Где рисовать скролл

            scroll_rect = ScrollRect(x=int(scroll_line.center_x), y=int(gde))  # Прямоугольник
            self.scroll_list.append(scroll_rect)
        else:  # Если зданий меньше, чем максимально допустимое кол-во
            # scroll_rect = ScrollRect(x=int(scroll_line.center_x), y=int(scroll_line_top), height=int(scroll_line.height*0.96))
            # scroll_rect.center_y = scroll_line.center_y
            pass

        i = 0
        for category in config.categories:  # Создание вкладок категорий
            tabs = TabButton(self, self.tabs_list, category, x=self.x + 50 - self.height / 2 + i * 50, y=self.y + 163)
            tab_icon = arcade.Sprite(os.getcwd() + config.categories.get(category), center_x=tabs.center_x,
                                     center_y=tabs.center_y, scale=0.9)
            self.tab_icon_list.append(tab_icon)
            self.tabs_list.append(tabs)
            i += 1

        self.button_list.append(CloseButton(self, self.x, self.y - self.height / 2.5))
        self.icon_list.append(scroll_line)
        # self.scroll_list.append(scroll_rect)
        self.icon_list.append(rope)
        self.text_list.append(top_text)

        list_to_after_build = []  # Здания, которые не открыты технологиями, доработать алгоритм.
        for tech in config.buildings:
            for t in config.buildings[tech][0]:
                for c in config.current_technologies:
                    if t == c:
                        list_to_after_build.append(tech)

        i = 0
        for building in list_buildings_to_create:
            y_coords = self.y + 120 - (i * 60)
            if i >= 0:  # Бесполезно, но отступ мешает
                rect = os.getcwd() + r"/images/rect1.png"
                if i % 2:
                    rect = os.getcwd() + r"/images/rect2.png"

                main_rect = arcade.Sprite(rect, center_x=self.x, center_y=y_coords)
                icon_building = arcade.Sprite((os.getcwd() + building.image_icon), 0.3, center_x=self.x - 220,
                                              center_y=y_coords)
                b_text = arcade.gui.TextLabel(building.name, icon_building.center_x + icon_building.width / 2 + 5,
                                              y_coords,
                                              themes.theme_text.font_color, font_size=20, font_name='Cursive',
                                              bold=True, anchor_x='left')
                distance = main_rect.right
                build_butt = BuildingButton(self, building, self.global_butt_list, self.global_dialog_list,
                                            int(distance) - 22, y_coords)

                self.icon_list.append(main_rect)
                self.text_list.append(b_text)
                self.icon_list.append(icon_building)
                self.button_list.append(build_butt)
                # Поиск сколько ресурсов всего у здания необходимы для строительства, планирую вычислить сколько должно
                #  быть прикреплено ресурсов с правой стороны GUI и нарисовать Стоимость + иконку в прямоугольнике.
                count = 0  # Счётчик ресурсов больше 0
                total_width = 0
                res_to_create = [[building.cost_wood, r"/images/wood.png"], [building.cost_clay, r"/images/clay.png"],
                                 [building.cost_food, r"/images/food.png"], [building.cost_iron, r"/images/iron.png"]]

                for f in res_to_create:  # Четыре ресурса
                    b_res_cost = f[0]  # Количество ресурсов
                    b_res_icon = f[1]  # Иконка
                    if b_res_cost > 0:
                        width_label = len(str(b_res_cost)) * 9

                        res_label = arcade.gui.TextLabel(str(b_res_cost), distance - 50 - total_width,
                                                         y_coords, themes.theme_text.font_color, align='center',
                                                         font_size=14, width=width_label, anchor_x='right')
                        res_icon = arcade.Sprite(os.getcwd() + b_res_icon, 0.5, center_x=res_label.x - width_label - 10,
                                                 center_y=res_label.y)
                        total_width += width_label + res_icon.width + 2
                        self.text_list.append(res_label)
                        self.icon_list.append(res_icon)
                    else:
                        if count > 0:
                            count -= 1
                    count += 1
                i += 1

    def create_house_content(self, name, icon, t_build, c_wood, c_food, c_iron, c_clay, b_lvl):
        self.delete_dialoguebox_content()
        self.button_list.append(CloseButton(self, self.x, self.y - self.height / 4))

        icon = arcade.Sprite(os.getcwd() + icon, 0.4, center_x=self.x - self.width / 3, center_y=self.y + 100)
        self.icon_list.append(icon)
        self.button_list.append(
            DestroyButton(self, self.global_butt_list, self.global_dialog_list, int(icon.center_x), int(icon.center_y-(icon.height/2)*1.3)))
        self.text_list.append(
            arcade.gui.TextLabel(f'{name}, уровень {b_lvl}', self.x, self.y + self.height / 2.4,
                                 themes.theme_text.font_color, bold=True, align='center'))

        count = 0  # Счётчик ресурсов больше 0
        total_width = 0

        res_rect = arcade.Sprite(os.getcwd() + r"/images/Brown.png", center_x=self.x,
                                 center_y=self.y + self.height / 3.5)
        distance = res_rect.right

        res_to_create = [[c_wood, r"/images/wood.png"], [c_clay, r"/images/clay.png"],
                         [c_food, r"/images/food.png"], [c_iron, r"/images/iron.png"]]

        for f in res_to_create:  # Четыре ресурса
            b_res_cost = f[0]  # Количество ресурсов
            b_res_icon = f[1]  # Иконка
            if b_res_cost > 0:
                width_label = len(str(b_res_cost)) * 9

                res_label = arcade.gui.TextLabel(str(b_res_cost), distance - 50 - total_width,
                                                 res_rect.center_y, themes.theme_text.font_color, align='center',
                                                 font_size=14, width=width_label, anchor_x='right')
                res_icon = arcade.Sprite(os.getcwd() + b_res_icon, 0.5, center_x=res_label.x - width_label - 10,
                                         center_y=res_label.y)
                total_width += width_label + res_icon.width + 2
                self.text_list.append(res_label)
                self.icon_list.append(res_icon)
            else:
                if count > 0:
                    count -= 1
            count += 1


class MainNav(arcade.Sprite):
    def update_pos(self, width, height):
        self.center_x = width / 2
        self.center_y = height - 67


class SideNav(arcade.Sprite):
    def __init__(self, image):
        super().__init__(filename=image)
        self.width_select = None

    def update_pos(self, width, height):
        self.center_x = width - self.width_select / 2
        self.center_y = height / 2


class CloseButton(ga.AdvancedButton):
    def __init__(self, dialoguebox, x, y, width=110, height=50, text="Закрыть"):
        super().__init__(x, y, width, height, text, theme=themes.theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed and self.dialoguebox.active:
            self.pressed = False
            self.dialoguebox.active = False
            self.dialoguebox.delete_dialoguebox_content()


class MusicButton(ga.AdvancedButton):
    def __init__(self, music, x, y, width=100, height=29, text="Turn on"):
        super().__init__(x, y, width, height, text, theme=themes.theme_textbox_button)
        self.music = music

    def on_press(self):
        self.pressed = True
        print(self.music)

    def on_release(self):
        if self.pressed:
            self.music.play()
            print(self.music)
            self.pressed = False


class AttackButton(ga.AdvancedButton):
    def __init__(self, dialoguebox_list, x, y, width=80, height=80, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_attack)
        self.dialoguebox_list = dialoguebox_list

    def on_press(self):
        if not self.dialoguebox_list[0].active and not self.dialoguebox_list[1].active and not self.dialoguebox_list[
            2].active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            #self.dialoguebox_list[0].active = True


class MailButton(ga.AdvancedButton):
    def __init__(self, dialoguebox_list, x, y, width=80, height=80, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_mail)
        self.dialoguebox_list = dialoguebox_list

    def on_press(self):
        if not self.dialoguebox_list[0].active and not self.dialoguebox_list[1].active and not self.dialoguebox_list[
            2].active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            #self.dialoguebox_list[0].active = True


class MapButton(ga.AdvancedButton):
    def __init__(self, dialoguebox_list, window, x, y, width=70, height=70, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_map)
        self.dialoguebox_list = dialoguebox_list
        self.window = window

    def on_press(self):
        if not self.dialoguebox_list[0].active and not self.dialoguebox_list[1].active and not self.dialoguebox_list[
            2].active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            view = iso.Iso(self.window)
            view.setup()
            self.window.show_view(view)
            #giself.dialoguebox_list[0].active = True


class Foundament(ga.AdvancedButton):
    def __init__(self, box_list, butt_list, x=0, y=0, width=149, height=200, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_found)
        self.dialoguebox = box_list[2]
        self.dialoguebox_list = box_list
        self.butt_list = butt_list
        self.current_place = None

    def on_press(self):
        if not self.dialoguebox_list[1].active and not self.dialoguebox_list[0].active and not self.dialoguebox_list[
            2].active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox.create_building_content()
            self.dialoguebox.active = True
            for dialog in self.dialoguebox_list:
                dialog.current_place = self.current_place  # С какой кнопки был вызов диалогбокса

    def update(self):
        pass

    def in_motion(self, y):
        pass


class DoorButton(ga.AdvancedButton):
    def __init__(self, x=0, y=0, width=100, height=40, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False


class BuildingButton(ga.AdvancedButton):
    def __init__(self, dialog, building, global_butt_list, global_dialog_list, x=0, y=0, width=32, height=32, text=""):
        super().__init__(x, y, width, height, text, theme=themes.theme_building_button)
        self.global_butt_list = global_butt_list
        self.global_dialog_list = global_dialog_list
        self.building = building
        self.dialog = dialog
        self.to_build = None

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            for b in config.b_buttons:
                if self.building.name == b:
                    self.to_build = config.b_buttons[self.building.name](self.global_dialog_list, self.dialog)
                    self.to_build.current_place = self.to_build
                    break
                else:
                    self.to_build = Foundament(self.global_dialog_list, self.global_butt_list)
                    self.to_build.current_place = self.to_build

            self.global_butt_list.remove(self.dialog.current_place)
            self.to_build.center_x, self.to_build.center_y = self.dialog.current_place.center_x, self.dialog.current_place.center_y
            for dialog in self.global_dialog_list:  # Установить текущее здание to build для всех окон dialoguebox
                dialog.current_place = self.to_build
            self.global_butt_list.append(self.to_build)
            self.dialog.active = False


class DestroyButton(ga.AdvancedButton):
    def __init__(self, dialog, global_butt_list, global_dialog_list, x=0, y=0, width=90, height=25, text="Разрушить"):
        super().__init__(x, y, width, height, text, theme=themes.theme_textbox_button, font_size=6)
        self.global_butt_list = global_butt_list
        self.global_dialog_list = global_dialog_list

        self.dialog = dialog
        self.to_build = None

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.to_build = Foundament(self.global_dialog_list, self.global_butt_list)  # При разрушении здания
            self.to_build.current_place = self.to_build  # указывается новое текущее здание: фундамент

            self.global_butt_list.remove(self.dialog.current_place)
            self.to_build.center_x, self.to_build.center_y = self.dialog.current_place.center_x, self.dialog.current_place.center_y
            for dialog in self.global_dialog_list:  # Установить текущее здание to build для всех окон dialoguebox
                dialog.current_place = self.to_build
            self.global_butt_list.append(self.to_build)
            self.dialog.active = False


class ScrollRect(ga.AdvancedButton):  # Доделать скролл перетягиванием мыши
    def __init__(self, x, y, width=15, height=100, text=""):
        super().__init__(x, y, width, height, text, theme=themes.scroll_theme)
        self.gde = 0
        self.shag = 0
        self.motion = False

    def on_update(self, delta_time):
        pass

    def check_mouse_press(self, x, y):
        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            return
        if y < self.center_y - self.height / 2:
            return
        self.on_press()

    def check_mouse_release(self, _x, _y):
        if self.pressed:
            self.on_release()

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.motion = False


class TabButton(ga.AdvancedButton):
    def __init__(self, dialogbox, tabs_list, id_building, x, y, width=40, height=20, text=''):
        super().__init__(x, y, width, height, text=text, theme=themes.theme_tabs)
        self.tabs_list = tabs_list
        self.id_building = id_building
        self.choice = False
        self.dialogbox = dialogbox

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            for k in self.tabs_list:
                if k.locked:
                    k.locked = False
            self.locked = True
            self.dialogbox.current_tab_choice = self.id_building
            self.dialogbox.how_scrolling = 0
            self.dialogbox.update()
