from elements import text_box as tb
import arcade
import constants as c

class TextBoxBundler():

    def __init__(self) -> None:
        self.tb_council = tb.TextBox(c.NATIVE_W*(75/480),c.NATIVE_H*(195/270),c.NATIVE_W*(125/480),c.NATIVE_H*(165/270),-9, line_spacing = 1.0, font_size=8)
        self.tb_king = tb.TextBox(c.NATIVE_W*(245/480),c.NATIVE_H*(145/270),c.NATIVE_W*(115/480),c.NATIVE_H*(80/270),-15, font_size=8)
        self.tb_world = tb.TextBox(c.NATIVE_W*(412/480),c.NATIVE_H*(111/270),c.NATIVE_W*(150/480),c.NATIVE_H*(115/270),-10)
        self.tb_poebel = tb.TextBox(c.NATIVE_W*(350/480),c.NATIVE_H*(257/270),c.NATIVE_W*(270/480),c.NATIVE_H*(80/270),-7)
        self.tb_player = tb.TextBox(c.NATIVE_W*(175/480),c.NATIVE_H*(35/270),c.NATIVE_W*(330/480),c.NATIVE_H*(25/270),0, font_name = "My Soul", prevent_overflow = False)
        #self.tb_council.set_text_instant("""[s:8]Hello! This is [c:RED]red text[c:BLACK].
#Now switching to [f:Courier New]monospace font[f:My Soul].
#Here's [c:BLUE][s:12]BIG BLUE TEXT[s:14][c:BLACK]!
#You can also use [c:255,0,255]RGB colors[c:BLACK].
#[c:GREEN]Green text with [s:18]different sizes[s:14]![c:BLACK]""")

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

    def add_message(self, sender, message):
        print(f"[DEBUG] Appendet message:\n-[Sender]{sender}\n-[Message]{message}")
        if sender == c.PLAYER:
            self.tb_council.append_text(f"\n[c:AFRICAN_VIOLET][f:My Soul]{sender}: {message}")
        elif sender == c.KING:
            self.tb_king.append_text(f"\n[c:GOLD][f:My Soul]{sender}: {message}")
        elif sender == c.GREEDY_BASTARD:
            self.tb_council.append_text(f"\n[c:OCEAN_BOAT_BLUE][f:Arial]{sender}: {message}")