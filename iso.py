"""
Example of displaying an isometric map.

Isometric maps aren't fully supported, and needs some additional work.

Isometric map created with Tiled Map Editor: https://www.mapeditor.org/
Tiles by Kenney: http://kenney.nl/assets/isometric-dungeon-tiles

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.isometric_example
"""

import arcade
import os
import mygame
import gui
import themes
import iso_func
import config

SPRITE_SCALING = 0.5

SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT
SCREEN_TITLE = "Isometric Map"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 0

MOVEMENT_SPEED = 5

TILE_WIDTH = 256
TILE_HEIGHT = 149
mh = 10  # self.my_map.height
mw = 10  # self.my_map.width


class Camera(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class City(arcade.Sprite):

    def __init__(self):
        super().__init__(filename=os.getcwd() + r"/resources/images/isometric_dungeon/city.png", scale=SPRITE_SCALING)


class Iso(arcade.View):

    def __init__(self, window):
        super().__init__()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.window = window
        self.tileS = 0, 0
        self.tileSS = 0, 0
        self.startX = 0
        self.startY = 0
        # Sprite lists
        self.all_sprites_list = None

        self.text_label_list = []

        # Set up the player
        self.player_sprite = None
        self.hightlight_sprite = None
        self.wall_list = None
        self.floor_list = None
        self.objects_list = None
        self.player_list = None
        self.hightlight_list = None
        self.pos_list = {}
        self.label_sprite = None
        self.view_bottom = 0
        self.view_left = 0
        self.my_map = None
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.mouse_pos = False
        self.mouse_move = False
        self.text_label = None
        self.door_button = None

    def setup(self):
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.objects_list = arcade.SpriteList()
        self.hightlight_list = arcade.SpriteList()

        # noinspection PyDeprecation
        self.my_map = arcade.read_tiled_map('./resources/tmx_maps/wayss.tmx', SPRITE_SCALING)
        # Set up the player
        self.player_sprite = Camera(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    0.01)
        self.hightlight_sprite = arcade.Sprite("./resources/images/isometric_dungeon/hightlight.png", SPRITE_SCALING)
        self.label_sprite = arcade.Sprite(os.getcwd() + r"/images/label.png", SPRITE_SCALING)

        self.text_label = arcade.gui.TextLabel("", 0, 0)
        self.text_label.active = False
        self.text_list.append(self.text_label)

        px, py = arcade.isometric_grid_to_screen(self.my_map.width // 2,
                                                 self.my_map.height // 2,
                                                 self.my_map.width,
                                                 self.my_map.height,
                                                 self.my_map.tilewidth,
                                                 self.my_map.tileheight)

        self.player_sprite.center_x = px * SPRITE_SCALING
        self.player_sprite.center_y = py * SPRITE_SCALING
        self.player_list.append(self.player_sprite)
        self.hightlight_list.append(self.hightlight_sprite)
        self.hightlight_list.append(self.label_sprite)

        iso_func.read_sprite_list(self.my_map.layers["floor"], self.floor_list)
        iso_func.read_sprite_list(self.my_map.layers["items"], self.wall_list)
        iso_func.read_sprite_list(self.my_map.layers["city"], self.objects_list)
        self.get_pos_list(self.objects_list)
        self.get_pos_list(self.wall_list)
        # Set the background color
        if self.my_map.backgroundcolor is None:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            arcade.set_background_color(self.my_map.backgroundcolor)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0
        self.door_button = gui.DoorButton(width=45, height=45, theme=themes.theme_door)
        self.button_list.append(self.door_button)

    def get_pos_list(self, list_to_add):
        for h in list_to_add:
            self.pos_list[iso_func.screen_to_isometric_grid(h.center_x, h.center_y)] = (h.center_x, h.center_y), h

    def on_draw(self):
        arcade.start_render()
        # super().on_draw()
        arcade.draw_text(f"({self.tileS})\n{self.tileSS}", 170, SCREEN_HEIGHT - 20, arcade.color.YELLOW, 12)
        self.floor_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.objects_list.draw()
        self.hightlight_list.draw()

        for text in self.text_list:
            text.draw()

        for butt in self.button_list:
            butt.draw()

        def tile_information():
            for j in self.floor_list:
                arcade.draw_text(f"({j.center_x}, {j.center_y})", j.center_x - 30,
                                 j.center_y - 10, arcade.color.BLUE, 12)
            for tile_x in range(self.my_map.width):
                for tile_y in range(self.my_map.height):
                    screen_x, screen_y = iso_func.get_screen_coordinates(tile_x, tile_y,
                                                                         self.my_map.width, self.my_map.height,
                                                                         self.my_map.tilewidth, self.my_map.tileheight)

                    arcade.draw_text(f"{tile_x}, {tile_y}",
                                     screen_x * SPRITE_SCALING, (screen_y * SPRITE_SCALING) + 10,
                                     arcade.color.RED, 12,
                                     width=200, align="center", anchor_x="center")

        def create_lines():
            g = arcade.create_isometric_grid_lines(self.my_map.width, self.my_map.height,
                                                   int(self.my_map.tilewidth * SPRITE_SCALING),
                                                   int(self.my_map.tileheight * SPRITE_SCALING),
                                                   arcade.color.WHITE_SMOKE, 1)
            g.draw()

        # tile_information()
        # create_lines()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        screen_x = x + self.view_left
        screen_y = y + self.view_bottom
        self.startX = x
        self.startY = y
        self.mouse_move = False
        iso_func.check_mouse_press_for_buttons(screen_x, screen_y, self.button_list)

        # print(self.view_left, self.view_bottom)

        def create_new_city():
            new_city = City()
            new_city.center_x = screen_x
            new_city.center_y = screen_y
            self.objects_list.append(new_city)
            self.pos_list[iso_func.screen_to_isometric_grid(new_city.center_x, new_city.center_y)] = (new_city.center_x,
                                                                                                      new_city.center_y), new_city
        # print(f"({x}, {y}) | ({screen_x}, {screen_y}) -> ()")

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_move = False

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)
        iso_func.check_mouse_release_for_buttons(x, y, self.button_list)
        # arcade.set_viewport(self.view_left,SCREEN_WIDTH + self.view_left,self.view_bottom,SCREEN_HEIGHT + self.view_bottom)
        # print(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        print(scroll_x, scroll_y, x, y)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        screen_x = x + self.view_left
        screen_y = y + self.view_bottom
        dif_x = self.startX - x
        dif_y = self.startY - y
        # print(f"Разница: {dif_x}, {dif_y}, {self.mouse_move}")
        self.tileS = (screen_x, screen_y)
        self.tileSS = iso_func.screen_to_isometric_grid(screen_x, screen_y)
        self.get_highlight(self.tileSS[0], self.tileSS[1])
        changed = False

        if self.mouse_move and dif_x > x:
            self.view_left -= self.startX - x
            changed = True

        if self.mouse_move and dif_x < x:
            self.view_left += self.startX - x
            changed = True

        if self.mouse_move and dif_y < y:
            self.view_bottom += self.startY - y
            changed = True

        if self.mouse_move and dif_y > y:
            self.view_bottom -= self.startY - y
            changed = True

        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
            # self.mouse_move=False

    def get_highlight(self, tileX, tileY):
        xt, yt = iso_func.get_screen_coordinates(tileX, tileY)
        self.hightlight_sprite.center_x = xt * SPRITE_SCALING
        self.hightlight_sprite.center_y = yt * SPRITE_SCALING
        for sprite_pos in self.pos_list:
            # print(self.door_button.active, self.door_button.center_x, self.door_button.center_y, self.door_button.pressed)
            if sprite_pos == self.tileSS:
                self.label_sprite.alpha = 255
                self.label_sprite.center_x = (xt + TILE_WIDTH - 27) * SPRITE_SCALING
                self.label_sprite.center_y = (yt - TILE_HEIGHT / 2 + 22) * SPRITE_SCALING
                self.text_label.text = f'{sprite_pos}'
                self.text_label.x = self.label_sprite.center_x
                self.text_label.y = self.label_sprite.center_y
                self.text_label.active = True
                self.door_button.center_x = xt * SPRITE_SCALING
                self.door_button.center_y = (yt * SPRITE_SCALING) + 50
                self.door_button.active = True
                return
            else:
                self.label_sprite.alpha = 0
                self.text_label.text = ''
                self.text_label.active = False
                self.door_button.active = True

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        elif key == arcade.key.F:  # НЕ РАБОТАЕТ ресайз GUI
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)
            # self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        elif key == arcade.key.G:
            game_view = mygame.MyGame(self.window)
            self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
            self.window.show_view(game_view)
            game_view.setup()

        elif key == arcade.key.K:
            self.window.set_viewport(100, SCREEN_WIDTH + 100, 100, SCREEN_HEIGHT + 100)

        # print(self.left_pressed, self.right_pressed, self.up_pressed, self.down_pressed)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):

        # Track if we need to change the viewport
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        changed = False
        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        self.player_sprite.update()
