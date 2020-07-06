import arcade
import os

theme_house = arcade.gui.Theme()
theme_house.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/house.png"
hover = os.getcwd() + r"/images/house_hover.png"
clicked = os.getcwd() + r"/images/house_clicked.png"
locked = os.getcwd() + r"/images/house_locked.png"
theme_house.add_button_textures(normal, hover, clicked, locked)

theme_attack = arcade.gui.Theme()
theme_attack.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/attack.png"
hover = os.getcwd() + r"/images/attack_click.png"
clicked = os.getcwd() + r"/images/attack_click.png"
locked = os.getcwd() + r"/images/attack_click.png"
theme_attack.add_button_textures(normal, clicked, hover, locked)

theme_mail = arcade.gui.Theme()
theme_mail.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/letter.png"
clicked = os.getcwd() + r"/images/letter_click.png"
locked = os.getcwd() + r"/images/letter_click.png"
theme_mail.add_button_textures(normal, clicked, locked)

theme_law = arcade.gui.Theme()
theme_law.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/pechat.png"
clicked = os.getcwd() + r"/images/pechat_click.png"
locked = os.getcwd() + r"/images/pechat_click.png"
theme_law.add_button_textures(normal, clicked, locked)

theme_found = arcade.gui.Theme()
theme_found.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/empty_place.png"
clicked = os.getcwd() + r"/images/empty_place.png"
theme_found.add_button_textures(normal, clicked)

theme_barracks = arcade.gui.Theme()
theme_barracks.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/barracks.png"
clicked = os.getcwd() + r"/images/barracks.png"
locked = os.getcwd() + r"/images/barracks.png"
theme_barracks.add_button_textures(normal, clicked, locked)

theme_building_button = arcade.gui.Theme()
theme_building_button.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/ButtBrown.png"
clicked = os.getcwd() + r"/images/ButtLightBrown.png"  # hover
locked = os.getcwd() + r"/images/ButtBrown_pressed.png"  # pressed
theme_building_button.add_button_textures(normal, clicked, locked)

theme_destroy_button = arcade.gui.Theme()  # Unused
theme_destroy_button.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/ButtBrown.png"
clicked = os.getcwd() + r"/images/ButtLightBrown.png"  # hover
locked = os.getcwd() + r"/images/ButtBrown_pressed.png"  # pressed
theme_destroy_button.add_button_textures(normal, clicked, locked)

theme_door = arcade.gui.Theme()
normal = os.getcwd() + r"/images/doors.png"
hover = os.getcwd() + r"/images/doors.png"
clicked = os.getcwd() + r"/images/doors.png"
locked = os.getcwd() + r"/images/doors.png"
theme_door.add_button_textures(normal, hover, clicked, locked)

theme = arcade.gui.Theme()
theme.set_font(24, arcade.color.WHITE)
normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
theme.add_button_textures(normal, hover, clicked, locked)

theme_textbox_button = arcade.gui.Theme()
theme_textbox_button.set_font(24, arcade.color.WHITE)
normal = os.getcwd() + r"/images/Brown.png"
clicked = os.getcwd() + r"/images/LightBrown.png"  # hover
locked = os.getcwd() + r"/images/LightBrown.png"  # pressed
theme_textbox_button.add_button_textures(normal, clicked, locked)

theme_tabs = arcade.gui.Theme()
normal = os.getcwd() + r"/images/tabs.png"
hover = os.getcwd() + r"/images/tab_hover.png"
clicked = os.getcwd() + r"/images/tab_clicked.png"  # hover
locked = os.getcwd() + r"/images/tab_locked.png"  # pressed
theme_tabs.add_button_textures(normal, hover, clicked, locked)

theme_text = arcade.gui.Theme()
theme.set_font(24, arcade.color.BLACK)

scroll_theme = arcade.gui.Theme()
normal = os.getcwd() + r"/images/scroll_rect.png"
scroll_theme.add_button_textures(normal)
