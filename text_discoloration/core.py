import time
import random
import sys
import os
import platform



RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK = "\033[90m"
END = "\033[0m"



if platform.system() == "Windows":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass



def info(text):
    print(f"{BLUE}[INFO]{END} {text}")

def success(text):
    print(f"{GREEN}[SUCCESS]{END} {text}")

def error(text):
    print(f"{RED}[ERROR]{END} {text}")

def warn(text):
    print(f"{YELLOW}[WARNING]{END} {text}")



def color_print_red(text):
    print(RED + text + END)

def color_print_green(text):
    print(GREEN + text + END)

def color_print_yellow(text):
    print(YELLOW + text + END)

def color_print_blue(text):
    print(BLUE + text + END)

def color_print_purple(text):
    print(PURPLE + text + END)

def color_print_cyan(text):
    print(CYAN + text + END)

def color_print_white(text):
    print(WHITE + text + END)

def color_print_black(text):
    print(BLACK + text + END)



def slow_print(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()



def typewriter(text, delay=0.05):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def color_typewriter(text, color, delay=0.05):
    color_code = globals().get(color.upper(), WHITE)
    for char in text:
        print(color_code + char + END, end="", flush=True)
        time.sleep(delay)
    print()



def typewriter_red(text, delay=0.05):
    color_typewriter(text, "red", delay)

def typewriter_green(text, delay=0.05):
    color_typewriter(text, "green", delay)

def typewriter_yellow(text, delay=0.05):
    color_typewriter(text, "yellow", delay)

def typewriter_blue(text, delay=0.05):
    color_typewriter(text, "blue", delay)

def typewriter_purple(text, delay=0.05):
    color_typewriter(text, "purple", delay)

def typewriter_cyan(text, delay=0.05):
    color_typewriter(text, "cyan", delay)

def typewriter_white(text, delay=0.05):
    color_typewriter(text, "white", delay)

def typewriter_black(text, delay=0.05):
    color_typewriter(text, "black", delay)



def random_typewriter(text, delay=0.05):
    color_codes = [RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE, BLACK]
    for char in text:
        color = random.choice(color_codes)
        print(color + char + END, end="", flush=True)
        time.sleep(delay)
    print()




def rgb_to_ansi(r, g, b):

    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        return f"\033[38;2;{r};{g};{b}m"
    return WHITE

def custom_print(text, color_code=None, r=None, g=None, b=None):
    if color_code:
        ansi_code = color_code
    elif r is not None and g is not None and b is not None:
        ansi_code = rgb_to_ansi(r, g, b)
    else:
        ansi_code = WHITE
    print(ansi_code + text + END)

def custom_typewriter(text, delay=0.05, color_code=None, r=None, g=None, b=None):
    if color_code:
        ansi_code = color_code
    elif r is not None and g is not None and b is not None:
        ansi_code = rgb_to_ansi(r, g, b)
    else:
        ansi_code = WHITE
    for char in text:
        print(ansi_code + char + END, end="", flush=True)
        time.sleep(delay)
    print()


__all__ = [
    "info", "success", "error", "warn",
    "color_print_red", "color_print_green", "color_print_yellow",
    "color_print_blue", "color_print_purple", "color_print_cyan",
    "color_print_white", "color_print_black",
    "slow_print", "typewriter",
    "color_typewriter",
    "typewriter_red", "typewriter_green", "typewriter_yellow",
    "typewriter_blue", "typewriter_purple", "typewriter_cyan",
    "typewriter_white", "typewriter_black",
    "random_typewriter",
    "rgb_to_ansi", "custom_print", "custom_typewriter",
    "RED", "GREEN", "YELLOW", "BLUE", "PURPLE", "CYAN", "WHITE", "BLACK", "END"
]