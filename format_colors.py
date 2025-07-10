from enum import Enum


# Set using the 256 Colors https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
class Color(Enum):
    ORANGE = 208
    BLUE = 45
    MAGENTA = 200
    RED = 196
    GREEN = 40


ANSI_ESCAPE = "\x1b"
MAIN_COLORS = {
    Color.ORANGE: "38;5;208",
    Color.BLUE: "38;5;45",
    Color.MAGENTA: "38;5;200",
    Color.RED: "38;5;196",
    Color.GREEN: "38;5;40",
}


def set_color(color: Color):
    if color not in MAIN_COLORS:
        return
    print(ANSI_ESCAPE + "[" + MAIN_COLORS[color] + "m")
    return


def reset_color():
    print(ANSI_ESCAPE + "[0m")


# Prints text in predefined color.
# color must be added/adjusted in format_colors.MAIN_COLORS
def fabulous_print(color: Color, text: str | None):
    if text is None:
        return
    set_color(color=color)
    print(text)
    reset_color()
    return
