import arcade
from typing import Tuple, Union


class AdvancedButton:  # Аналогичный класс arcade.gui.TextButton, но с корректировкой hover
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=8, font_face: Union[str, Tuple[str, ...]] = "Arial", font_color=None,
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2,
                 theme=None):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.pressed = False
        self.hover = False
        self.locked = False
        self.active = True
        self.button_height = button_height
        self.theme = theme
        self.font_color = font_color
        if self.theme:
            self.normal_texture = self.theme.button_textures['normal']
            self.hover_texture = self.theme.button_textures['hover']
            self.clicked_texture = self.theme.button_textures['clicked']
            self.locked_texture = self.theme.button_textures['locked']
            self.font_size = self.theme.font_size
            self.font_name = self.theme.font_name
            self.font_color = self.theme.font_color
        else:
            self.font_size = font_size
            self.font_face = font_face
            self.face_color = face_color
            self.highlight_color = highlight_color
            self.shadow_color = shadow_color
            self.font_name = font_face
        if self.font_color is None:
            self.font_color = self.face_color

    def draw_color_theme(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

    def draw_texture_theme(self):
        if self.pressed:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        elif self.hover:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.hover_texture)
        elif self.locked:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.locked_texture)
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)

    def draw(self):
        """ Draw the button """
        if self.theme:
            self.draw_texture_theme()
        else:
            self.draw_color_theme()

        arcade.draw_text(self.text, self.center_x, self.center_y,
                         self.font_color, font_size=self.font_size,
                         font_name=self.font_name,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        pass

    def on_release(self):
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

    def check_mouse_hover(self, x, y):
        if x > self.center_x + self.width / 2:
            return
        if x < self.center_x - self.width / 2:
            return
        if y > self.center_y + self.height / 2:
            return
        if y < self.center_y - self.height / 2:
            return
        self.hover = True

    def check_mouse_release(self, _x, _y):
        if self.pressed:
            self.on_release()