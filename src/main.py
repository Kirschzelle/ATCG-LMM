import arcade
import constants as c
import elements.text_box_bundler as tbb
import elements.board as board
import elements.pause as pause
import core.chat_log as cl
import core.user_input as input
import os
from huggingface_hub import hf_hub_download

MODEL_REPO = "bartowski/Llama-3.2-3B-Instruct-GGUF"
MODEL_FILE = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
MODEL_PATH = os.path.join("models", MODEL_FILE)

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
    get_model()
    game = Main()
    game.setup()
    arcade.run()

def get_model():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found. Downloading {MODEL_FILE}...")
        os.makedirs("models", exist_ok=True)
        
        downloaded_path = hf_hub_download(
            repo_id=MODEL_REPO,
            filename=MODEL_FILE,
            local_dir="models"
        )
        print(f"Model downloaded to: {downloaded_path}")
    else:
        print(f"Model already exists at: {MODEL_PATH}")
    
    return MODEL_PATH

if __name__ == "__main__":
    run()