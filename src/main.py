import arcade
import constants as c

class Main(arcade.Window):
    def __init__(self):
        super().__init__(title = c.NAME, fullscreen = False)
        self.game_state = c.RUNNING
        self.game_board = arcade.Sprite("assets/board.png", self.get_scaling(), self.get_size()[0]/2, self.get_size()[1]/2)
        self.background_color = arcade.csscolor.ANTIQUE_WHITE

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        if(self.game_state == c.RUNNING):
            arcade.draw_sprite(self.game_board, pixelated = True)

    def update(self, delta_time):
        pass

    def get_scaling(self):
        return min(self.get_size()[0]/480,self.get_size()[1]/270)

def run():
    game = Main()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    run()