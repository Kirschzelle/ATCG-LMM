import arcade
import constants as c
import elements.text_box as tb
import random

kb_sounds = [
    arcade.load_sound(f"assets/audio/kdeyboard_typing/{i:02}.wav")
    for i in range(1, 16)
]

def handle_user_input(key, modifiers, player_tb : tb.TextBox, cl):
    if key == arcade.key.BACKSPACE:
        player_tb.remove_one_instant()
        play_keyboard()
        return

    if key == arcade.key.ENTER:
        message = player_tb.get_current_text()
        player_tb.clear()
        cl.add_message(c.PEASANT, c.COUNCIL, message)
        # TODO: Handle player speaking events.
        play_keyboard()
        return

    input = _user_input_to_char(key, modifiers)

    if input is not None:
        player_tb.append_text_instant(input)
        play_keyboard()

def _user_input_to_char(key, modifiers=0):
    if arcade.key.A <= key <= arcade.key.Z:
        char = chr(ord('a') + (key - arcade.key.A))
        if modifiers & arcade.key.MOD_SHIFT:
            char = char.upper()
        return char
    
    if arcade.key.KEY_0 <= key <= arcade.key.KEY_9:
        if modifiers & arcade.key.MOD_SHIFT:
            shift_numbers = {
                arcade.key.KEY_0: ')',
                arcade.key.KEY_1: '!',
                arcade.key.KEY_2: '@',
                arcade.key.KEY_3: '#',
                arcade.key.KEY_4: '$',
                arcade.key.KEY_5: '%',
                arcade.key.KEY_6: '^',
                arcade.key.KEY_7: '&',
                arcade.key.KEY_8: '*',
                arcade.key.KEY_9: '(',
            }
            return shift_numbers.get(key)
        else:
            return str(key - arcade.key.KEY_0)
    
    if arcade.key.NUM_0 <= key <= arcade.key.NUM_9:
        return str(key - arcade.key.NUM_0)
    
    if key == arcade.key.SPACE:
        return ' '
    
    punctuation_map = {
        arcade.key.MINUS: '-',
        arcade.key.EQUAL: '=',
        arcade.key.BACKSLASH: '\\',
        arcade.key.SEMICOLON: ';',
        arcade.key.APOSTROPHE: "'",
        arcade.key.COMMA: ',',
        arcade.key.PERIOD: '.',
        arcade.key.SLASH: '/',
        arcade.key.GRAVE: '`',
    }
    
    punctuation_shift_map = {
        arcade.key.MINUS: '_',
        arcade.key.EQUAL: '+',
        arcade.key.BRACKETLEFT: '{',
        arcade.key.BRACKETRIGHT: '}',
        arcade.key.BACKSLASH: '|',
        arcade.key.SEMICOLON: ':',
        arcade.key.APOSTROPHE: '"',
        arcade.key.COMMA: '<',
        arcade.key.PERIOD: '>',
        arcade.key.SLASH: '?',
        arcade.key.GRAVE: '~',
    }
    
    if key in punctuation_map:
        if modifiers & arcade.key.MOD_SHIFT:
            return punctuation_shift_map.get(key, punctuation_map[key])
        return punctuation_map[key]
    
    numpad_map = {
        arcade.key.NUM_ADD: '+',
        arcade.key.NUM_SUBTRACT: '-',
        arcade.key.NUM_MULTIPLY: '*',
        arcade.key.NUM_DIVIDE: '/',
        arcade.key.NUM_DECIMAL: '.',
    }
    
    if key in numpad_map:
        return numpad_map[key]
    
    try:
        if 32 <= key <= 126:
            return chr(key)
    except:
        pass
    
    return None

def play_keyboard():
    index = random.randint(0, len(kb_sounds)-1)
    arcade.play_sound(kb_sounds[index])