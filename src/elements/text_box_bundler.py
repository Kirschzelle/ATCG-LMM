from elements import text_box as tb
import arcade

class TextBoxBundler():

    def __init__(self) -> None:
        self.tb_council = tb.TextBox(75,195,125,165,-9)
        self.tb_king = tb.TextBox(245,145,115,80,-15)
        self.tb_world = tb.TextBox(412,111,150,115,-10)
        self.tb_poebel = tb.TextBox(350,257,270,80,-7)
        self.tb_player = tb.TextBox(175,35,330,25,0, font_name="My Soul", prevent_overflow=False)
        self.tb_council.set_text_instant("""Hello! This is [c:RED]red text[c:BLACK].
Now switching to [f:Courier New]monospace font[f:Arial].
Here's [c:BLUE][s:20]BIG BLUE TEXT[s:14][c:BLACK]!
You can also use [c:255,0,255]RGB colors[c:BLACK].
[c:GREEN]Green text with [s:18]different sizes[s:14]![c:BLACK]""")

    def draw(self, scale):
        self.tb_council.draw(scale)
        self.tb_king.draw(scale)
        self.tb_world.draw(scale)
        self.tb_poebel.draw(scale)
        self.tb_player.draw(scale)

    def update(self, delta_time):
        self.tb_council.update(delta_time)
        self.tb_king.update(delta_time)
        self.tb_world.update(delta_time)
        self.tb_poebel.update(delta_time)
        self.tb_player.update(delta_time)