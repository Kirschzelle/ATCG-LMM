from elements import text_box as tb
import arcade

class TextBoxBundler():

    def __init__(self) -> None:
        self.tb_council = tb.TextBox(75,195,125,165,-9)
        self.tb_king = tb.TextBox(245,145,115,80,-15)
        self.tb_world = tb.TextBox(412,111,150,115,-10)
        self.tb_poebel = tb.TextBox(350,257,270,80,-7)
        self.tb_player = tb.TextBox(175,35,330,25,0)

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