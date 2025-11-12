import arcade
import math

class TextBox():

    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 angle = 0,
                 padding = 0,
                 font_size = 12,
                 font_name = "Arial",
                 text_color = arcade.color.BLACK,
                 bg_color = arcade.color.TRANSPARENT_BLACK,
                 write_speed = 20):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.padding = padding
        self.font_size = font_size
        self.font_name = font_name
        self.text_color = text_color
        self.bg_color = bg_color
        self.write_speed = write_speed

        self.target_text = ""
        self.current_text = ""
        self.char_progress = 0.0
        
    def set_text(self, text):
        self.target_text = text
        if not self.target_text.startswith(self.current_text):
            self.current_text = ""
            self.char_progress = 0.0

    def set_text_instant(self, text):
        self.target_text = text
        self.current_text = text
        self.char_progress = len(text)

    def append_text(self, text):
        self.set_text(self.target_text + text)

    def append_text_instant(self, text):
        self.set_text_instant(self.target_text + text)

    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def set_rotation(self, angle):
        self.angle = angle
    
    def skip_to_end(self):
        self.current_text = self.target_text
        self.char_progress = len(self.target_text)

    def is_finished(self):
        return self.current_text == self.target_text
    
    def update(self, delta_time):
        max_length = len(self.target_text)
        if len(self.current_text) < max_length:
            self.char_progress += self.write_speed * delta_time
            if(max_length < self.char_progress):
                self.char_progress = max_length
            target_length = int(self.char_progress)
            self.current_text = self.target_text[:target_length]

    def draw(self, scaling):
        screen_x = self.x * scaling
        screen_y = self.y * scaling
        screen_width = self.width * scaling
        screen_height = self.height * scaling
        screen_padding = self.padding * scaling
        screen_font_size = int(self.font_size * scaling)

        if True:
            available_width = self.width - 2 * self.padding
            available_height = self.height - 2 * self.padding

            lines = self._split_lines(self.current_text, available_width)

            temp_text = arcade.Text("Ay", 0, 0, font_size=self.font_size, font_name=self.font_name)
            line_height = temp_text.content_height

            max_lines = int(available_height / line_height)

            if len(lines) > max_lines:
                lines_to_remove = lines[:len(lines) - max_lines]
                lines_to_remove = '\n'.join(lines_to_remove)

                if self.target_text.startswith(lines_to_remove):
                    self.target_text = self.target_text[len(lines_to_remove):].lstrip('\n')
                
                if self.current_text.startswith(lines_to_remove):
                    self.current_text = self.current_text[len(lines_to_remove):].lstrip('\n')

                lines = lines[-max_lines:]
            
            total_text_height = len(lines) * line_height * scaling
            start_y_offset = -screen_height/2 + screen_padding + total_text_height - line_height * scaling

            if self.bg_color != arcade.color.TRANSPARENT_BLACK:
                half_width = screen_width / 2
                half_height = screen_height / 2
                angle_rad = math.radians(self.angle)
                cos_a = math.cos(angle_rad)
                sin_a = math.sin(angle_rad)
                
                corners = [
                    (-half_width, -half_height),
                    (half_width, -half_height),
                    (half_width, half_height),
                    (-half_width, half_height)
                ]
                
                rotated_corners = []
                for x, y in corners:
                    rotated_x = screen_x + (x * cos_a - y * sin_a)
                    rotated_y = screen_y + (x * sin_a + y * cos_a)
                    rotated_corners.append((rotated_x, rotated_y))
                
                arcade.draw_polygon_filled(rotated_corners, self.bg_color)
            
            for i, line in enumerate(lines):
                line_y_offset = start_y_offset - i * line_height * scaling
                
                angle_rad = math.radians(self.angle)
                rotated_x = line_y_offset * math.sin(angle_rad)
                rotated_y = line_y_offset * math.cos(angle_rad)
                
                arcade.draw_text(
                    line,
                    screen_x + rotated_x,
                    screen_y + rotated_y,
                    self.text_color,
                    screen_font_size,
                    anchor_x="left",
                    anchor_y="center",
                    font_name=self.font_name,
                    rotation=self.angle
                )

    def _split_lines(self, text, max_width):
        lines = []
        paragraphs = text.split('\n')

        for paragraph in paragraphs:
            if not paragraph:
                lines.append("")
                continue

        words = paragraph.split(' ')
        current_line = ""

        for word in words:
            test_line = current_line + (' ' if current_line else "") + word
            actual_width = self._get_text_width(test_line, self.font_size)

            if actual_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        return lines

    def _get_text_width(self, text, font_size):
        if not text:
            return 0
        
        temp_text = arcade.Text( # Note: We are creating a new object each time. This might not be the best for performance, but it was judged negligible in the game's scope.
            text,
            0,
            0,
            font_size=font_size,
            font_name=self.font_name
        )
        return temp_text.content_width

