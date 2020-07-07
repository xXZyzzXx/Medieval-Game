import arcade

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 0

MOVEMENT_SPEED = 5

TILE_WIDTH = 256
TILE_HEIGHT = 149
mh = 10  # self.my_map.height
mw = 10  # self.my_map.width


def cartToIso(cartX, cartY):
    isoX = (cartX - cartY)
    isoY = (cartX + cartY) / 2
    pos = (isoX, isoY)
    return pos


def get_screen_coordinates(tile_x, tile_y, width=mw, height=mh, tilewidth=TILE_WIDTH, tileheight=TILE_HEIGHT):
    screen_x = tilewidth * tile_x // 2 + height * tilewidth // 2 - tile_y * tilewidth // 2
    screen_y = (height - tile_y - 1) * tileheight // 2 + width * tileheight // 2 - tile_x * tileheight // 2
    return screen_x, screen_y


def screen_to_isometric_grid(cartX, cartY):
    screenx = mh - cartY / (TILE_HEIGHT * SPRITE_SCALING) + cartX / (TILE_WIDTH * SPRITE_SCALING) - mw / 2 - 1 / 2
    screeny = mh - cartY / (TILE_HEIGHT * SPRITE_SCALING) - cartX / (TILE_WIDTH * SPRITE_SCALING) + mw / 2 - 1 / 2
    screenx2 = round(screenx)
    screeny2 = round(screeny)
    return screenx2, screeny2


def read_sprite_list(grid, sprite_list):
    for row in grid:
        for grid_location in row:
            if grid_location.tile is not None:
                tile_sprite = arcade.Sprite("./resources/images/" + grid_location.tile.source, SPRITE_SCALING)
                tile_sprite.center_x = grid_location.center_x * SPRITE_SCALING
                tile_sprite.center_y = grid_location.center_y * SPRITE_SCALING
                sprite_list.append(tile_sprite)


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()
