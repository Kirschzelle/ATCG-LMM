import arcade
import constants as c

x = c.NATIVE_W / 2
y = c.NATIVE_H / 2

class Board():

    def __init__(self) -> None:
        self.sprites = [
            arcade.Sprite("assets/sprites/board_1.png", center_x = x, center_y = y),
            arcade.Sprite("assets/sprites/board_2.png", center_x = x, center_y = y),
            arcade.Sprite("assets/sprites/board_3.png", center_x = x, center_y = y)
            ]
        self.current = 0
        self.time_passed = 0.0

    def update(self, delta_time):
        self.time_passed += delta_time
        if(self.time_passed > c.BOARD_SWITCH_EVERY):
            self.time_passed -= c.BOARD_SWITCH_EVERY
            self.current += 1

    def draw(self, scale):
        current_index = min(len(self.sprites) - 1, abs(self.current % len(self.sprites))) # In case we wrap around.
        self.sprites[current_index].center_x = x * scale
        self.sprites[current_index].center_y = y * scale
        self.sprites[current_index].scale = scale
        arcade.draw_sprite(self.sprites[current_index], pixelated = True)
