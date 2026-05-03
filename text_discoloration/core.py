import time
import random
import sys
import platform
import os

COLORS = {
    "red": "\033[91m",
    "dark_red": "\033[31m",
    "green": "\033[92m",
    "dark_green": "\033[32m",
    "yellow": "\033[93m",
    "dark_yellow": "\033[33m",
    "blue": "\033[94m",
    "dark_blue": "\033[34m",
    "purple": "\033[95m",
    "dark_purple": "\033[35m",
    "cyan": "\033[96m",
    "dark_cyan": "\033[36m",
    "white": "\033[97m",
    "gray": "\033[90m"
}
END = "\033[0m"
ALL_COLOR_POOL = list(COLORS.values())

if platform.system() == "Windows":
    os.system("reg add HKCU\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f")


def slow_print(text, delay=0.5):
    print(text)
    time.sleep(delay)


def typewriter(text, delay=0.05):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def color_typewriter(text, color="red", delay=0.05):
    use_color = COLORS.get(color, COLORS["white"])
    for ch in text:
        sys.stdout.write(use_color + ch)
        sys.stdout.flush()
        time.sleep(delay)
    print(END)


def random_typewriter(text, delay=0.05):
    for ch in text:
        ran_c = random.choice(ALL_COLOR_POOL)
        sys.stdout.write(ran_c + ch)
        sys.stdout.flush()
        time.sleep(delay)
    print(END)


def typewriter_red(text, delay=0.05):
    color_typewriter(text, color="red", delay=delay)

def typewriter_green(text, delay=0.05):
    color_typewriter(text, color="green", delay=delay)

def typewriter_yellow(text, delay=0.05):
    color_typewriter(text, color="yellow", delay=delay)

def typewriter_blue(text, delay=0.05):
    color_typewriter(text, color="blue", delay=delay)

def typewriter_purple(text, delay=0.05):
    color_typewriter(text, color="purple", delay=delay)

def typewriter_cyan(text, delay=0.05):
    color_typewriter(text, color="cyan", delay=delay)

def typewriter_white(text, delay=0.05):
    color_typewriter(text, color="white", delay=delay)

def typewriter_gray(text, delay=0.05):
    color_typewriter(text, color="gray", delay=delay)

def typewriter_dark_red(text, delay=0.05):
    color_typewriter(text, color="dark_red", delay=delay)

def typewriter_dark_green(text, delay=0.05):
    color_typewriter(text, color="dark_green", delay=delay)

def typewriter_dark_yellow(text, delay=0.05):
    color_typewriter(text, color="dark_yellow", delay=delay)

def typewriter_dark_blue(text, delay=0.05):
    color_typewriter(text, color="dark_blue", delay=delay)

def typewriter_dark_purple(text, delay=0.05):
    color_typewriter(text, color="dark_purple", delay=delay)

def typewriter_dark_cyan(text, delay=0.05):
    color_typewriter(text, color="dark_cyan", delay=delay)


def red_text(text):
    print(f"{COLORS['red']}{text}{END}")

def green_text(text):
    print(f"{COLORS['green']}{text}{END}")

def yellow_text(text):
    print(f"{COLORS['yellow']}{text}{END}")

def blue_text(text):
    print(f"{COLORS['blue']}{text}{END}")

def purple_text(text):
    print(f"{COLORS['purple']}{text}{END}")

def cyan_text(text):
    print(f"{COLORS['cyan']}{text}{END}")

def white_text(text):
    print(f"{COLORS['white']}{text}{END}")

def gray_text(text):
    print(f"{COLORS['gray']}{text}{END}")

def dark_red_text(text):
    print(f"{COLORS['dark_red']}{text}{END}")

def dark_green_text(text):
    print(f"{COLORS['dark_green']}{text}{END}")

def dark_yellow_text(text):
    print(f"{COLORS['dark_yellow']}{text}{END}")

def dark_blue_text(text):
    print(f"{COLORS['dark_blue']}{text}{END}")

def dark_purple_text(text):
    print(f"{COLORS['dark_purple']}{text}{END}")

def dark_cyan_text(text):
    print(f"{COLORS['dark_cyan']}{text}{END}")

__all__ = [
    "slow_print",
    "typewriter",
    "color_typewriter",
    "random_typewriter",
    "typewriter_red",
    "typewriter_green",
    "typewriter_yellow",
    "typewriter_blue",
    "typewriter_purple",
    "typewriter_cyan",
    "typewriter_white",
    "typewriter_gray",
    "typewriter_dark_red",
    "typewriter_dark_green",
    "typewriter_dark_yellow",
    "typewriter_dark_blue",
    "typewriter_dark_purple",
    "typewriter_dark_cyan",
    "red_text",
    "green_text",
    "yellow_text",
    "blue_text",
    "purple_text",
    "cyan_text",
    "white_text",
    "gray_text",
    "dark_red_text",
    "dark_green_text",
    "dark_yellow_text",
    "dark_blue_text",
    "dark_purple_text",
    "dark_cyan_text"
]
