import arcade
import os
import gui
import iso
import config
import time

SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT
MUSIC_VOLUME = config.MUSIC_VOLUME


def check_mouse_hover_for_buttons(x, y, button_list):  # Доработать, неправильно показывает границы
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        else:
            button.hover = False
        if x < button.center_x - button.width / 2:
            continue
        else:
            button.hover = False
        if y > button.center_y + button.height / 2:
            continue
        else:
            button.hover = False
        if y < button.center_y - button.height / 2:
            continue
        else:
            button.hover = False
        button.hover = True


class MyGame(arcade.View):
    def __init__(self, window):
        super().__init__()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcade.set_background_color(arcade.color.AMAZON)
        self.window = window
        self.pause = False
        self.text = "Medieval Game"
        self.background = None
        self.text_x = 0
        self.text_y = 300
        self.text_font_size = 40
        self.speed = 1
        self.theme = None
        self.theme_house = None
        self.theme_mail = None
        self.theme_law = None
        self.theme_found = None
        self.theme_button = None
        self.theme_attack = None
        self.dialoguebox = None
        self.gui_list = None
        self.line_shape = None
        self.res_list = None
        self.res_wood = None
        self.hijina = None
        self.place_for_building = None
        self.place_for_building2 = None
        self.count_res_list = []
        self.count_prod_list = []
        self.foundaments_list = []
        self.to_build = None
        self.half_width = None
        self.half_height = None
        self.current_song = 0
        self.music = None
        self.left = None
        self.screen_width = None
        self.bottom = None
        self.icon_res = None
        self.text_res = None
        self.screen_height = None
        self.gold = 0
        self.wood = 0
        self.iron = 0
        self.clay = 0
        self.food = 0
        self.food_prod = 0.2
        self.total_time = 0
        self.new_second = 0  # Как понять, что прошла секунда?
        self.scroll = 0
        self.how_scrolling = 0
        self.on_motion_scroll = False

    def setup(self):
        self.background = arcade.load_texture(os.getcwd() + r"/images/background.jpg")
        self.setup_theme()
        self.res_list = arcade.SpriteList()
        self.gui_list = arcade.SpriteList()
        self.set_gui()
        self.add_custom_dialoguebox()
        self.add_attack_menu()
        self.add_building_dialoguebox()
        self.set_buttons()
        self.draw_res_labels()
        self.music_list = [os.getcwd() + r"/music/main_theme.mp3", os.getcwd() + r"/music/road_home.mp3"]
        self.current_song = 0
        self.play_song()

    def on_draw(self):
        self.left, self.screen_width, self.bottom, self.screen_height = self.window.get_viewport()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.screen_width, self.screen_height, self.background)  # Задний фон
        self.gui_list.draw()
        self.res_list.draw()
        for res in self.count_res_list:
            res.draw()
        for prod in self.count_prod_list:
            prod.draw()
        for f in self.foundaments_list:
            f.draw()
        super().on_draw()

        position = self.music.get_stream_position()
        length = self.music.get_length()
        size = 12
        margin = size * .5

        y = SCREEN_HEIGHT - (size + margin)
        text = f"Текущая музыка: {self.music_list[self.current_song].split('/')[-1]}"
        arcade.draw_text(text, 0, y, arcade.csscolor.BLACK, size)

        y -= size + margin
        text = f"{int(position) // 60}:{int(position) % 60:02} из {int(length) // 60}:{int(length) % 60:02}"
        arcade.draw_text(text, 0, y, arcade.csscolor.BLACK, size)

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.res_update(delta_time)
        for d in self.foundaments_list:
            d.update()
        for d in self.dialogue_box_list:
            d.global_butt_list = self.foundaments_list
            d.global_dialog_list = self.dialogue_box_list

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:  # НЕ РАБОТАЕТ ресайз GUI
            # User hits f. Flip between full and not full screen.
            self.window.set_fullscreen(not self.window.fullscreen)
            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)
            self.top_nav.update_pos(width, height)
            self.sidebar_nav.update_pos(width, height)

        elif key == arcade.key.G:
            game_view = iso.Iso(self.window)
            game_view.setup()
            self.window.show_view(game_view)

        elif key == arcade.key.S:
            # User hits s. Flip between full and not full screen.
            self.window.set_fullscreen(not self.window.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        for f in self.foundaments_list:
            f.check_mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_release(x, y, button, modifiers)
        for f in self.foundaments_list:
            f.check_mouse_release(x, y)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        check_mouse_hover_for_buttons(x, y, self.dialoguebox3.button_list)
        check_mouse_hover_for_buttons(x, y, self.dialoguebox3.tabs_list)
        # for f in self.foundaments_list:  # Запихнуть глубже в ScrollRect, а пока и так сгодится
        # f.in_motion(y)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.dialogue_box_list[2].on_mouse_scroll(x, y, scroll_x, scroll_y)

    def setup_theme(self):
        self.theme = arcade.gui.Theme()
        self.theme.set_font(24, arcade.color.WHITE)
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        dialogue_box = os.getcwd() + r"/images/dialog.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)
        self.theme.add_dialogue_box_texture(dialogue_box)

    def set_buttons(self):
        width, height = self.window.get_size()
        self.place_for_building = gui.Foundament(self.dialogue_box_list, self.foundaments_list, (width / 2) + 100,
                                                 150)  # Поменять button_list на founmdament в классе
        self.place_for_building2 = gui.Foundament(self.dialogue_box_list, self.foundaments_list, (width / 2) - 200, 150)
        self.place_for_building.current_place = self.place_for_building  # Выбор к какому месту для строительства
        # подвязан dialoguebox
        self.place_for_building2.current_place = self.place_for_building2

        self.button_list.append(
            gui.AttackButton(self.dialogue_box_list, self.top_nav.center_x - 100, height - 55))
        self.button_list.append(
            gui.MailButton(self.dialogue_box_list, (width / 2), height - 55))
        self.button_list.append(
            gui.MapButton(self.dialogue_box_list, self.window, (width / 2) + 100, height - 55))

        # music_button = gui.MusicButton(self.music, 50, SCREEN_HEIGHT - 55)
        # self.button_list.append(music_button)
        self.foundaments_list.append(self.place_for_building)
        self.foundaments_list.append(self.place_for_building2)

    def set_gui(self):
        width, height = self.window.get_size()  # MAke unique self.width etc.

        self.top_nav = gui.MainNav(os.getcwd() + r"/images/top_bar.png")
        self.top_nav.center_x = width / 2
        self.top_nav.center_y = height - 67
        self.gui_list.append(self.top_nav)

        self.sidebar_nav = gui.SideNav(os.getcwd() + r"/images/side_bar.png")
        self.sidebar_nav.center_x = width - self.sidebar_nav.width / 2
        self.sidebar_nav.center_y = height / 2
        self.sidebar_nav.width_select = self.sidebar_nav.width
        self.gui_list.append(self.sidebar_nav)

    def draw_res_labels(self):
        i = 0
        for res in config.resourses:
            width_label = int(len(str(int(config.resourses[res][0]))) * 7.5)

            self.icon_res = arcade.Sprite(os.getcwd() + config.resourses[res][2], scale=0.8,
                                          center_x=self.sidebar_nav.left + 45,
                                          center_y=self.sidebar_nav.top - 60 - i * 30)

            self.text_res = arcade.gui.TextLabel(text=f'{float(config.resourses[res][0]):.0f}',
                                                 x=self.icon_res.center_x + 16,
                                                 y=self.icon_res.center_y, font_size=10, anchor_x='left')
            self.res_list.append(self.icon_res)
            self.count_res_list.append(self.text_res)
            self.count_prod_list.append(
                arcade.gui.TextLabel(text=f'+{float(config.resourses[res][1]):.1f}',
                                     x=self.text_res.x + width_label,
                                     y=self.text_res.y + 1, font_size=8, anchor_x='left', anchor_y='center',
                                     color=arcade.color.AVOCADO))
            i += 1

    def add_custom_dialoguebox(self):
        self.half_width = self.window.width / 2
        self.half_height = self.window.height / 2
        scaling_menu_box = 0.5
        self.dialoguebox = gui.MenuBox(self.half_width, self.half_height, 1000 * scaling_menu_box,
                                       800 * scaling_menu_box, theme=self.theme)
        self.dialogue_box_list.append(self.dialoguebox)

    def add_attack_menu(self):
        color = (220, 228, 255)
        dialoguebox2 = gui.MenuBox(self.half_width, self.half_height, self.half_width * 1.3,
                                   self.half_height * 1.6, color, self.theme)
        close_button2 = gui.CloseButton(dialoguebox2, self.half_width, self.half_height - (self.half_height / 2) + 40)
        dialoguebox2.button_list.append(close_button2)
        message = "Дом, уровень 2"
        dialoguebox2.text_list.append(
            arcade.gui.TextLabel(message, self.half_width - 100, self.half_height + 100, self.theme.font_color,
                                 bold=True, align='center'))
        self.dialogue_box_list.append(dialoguebox2)

    def add_building_dialoguebox(self):
        scaling_menu_box = 0.7
        self.dialoguebox3 = gui.MenuBox(self.half_width, self.half_height, 1000 * scaling_menu_box,
                                        800 * scaling_menu_box, theme=self.theme)

        self.dialogue_box_list.append(self.dialoguebox3)

    def res_update(self, delta_time):
        self.total_time += delta_time
        if self.total_time > self.new_second:  # Прошла секунда
            self.new_second += 1
            config.resourses['Древесина'][0] += config.resourses['Древесина'][1]
            config.resourses['Железо'][0] += config.resourses['Железо'][1]
            config.resourses['Еда'][0] += config.resourses['Еда'][1]
            config.resourses['Глина'][0] += config.resourses['Глина'][1]
            config.resourses['Деньги'][0] += config.resourses['Деньги'][1]

        self.wood = config.resourses['Древесина']
        self.iron = config.resourses['Железо']
        self.food = config.resourses['Еда']
        self.clay = config.resourses['Глина']
        self.gold = config.resourses['Деньги']
        local_res_list = [self.wood[0], self.iron[0], self.food[0], self.clay[0], self.gold[0]]
        local_prod_list = [self.wood[1], self.iron[1], self.food[1], self.clay[1], self.gold[1]]
        i = 0
        for text_res in self.count_res_list:
            text_res.text = f'{float(local_res_list[i]):.0f}'
            i += 1
        i = 0
        for text_prod in self.count_prod_list:
            if float(local_prod_list[i]) > 0:
                if str(float(local_prod_list[i])).split('.')[1] != '0':
                    text_prod.text = f'+{float(local_prod_list[i]):.1f}'
                else:
                    text_prod.text = f'+{float(local_prod_list[i]):.0f}'
            else:
                text_prod.text = ''
            text_prod.x = self.count_res_list[i].x + int(len(str(int(self.count_res_list[i].text))) * 7.5)
            i += 1

    def advance_song(self):
        self.current_song += 1
        if self.current_song >= len(self.music_list):
            self.current_song = 0
        print(f"Advancing song to {self.current_song}.")

    def play_song(self):
        if self.music:
            self.music.stop()

        print(f"Playing {self.music_list[self.current_song]}")
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(MUSIC_VOLUME)
        self.music.stop()
        time.sleep(0.03)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Medieval Game", fullscreen=False)
    main_view = MyGame(window)  # iso.Iso()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
