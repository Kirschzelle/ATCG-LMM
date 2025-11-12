import arcade
import constants as c
import elements.text_box_bundler as tbb
import elements.board as board
import elements.pause as pause
import core.chat_log as cl
import core.user_input as input

class Main(arcade.Window):
    def __init__(self):
        super().__init__(title = c.NAME, fullscreen = False)
        self.game_state = c.RUNNING
        self.background_color = arcade.csscolor.ANTIQUE_WHITE
        self._load_fonts()

    def setup(self):
        self.tb_bundler = tbb.TextBoxBundler()
        self.cl = cl.ChatLog()
        self.board = board.Board()
        self.pause = pause.Pause()

    def on_update(self, delta_time):
        if(self.game_state == c.RUNNING):
            self.tb_bundler.update(delta_time)
            self.board.update(delta_time)
        if(self.game_state == c.PAUSED):
            self.pause.update(delta_time)
        if(self.game_state == c.EXITED):
            arcade.exit()
            self.close()

    def on_draw(self):
        if(self.game_state != c.EXITED):
            self.clear()
            scale = self.get_scaling()

        if(self.game_state == c.RUNNING):
            self.tb_bundler.draw(scale)
            self.board.draw(scale)

        if(self.game_state == c.PAUSED):
            self.pause.draw(scale)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.game_state == c.RUNNING:
                self.game_state = c.PAUSED
            else:
                self.game_state =c.EXITED
        if self.game_state == c.PAUSED and key == arcade.key.SPACE:
            self.game_state = c.RUNNING
        if self.game_state == c.RUNNING:
            input.handle_user_input(key, modifiers, self.tb_bundler.tb_player, self.cl)

    def get_scaling(self):
        return min(self.get_size()[0]/c.NATIVE_W,self.get_size()[1]/c.NATIVE_H)
    
    def _load_fonts(self):
        arcade.load_font("assets/fonts/my_soul/MySoul-Regular.ttf")
        arcade.load_font("assets/fonts/rubik_glitch/RubikGlitch-Regular.ttf")
        arcade.load_font("assets/fonts/monoton/Monoton-Regular.ttf")

def run():
    game = Main()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    run()