import arcade
import constants as c
import elements.text_box as tb

default_color = "BLACK"
default_font = "Arial"
default_size = "24"

class Pause():
    def __init__(self):
        self.fonts = ["My Soul","Rubik Glitch", "Monoton"]
        self.text = tb.TextBox(c.NATIVE_W/2,c.NATIVE_H/2,c.NATIVE_W*0.75,c.NATIVE_H*0.6, prevent_overflow=False, line_spacing=1.2)
        self.current_time = c.BOARD_SWITCH_EVERY  + 0.1
        self.iteration = 0

    def update(self, delta_time):
        self.current_time += delta_time
        if self.current_time > c.BOARD_SWITCH_EVERY:
            self.current_time -= c.BOARD_SWITCH_EVERY
            self.iteration += 1

            index = min(len(self.fonts)-1,abs(self.iteration%len(self.fonts))) # prevent overflow bugs if game runs till the heatdeath of the universe
            self.text.set_text_instant("[f:"+default_font+"][c:"+default_color+"][s:"+default_size+"]             "
                "[f:"+self.fonts[(index+0)%len(self.fonts)]+"]P"
                "[f:"+self.fonts[(index+1)%len(self.fonts)]+"]a"
                "[f:"+self.fonts[(index+2)%len(self.fonts)]+"]u"
                "[f:"+self.fonts[(index+3)%len(self.fonts)]+"]s"
                "[f:"+self.fonts[(index+4)%len(self.fonts)]+"]e"
                "[f:"+self.fonts[(index+5)%len(self.fonts)]+"]d[f:"+default_font+"]"
                "\n[s:"+default_size+"]      Press[c:RED_DEVIL][f:Rubik Glitch][s:30] "
                "[f:"+self.fonts[(index+7)%len(self.fonts)]+"]E"
                "[f:"+self.fonts[(index+8)%len(self.fonts)]+"]S"
                "[f:"+self.fonts[(index+9)%len(self.fonts)]+"]C [s:"+default_size+"][f:"+default_font+"][c:"+default_color+"] to quit."
                "\n   [c:LIMERICK][f:Monoton][s:30] "
                "[f:"+self.fonts[(index+11)%len(self.fonts)]+"]S"
                "[f:"+self.fonts[(index+12)%len(self.fonts)]+"]p"
                "[f:"+self.fonts[(index+13)%len(self.fonts)]+"]a"
                "[f:"+self.fonts[(index+14)%len(self.fonts)]+"]c"
                "[f:"+self.fonts[(index+15)%len(self.fonts)]+"]e"
                " [s:"+default_size+"][f:"+default_font+"][c:"+default_color+"] to continue.")

        self.text.update(delta_time)

    def draw(self, scale):
        self.text.draw(scale)