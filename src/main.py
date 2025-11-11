import arcade
import constants as c

class Main(arcade.Window):
    def __init__(self):
        super().__init__(title = c.NAME, fullscreen = True)

    def setup(sefl):
        pass

    def on_draw(self):
        pass

    def update(self, delta_time):
        pass

def run():
    game = Main()
    game.setup()
    arcade.run()