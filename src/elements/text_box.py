import arcade
import math
import re

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
                 write_speed = 20,
                 prevent_overflow = True):
        
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
        self.prevent_overflow = prevent_overflow

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

    def remove_one(self):
        iterator = max(0,len(self.target_text)-1)
        text = self.target_text[:iterator]
        self.set_text(text)

    def remove_one_instant(self):
        iterator = max(0,len(self.target_text)-1)
        text = self.target_text[:iterator]
        self.set_text_instant(text)

    def get_current_text(self):
        return self.current_text

    def get_target_text(self):
        return self.target_text
    
    def clear(self):
        self.current_text = ""
        self.target_text = ""

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
            candidate_text = self.target_text[:target_length]
            
            open_bracket_pos = candidate_text.rfind('[')
            if open_bracket_pos != -1:
                close_bracket_pos = candidate_text.find(']', open_bracket_pos)
                if close_bracket_pos == -1:
                    full_close_pos = self.target_text.find(']', open_bracket_pos)
                    if full_close_pos != -1:
                        target_length = full_close_pos + 1

            self.current_text = self.target_text[:target_length]

    def draw(self, scaling):
        screen_x = self.x * scaling
        screen_y = self.y * scaling
        screen_width = self.width * scaling
        screen_height = self.height * scaling

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

        if self.current_text:
            available_width = self.width - 2 * self.padding
            available_height = self.height - 2 * self.padding

            segments = self._parse_format_codes(self.current_text)

            lines = self._split_lines(segments, available_width)

            line_heights = []
            for line_segments in lines:
                max_size_in_line = max((size for _, _, _, size in line_segments), default=self.font_size)
                temp_text = arcade.Text("Ay", 0, 0, font_size=max_size_in_line, font_name=self.font_name)
                line_heights.append(temp_text.content_height)

            total_text_height = sum(line_heights)

            lines_removed = 0
            while total_text_height > available_height and lines:
                lines.pop(0)
                removed_height = line_heights.pop(0)
                total_text_height -= removed_height
                lines_removed += 1

            if lines_removed > 0 and self.prevent_overflow:
                stripped_text = self._strip_format_codes(self.current_text)
                stripped_segments = [(stripped_text, self.text_color, self.font_name, self.font_size)]
                all_lines_stripped = self._split_lines(stripped_segments, available_width)
                
                if len(all_lines_stripped) > lines_removed:
                    lines_to_remove = []
                    for line_segments in all_lines_stripped[:lines_removed]:
                        line_text = ''.join(text for text, _, _, _ in line_segments)
                        lines_to_remove.append(line_text)
                    lines_to_remove_str = '\n'.join(lines_to_remove)
                    
                    clean_target = self._strip_format_codes(self.target_text)
                    if clean_target.startswith(lines_to_remove_str):
                        chars_to_remove = len(lines_to_remove_str) + lines_removed
                        
                        visible_count = 0
                        char_index = 0
                        while visible_count < chars_to_remove and char_index < len(self.target_text):
                            if self.target_text[char_index] == '[':
                                close_bracket = self.target_text.find(']', char_index)
                                if close_bracket != -1:
                                    char_index = close_bracket + 1
                                    continue
                            visible_count += 1
                            char_index += 1
                        
                        self.target_text = self.target_text[char_index:].lstrip('\n')
                    
                    clean_current = self._strip_format_codes(self.current_text)
                    if clean_current.startswith(lines_to_remove_str):
                        chars_to_remove = len(lines_to_remove_str) + lines_removed
                        
                        visible_count = 0
                        char_index = 0
                        while visible_count < chars_to_remove and char_index < len(self.current_text):
                            if self.current_text[char_index] == '[':
                                close_bracket = self.current_text.find(']', char_index)
                                if close_bracket != -1:
                                    char_index = close_bracket + 1
                                    continue
                            visible_count += 1
                            char_index += 1
                        
                        self.current_text = self.current_text[char_index:].lstrip('\n')
                    
            start_y = -self.height/2 + self.padding + total_text_height - (line_heights[0] if line_heights else 0)
            start_x = -self.width/2 + self.padding
            
            angle_rad = math.radians(self.angle)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            current_y_offset = 0
            for _, (line_segments, line_height) in enumerate(zip(lines, line_heights)):
                local_x = start_x
                local_y = start_y - current_y_offset
                
                local_x *= scaling
                local_y *= scaling
                
                rotated_x = local_x * cos_a - local_y * sin_a
                rotated_y = local_x * sin_a + local_y * cos_a
                
                current_x_offset = 0
                
                for text_seg, color, font, size in line_segments:
                    final_x = screen_x + rotated_x + current_x_offset
                    final_y = screen_y + rotated_y
                    
                    scaled_size = int(size * scaling)
                    
                    arcade.draw_text(
                        text_seg,
                        final_x,
                        final_y,
                        color,
                        scaled_size,
                        anchor_x="left",
                        anchor_y="bottom",
                        font_name=font,
                        rotation=-self.angle
                    )
                    
                    segment_width = self._get_text_width(text_seg, size, font)
                    current_x_offset += segment_width * scaling
                
                current_y_offset += line_height

    def _split_lines(self, segments, max_width):
        lines = []
        current_line = []
        current_line_width = 0

        for text_seg, color, font, size in segments:
            parts = text_seg.split('\n')
            
            for idx, part in enumerate(parts):
                if idx > 0:
                    if current_line:
                        lines.append(current_line)
                    current_line = []
                    current_line_width = 0
                
                if not part:
                    continue
                
                words = part.split(' ')
                for word_idx, word in enumerate(words):
                    if word_idx > 0:
                        space_width = self._get_text_width(' ', size, font)
                        test_width = current_line_width + space_width
                        
                        if test_width <= max_width:
                            if current_line and \
                            current_line[-1][1] == color and \
                            current_line[-1][2] == font and \
                            current_line[-1][3] == size:
                                current_line[-1] = (current_line[-1][0] + ' ', color, font, size)
                            else:
                                current_line.append((' ', color, font, size))
                            current_line_width = test_width
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = []
                            current_line_width = 0
                    
                    word_width = self._get_text_width(word, size, font)
                    test_width = current_line_width + word_width
                    
                    if test_width <= max_width or current_line_width == 0:
                        current_line.append((word, color, font, size))
                        current_line_width = test_width
                    else:
                        if word_width > max_width:
                            for char in word:
                                char_width = self._get_text_width(char, size, font)
                                if current_line_width + char_width <= max_width:
                                    current_line.append((char, color, font, size))
                                    current_line_width += char_width
                                else:
                                    if current_line:
                                        lines.append(current_line)
                                    current_line = [(char, color, font, size)]
                                    current_line_width = char_width
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = [(word, color, font, size)]
                            current_line_width = word_width
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def _get_text_width(self, text, font_size, font_name):
        if not text:
            return 0
        
        # Note: We are creating a new object each time. This might not be the best 
        # for performance, but it was judged negligible in the game's scope.
        temp_text = arcade.Text(
            text,
            0,
            0,
            font_size=font_size,
            font_name=font_name
        )
        return temp_text.content_width
    
    def _parse_format_codes(self, text):
        segments = []
        
        current_color = self.text_color
        current_font = self.font_name
        current_size = self.font_size
        
        pattern = r'\[([cfs]):([^\]]+)\]'
        
        last_end = 0
        for match in re.finditer(pattern, text):
            if match.start() > last_end:
                text_segment = text[last_end:match.start()]
                if text_segment:
                    segments.append((text_segment, current_color, current_font, current_size))
            
            code_type = match.group(1)
            code_value = match.group(2)
            
            if code_type == 'c':
                current_color = self._parse_color(code_value)
            elif code_type == 'f':
                current_font = code_value
            elif code_type == 's':
                try:
                    current_size = int(code_value)
                except ValueError:
                    pass
            
            last_end = match.end()
        
        if last_end < len(text):
            text_segment = text[last_end:]
            if text_segment:
                segments.append((text_segment, current_color, current_font, current_size))
        
        return segments

    def _parse_color(self, color_str):
        color_str = color_str.strip()
        
        if ',' in color_str:
            try:
                parts = [int(x.strip()) for x in color_str.split(',')]
                if len(parts) == 3:
                    return tuple(parts)
                elif len(parts) == 4:
                    return tuple(parts)
            except ValueError:
                pass
        
        try:
            return getattr(arcade.color, color_str.upper())
        except AttributeError:
            pass
        
        return self.text_color
    
    def _strip_format_codes(self, text):
        pattern = r'\[([cfs]):([^\]]+)\]'
        return re.sub(pattern, '', text)