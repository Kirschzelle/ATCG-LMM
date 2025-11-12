from llm.council import get_council_response
import arcade
import constants as c
import elements.text_box_bundler as tbb

class Main(arcade.Window):
    def __init__(self):
        super().__init__(title = c.NAME, fullscreen = False)
        self.game_state = c.RUNNING
        self.game_board = arcade.Sprite("assets/board.png", self.get_scaling(), self.get_size()[0]/2, self.get_size()[1]/2)
        self.background_color = arcade.csscolor.ANTIQUE_WHITE

    def setup(self):
        self.tb_bundler = tbb.TextBoxBundler()

    def on_draw(self):
        self.clear()

        if(self.game_state == c.RUNNING):
            scale = self.get_scaling()
            self.tb_bundler.draw(scale)
            arcade.draw_sprite(self.game_board, pixelated = True)

    def update(self, delta_time):
        
        if(self.game_state == c.RUNNING):
            self.tb_bundler.update(delta_time)

    def get_scaling(self):
        return min(self.get_size()[0]/480,self.get_size()[1]/270)

def run():
    game = Main()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    run()