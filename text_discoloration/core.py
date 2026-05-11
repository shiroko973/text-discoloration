import os
import time
import random
import sys
import re
import platform
import threading
import hashlib
import base64
from datetime import datetime
from pathlib import Path
import secrets

__version__ = "3.0.1"


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK = "\033[90m"
END = "\033[0m"

def ra_key(length=20, no_letter=False, no_num=False, no_symbol=False):
    upper_pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_pool = 'abcdefghijklmnopqrstuvwxyz'
    num_pool = '0123456789'
    symbol_pool = '!@#$%^&*_+-=[]{}|;:,.<>?'

    pool = ''
    if not no_letter:
        pool += upper_pool + lower_pool
    if not no_num:
        pool += num_pool
    if not no_symbol:
        pool += symbol_pool

    if not pool:
        return "[错误] 至少选择一种字符类型"

    return ''.join(secrets.choice(pool) for _ in range(length))

COLOR_MAP = {
    'red': RED, 'green': GREEN, 'yellow': YELLOW,
    'blue': BLUE, 'purple': PURPLE, 'cyan': CYAN,
    'white': WHITE, 'black': BLACK
}

_enabled = True
_force_color = False


_quiet = False


def set_quiet():
    global _quiet
    _quiet = True


def set_verbose():
    global _quiet
    _quiet = False


def is_quiet():
    return _quiet


def _is_tty():
    if _force_color:
        return True
    try:
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    except Exception:
        return False


def enable():
    global _enabled
    _enabled = True


def disable():
    global _enabled
    _enabled = False


def force_color():
    global _force_color
    _force_color = True


def _setup_windows_console():
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


_already_setup = False


def _lazy_setup():
    global _already_setup
    if not _already_setup:
        _setup_windows_console()
        _already_setup = True


def _resolve_color(color=None, r=None, g=None, b=None):
    if color is not None and color.lower() in COLOR_MAP:
        return COLOR_MAP[color.lower()]
    if r is not None and g is not None and b is not None:
        return f"\033[38;2;{r};{g};{b}m"
    return WHITE


def _str_texts(texts):
    return [str(t) for t in texts]


def _print_color(ansi, texts, sep, end):
    parts = []
    for t in texts:
        parts.append(f"{ansi}{t}{END}")
    print(sep.join(parts), end=end)


def _write_color(ansi, texts, delay, sep, end):
    for i, text in enumerate(texts):
        for ch in text:
            sys.stdout.write(f"{ansi}{ch}{END}")
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
        if i < len(texts) - 1:
            sys.stdout.write(sep)
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()



def info(*texts, sep=' ', end='\n'):
    if _quiet:
        return
    _lazy_setup()
    texts = _str_texts(texts)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    prefix = f"{BLUE}[INFO]{END} "
    print(prefix + sep.join(str(t) for t in texts), end=end)


def success(*texts, sep=' ', end='\n'):
    if _quiet:
        return
    _lazy_setup()
    texts = _str_texts(texts)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    prefix = f"{GREEN}[SUCCESS]{END} "
    print(prefix + sep.join(str(t) for t in texts), end=end)


def error(*texts, sep=' ', end='\n'):
    if _quiet:
        return
    _lazy_setup()
    texts = _str_texts(texts)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    prefix = f"{RED}[ERROR]{END} "
    print(prefix + sep.join(str(t) for t in texts), end=end)


def warn(*texts, sep=' ', end='\n'):
    if _quiet:
        return
    _lazy_setup()
    texts = _str_texts(texts)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    prefix = f"{YELLOW}[WARNING]{END} "
    print(prefix + sep.join(str(t) for t in texts), end=end)



def _color_print_factory(color_name):
    ansi = COLOR_MAP[color_name]
    def func(*texts, sep=' ', end='\n'):
        if _quiet:
            print(*texts, sep=sep, end=end)
            return
        _lazy_setup()
        texts = _str_texts(texts)
        if not _enabled or not _is_tty():
            print(*texts, sep=sep, end=end)
            return
        _print_color(ansi, texts, sep, end)
    return func


color_print_red = _color_print_factory('red')
color_print_green = _color_print_factory('green')
color_print_yellow = _color_print_factory('yellow')
color_print_blue = _color_print_factory('blue')
color_print_purple = _color_print_factory('purple')
color_print_cyan = _color_print_factory('cyan')
color_print_white = _color_print_factory('white')
color_print_black = _color_print_factory('black')



def slow_print(*texts, delay=0.05, sep=' ', end='\n'):
    typewriter(*texts, delay=delay, sep=sep, end=end)


def typewriter(*texts, delay=0.05, sep=' ', end='\n'):
    if _quiet:
        print(*texts, sep=sep, end=end)
        return
    _lazy_setup()
    texts = _str_texts(texts)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    for i, text in enumerate(texts):
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
        if i < len(texts) - 1:
            sys.stdout.write(sep)
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def color_typewriter(color, *texts, delay=0.05, sep=' ', end='\n'):
    if _quiet:
        print(*texts, sep=sep, end=end)
        return
    _lazy_setup()
    texts = _str_texts(texts)
    ansi = _resolve_color(color=color)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    _write_color(ansi, texts, delay, sep, end)


def _typewriter_color_factory(color_name):
    def func(*texts, delay=0.05, sep=' ', end='\n'):
        color_typewriter(color_name, *texts, delay=delay, sep=sep, end=end)
    func.__name__ = f"typewriter_{color_name}"
    return func


typewriter_red = _typewriter_color_factory('red')
typewriter_green = _typewriter_color_factory('green')
typewriter_yellow = _typewriter_color_factory('yellow')
typewriter_blue = _typewriter_color_factory('blue')
typewriter_purple = _typewriter_color_factory('purple')
typewriter_cyan = _typewriter_color_factory('cyan')
typewriter_white = _typewriter_color_factory('white')
typewriter_black = _typewriter_color_factory('black')


def random_typewriter(*texts, delay=0.05, sep=' ', end='\n'):
    if _quiet:
        print(*texts, sep=sep, end=end)
        return
    _lazy_setup()
    texts = _str_texts(texts)
    color_codes = list(COLOR_MAP.values())
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    for i, text in enumerate(texts):
        for ch in text:
            color = random.choice(color_codes)
            sys.stdout.write(f"{color}{ch}{END}")
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
        if i < len(texts) - 1:
            sys.stdout.write(sep)
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()



def rgb_to_ansi(r, g, b):
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        return f"\033[38;2;{r};{g};{b}m"
    return WHITE


def custom_print(*texts, color=None, r=None, g=None, b=None, sep=' ', end='\n'):
    if _quiet:
        print(*texts, sep=sep, end=end)
        return
    _lazy_setup()
    texts = _str_texts(texts)
    ansi = _resolve_color(color=color, r=r, g=g, b=b)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    _print_color(ansi, texts, sep, end)


def custom_typewriter(*texts, delay=0.05, color=None, r=None, g=None, b=None, sep=' ', end='\n'):
    if _quiet:
        print(*texts, sep=sep, end=end)
        return
    _lazy_setup()
    texts = _str_texts(texts)
    ansi = _resolve_color(color=color, r=r, g=g, b=b)
    if not _enabled or not _is_tty():
        print(*texts, sep=sep, end=end)
        return
    _write_color(ansi, texts, delay, sep, end)



def gradient_text(text, start_rgb, end_rgb, delay=0.05, end='\n'):
    if _quiet:
        print(text, end=end)
        return
    _lazy_setup()
    text = str(text)
    if not _enabled or not _is_tty():
        print(text, end=end)
        return
    n = len(text)
    r1, g1, b1 = start_rgb
    r2, g2, b2 = end_rgb
    for i, ch in enumerate(text):
        if n == 1:
            r, g, b = r1, g1, b1
        else:
            r = int(r1 + (r2 - r1) * i / (n - 1))
            g = int(g1 + (g2 - g1) * i / (n - 1))
            b = int(b1 + (b2 - b1) * i / (n - 1))
        ansi = rgb_to_ansi(r, g, b)
        sys.stdout.write(f"{ansi}{ch}{END}")
        sys.stdout.flush()
        if delay:
            time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def rainbow_text(text, delay=0.05, end='\n'):
    if _quiet:
        print(text, end=end)
        return
    _lazy_setup()
    text = str(text)
    if not _enabled or not _is_tty():
        print(text, end=end)
        return
    colors = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0),
        (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
    ]
    for i, ch in enumerate(text):
        r, g, b = colors[i % len(colors)]
        ansi = rgb_to_ansi(r, g, b)
        sys.stdout.write(f"{ansi}{ch}{END}")
        sys.stdout.flush()
        if delay:
            time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()



def binary_output(*texts, sep=' ', end='\n', color=None):
    if _quiet:
        out_str = sep.join(format(ord(ch), '08b') for t in texts for ch in str(t))
        print(out_str, end=end)
        return
    _lazy_setup()
    texts = _str_texts(texts)
    parts = []
    for t in texts:
        for ch in t:
            parts.append(format(ord(ch), '08b'))
    out_str = sep.join(parts)
    if color and color.lower() in COLOR_MAP:
        if _enabled and _is_tty():
            ansi = COLOR_MAP[color.lower()]
            print(f"{ansi}{out_str}{END}", end=end)
            return
    print(out_str, end=end)


def binary_text(binary_str, sep=' ', end='\n', color="cyan"):
    if _quiet:
        clean = binary_str.replace(' ', '').replace('\n', '')
        if not all(c in '01' for c in clean):
            return None
        if len(clean) % 8 != 0:
            return None
        result = ''
        for i in range(0, len(clean), 8):
            byte = clean[i:i+8]
            char_code = int(byte, 2)
            result += chr(char_code)
        print(result, end=end)
        return result
    _lazy_setup()
    clean = binary_str.replace(' ', '').replace('\n', '')
    if not all(c in '01' for c in clean):
        error(f"无效的二进制字符串: {binary_str[:50]}...")
        return None
    if len(clean) % 8 != 0:
        error(f"二进制长度 {len(clean)} 不是 8 的倍数")
        return None
    result = ''
    for i in range(0, len(clean), 8):
        byte = clean[i:i+8]
        char_code = int(byte, 2)
        result += chr(char_code)
    color_func = globals().get(f"color_print_{color}")
    if color_func:
        color_func(result, end=end)
    else:
        print(result, end=end)
    return result


def text_to_binary(text, sep=' ', end='\n', color=None):
    binary = sep.join(format(ord(c), '08b') for c in str(text))
    if _quiet:
        print(binary, end=end)
        return binary
    _lazy_setup()
    if color and color in COLOR_MAP:
        ansi = COLOR_MAP[color]
        print(f"{ansi}{binary}{END}", end=end)
    else:
        print(binary, end=end)
    return binary


def binary_exec(binary_str, safe_mode=True, quiet=False, color="cyan", show_return=False):
    actual_quiet = quiet or _quiet
    if not actual_quiet:
        info("解析二进制中...")
    code = binary_text(binary_str, end='', color=color)
    if code is None:
        return None
    print()
    if not actual_quiet:
        color_func = globals().get(f"color_print_{color}")
        if color_func:
            color_func(f"解析结果: {code[:100]}")
    if not actual_quiet:
        success("正在执行...")
    if safe_mode:
        safe_builtins = {
            'print': print, 'len': len, 'str': str,
            'int': int, 'float': float, 'bool': bool,
            'list': list, 'dict': dict, 'tuple': tuple,
            'range': range, 'input': input,
        }
        dangerous_patterns = [
            r'\bimport\b', r'\bexec\b', r'\beval\b',
            r'__', r'\bopen\b', r'\bfile\b',
            r'\bos\.', r'\bsys\.', r'\bsubprocess\b'
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                if not actual_quiet:
                    error(f"安全模式拒绝执行: 包含危险关键词 '{pattern}'")
                return None
    try:
        if safe_mode:
            exec(code, {'__builtins__': safe_builtins}, {})
        else:
            exec(code)
        if not actual_quiet:
            success("执行完成")
        return code if show_return else None
    except Exception as e:
        if not actual_quiet:
            error(f"执行失败: {e}")
        return None


def binary_from_file(filepath, color="cyan"):
    if _quiet:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                binary_str = f.read().strip()
            return binary_text(binary_str, color=color)
        except Exception:
            return None
    _lazy_setup()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            binary_str = f.read().strip()
        return binary_text(binary_str, color=color)
    except Exception as e:
        error(f"读取文件失败: {e}")
        return None


def binary_to_file(content, filepath, mode='w'):
    if _quiet:
        try:
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(str(content))
            return True
        except Exception:
            return False
    _lazy_setup()
    try:
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(str(content))
        success(f"已写入 {filepath}")
        return True
    except Exception as e:
        error(f"写入文件失败: {e}")
        return False


def binary_exec_file(filepath, safe_mode=True, quiet=False, color="cyan", show_return=False):
    actual_quiet = quiet or _quiet
    if not actual_quiet:
        info("从文件读取二进制...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            binary_str = f.read().strip()
        return binary_exec(binary_str, safe_mode=safe_mode, quiet=actual_quiet, color=color, show_return=show_return)
    except Exception as e:
        if not actual_quiet:
            error(f"读取文件失败: {e}")
        return None



def title_box(text, width=50, char='=', color=None):
    if _quiet:
        line = char * width
        padding = max(0, (width - len(str(text)) - 2) // 2)
        print(line)
        print(f"{' ' * padding}{text}{' ' * (width - len(str(text)) - padding)}")
        print(line)
        return
    _lazy_setup()
    text = str(text)
    padding = max(0, (width - len(text) - 2) // 2)
    line = char * width
    if color and color in COLOR_MAP:
        ansi = COLOR_MAP[color]
        print(f"{ansi}{line}{END}")
        print(f"{ansi}{' ' * padding}{text}{' ' * (width - len(text) - padding)}{END}")
        print(f"{ansi}{line}{END}")
    else:
        print(line)
        print(f"{' ' * padding}{text}{' ' * (width - len(text) - padding)}")
        print(line)


def separator(char='-', width=None, color=None):
    if _quiet:
        if width is None:
            try:
                width = os.get_terminal_size().columns
            except:
                width = 80
        line = char * min(width, 200)
        print(line)
        return
    _lazy_setup()
    if width is None:
        try:
            width = os.get_terminal_size().columns
        except:
            width = 80
    line = char * min(width, 200)
    if color and color in COLOR_MAP:
        ansi = COLOR_MAP[color]
        print(f"{ansi}{line}{END}")
    else:
        print(line)


def table(data, headers=None, border=True, header_color=None, align="left"):
    if _quiet:
        for row in data:
            print(' | '.join(str(cell) for cell in row))
        return
    _lazy_setup()
    if not data:
        return
    if headers is None:
        headers = data[0]
        rows = data[1:]
    else:
        rows = data
    def format_cell(cell, width, align):
        cell_str = str(cell)
        if align == "left":
            return cell_str.ljust(width)
        elif align == "right":
            return cell_str.rjust(width)
        else:
            return cell_str.center(width)
    col_widths = []
    for i in range(len(headers)):
        max_width = len(str(headers[i]))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)
    def print_line():
        line = '+' + '+'.join('-' * w for w in col_widths) + '+'
        if border:
            print(line)
    if border:
        print_line()
    header_cells = []
    for i, h in enumerate(headers):
        header_cells.append(" " + format_cell(h, col_widths[i] - 1, align))
    header_line = '|' + '|'.join(header_cells) + '|'
    if header_color and header_color in COLOR_MAP:
        ansi = COLOR_MAP[header_color]
        print(f"{ansi}{header_line}{END}")
    else:
        print(header_line)
    if border:
        print_line()
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            if i < len(col_widths):
                cells.append(" " + format_cell(cell, col_widths[i] - 1, align))
            else:
                cells.append(" " + str(cell))
        while len(cells) < len(col_widths):
            cells.append(" " + " " * (col_widths[len(cells)] - 1))
        row_line = '|' + '|'.join(cells) + '|'
        print(row_line)
    if border:
        print_line()


def tree(data, prefix="", color=None, indent_char="  "):
    if _quiet:
        def _print_tree(d, p):
            if isinstance(d, dict):
                for k, v in d.items():
                    print(f"{p}{k}")
                    _print_tree(v, p + indent_char)
            elif isinstance(d, list):
                for item in d:
                    _print_tree(item, p)
            else:
                print(f"{p}{d}")
        _print_tree(data, prefix)
        return
    _lazy_setup()
    if isinstance(data, dict):
        items = list(data.items())
        for i, (key, value) in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            node_str = f"{prefix}{connector}{key}"
            if color and color in COLOR_MAP:
                ansi = COLOR_MAP[color]
                print(f"{ansi}{node_str}{END}")
            else:
                print(node_str)
            new_prefix = prefix + (indent_char + "    " if is_last else indent_char + "│   ")
            tree(value, new_prefix, color, indent_char)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            is_last = (i == len(data) - 1)
            connector = "└── " if is_last else "├── "
            node_str = f"{prefix}{connector}{item}"
            if color and color in COLOR_MAP:
                ansi = COLOR_MAP[color]
                print(f"{ansi}{node_str}{END}")
            else:
                print(node_str)
            if isinstance(item, (dict, list)):
                new_prefix = prefix + (indent_char + "    " if is_last else indent_char + "│   ")
                tree(item, new_prefix, color, indent_char)
    else:
        node_str = f"{prefix}{data}"
        if color and color in COLOR_MAP:
            ansi = COLOR_MAP[color]
            print(f"{ansi}{node_str}{END}")
        else:
            print(node_str)



class Live:
    def __init__(self, text="", delay=0.05):
        _lazy_setup()
        self.text = text
        self.delay = delay
        self._stop = False
        self._thread = None
    
    def update(self, text):
        self.text = text
        sys.stdout.write(f"\r{self.text}")
        sys.stdout.flush()
    
    def start(self):
        self._stop = False
        def _run():
            while not self._stop:
                sys.stdout.write(f"\r{self.text}")
                sys.stdout.flush()
                time.sleep(self.delay)
        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()
    
    def stop(self):
        self._stop = True
        if self._thread:
            self._thread.join(timeout=0.5)
        sys.stdout.write("\r" + " " * len(self.text) + "\r")
        sys.stdout.flush()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()


def live(text="", delay=0.05):
    return Live(text, delay)



def highlight(text, keywords, color="yellow", case_sensitive=False):
    if _quiet:
        print(text)
        return text
    _lazy_setup()
    if isinstance(keywords, str):
        keywords = [keywords]
    ansi = COLOR_MAP.get(color.lower(), YELLOW)
    result = text
    flags = 0 if case_sensitive else re.IGNORECASE
    for keyword in keywords:
        pattern = re.escape(keyword)
        result = re.sub(f"({pattern})", f"{ansi}\\1{END}", result, flags=flags)
    print(result)
    return result



def progress_bar(percent, width=50, fill='█', empty='░', color=None, show_percent=True, auto_end=False):
    percent = min(100, max(0, percent))
    filled = int(width * percent / 100)
    bar = fill * filled + empty * (width - filled)
    if not _quiet and color and color in COLOR_MAP:
        ansi = COLOR_MAP[color]
        bar = f"{ansi}{bar}{END}"
    if show_percent:
        print(f"\r{bar} {percent:.1f}%", end='', flush=True)
    else:
        print(f"\r{bar}", end='', flush=True)
    if auto_end and percent >= 100:
        print()


def spinner(text="Loading", delay=0.1, duration=None):
    _lazy_setup()
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    stop_flag = False
    def stop():
        nonlocal stop_flag
        stop_flag = True
    def spin():
        i = 0
        while not stop_flag:
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{frame} {text}...")
            sys.stdout.flush()
            time.sleep(delay)
            i += 1
        sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
        sys.stdout.flush()
    t = threading.Thread(target=spin, daemon=True)
    t.start()
    if duration is not None:
        time.sleep(duration)
        stop()
        t.join(timeout=0.5)
        return None
    else:
        return stop


def spinner_context(text="Loading", delay=0.1):
    _lazy_setup()
    stop_flag = False
    def spin():
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        i = 0
        while not stop_flag:
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{frame} {text}...")
            sys.stdout.flush()
            time.sleep(delay)
            i += 1
        sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
        sys.stdout.flush()
    t = threading.Thread(target=spin, daemon=True)
    t.start()
    try:
        yield
    finally:
        stop_flag = True
        t.join(timeout=0.5)


def list_item(text, symbol="•", color=None, indent=0):
    if _quiet:
        prefix = " " * indent + symbol + " "
        print(f"{prefix}{text}")
        return
    _lazy_setup()
    prefix = " " * indent + symbol + " "
    if color and color in COLOR_MAP:
        ansi = COLOR_MAP[color]
        print(f"{ansi}{prefix}{END}{text}")
    else:
        print(f"{prefix}{text}")


def OK(text=None, sep=' ', end='\n'):
    if text is None:
        color_print_green("✓", end=end)
    else:
        color_print_green(f"✓ {text}", sep=sep, end=end)


def FAIL(text=None, sep=' ', end='\n'):
    if text is None:
        color_print_red("✗", end=end)
    else:
        color_print_red(f"✗ {text}", sep=sep, end=end)



def hash_text(text, algo="md5"):
    _lazy_setup()
    text = str(text)
    algos = {
        "md5": hashlib.md5, "sha1": hashlib.sha1,
        "sha256": hashlib.sha256, "sha512": hashlib.sha512,
    }
    if algo.lower() not in algos:
        if not _quiet:
            error(f"不支持的算法: {algo}")
        return None
    result = algos[algo.lower()](text.encode()).hexdigest()
    if not _quiet:
        info(f"{algo.upper()} 哈希")
        color_print_cyan(result)
    return result


def hash_file(filepath, algo="md5"):
    _lazy_setup()
    p = Path(filepath)
    if not p.exists():
        if not _quiet:
            error(f"文件不存在: {filepath}")
        return None
    algos = {
        "md5": hashlib.md5, "sha1": hashlib.sha1,
        "sha256": hashlib.sha256, "sha512": hashlib.sha512,
    }
    if algo.lower() not in algos:
        if not _quiet:
            error(f"不支持的算法: {algo}")
        return None
    hasher = algos[algo.lower()]()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    result = hasher.hexdigest()
    if not _quiet:
        info(f"文件: {filepath}")
        info(f"{algo.upper()} 哈希")
        color_print_cyan(result)
    return result



class Logger:
    def __init__(self, name="app", log_file=None):
        self.name = name
        self.log_file = log_file
    
    def _log(self, level, color_func, *texts, sep=' '):
        if _quiet:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{timestamp}] [{level}] {sep.join(str(t) for t in texts)}"
        if _enabled and _is_tty():
            color_func(msg)
        else:
            print(msg)
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(msg + '\n')
    
    def info(self, *texts, sep=' '):
        self._log("INFO", lambda x: print(f"{BLUE}{x}{END}"), *texts, sep=sep)
    def success(self, *texts, sep=' '):
        self._log("SUCCESS", lambda x: print(f"{GREEN}{x}{END}"), *texts, sep=sep)
    def error(self, *texts, sep=' '):
        self._log("ERROR", lambda x: print(f"{RED}{x}{END}"), *texts, sep=sep)
    def warn(self, *texts, sep=' '):
        self._log("WARN", lambda x: print(f"{YELLOW}{x}{END}"), *texts, sep=sep)



def read_file(filepath, lines=None, encoding='utf-8'):
    _lazy_setup()
    p = Path(filepath)
    if not p.exists():
        if not _quiet:
            error(f"文件不存在: {filepath}")
        return None
    if not p.is_file():
        if not _quiet:
            error(f"不是文件: {filepath}")
        return None
    size = p.stat().st_size
    if not _quiet:
        info(f"文件: {filepath}")
        info(f"大小: {size} 字节")
    with open(p, 'r', encoding=encoding) as f:
        content = f.readlines()
    total_lines = len(content)
    if not _quiet:
        info(f"行数: {total_lines}")
    if lines:
        content = content[:lines]
        if not _quiet:
            info(f"显示前 {lines} 行")
    if not _quiet:
        separator(char='-', color="cyan")
        color_print_cyan("内容")
    for i, line in enumerate(content, 1):
        print(f"{i:4d} | {line.rstrip()}")
    if not _quiet:
        separator(char='-', color="cyan")
    return ''.join(content)


def write_file(filepath, content, encoding='utf-8', append=False):
    _lazy_setup()
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if append else 'w'
    try:
        with open(p, mode, encoding=encoding) as f:
            f.write(str(content))
        if not _quiet:
            if append:
                success(f"已追加到: {filepath}")
            else:
                success(f"已写入: {filepath}")
        return True
    except Exception as e:
        if not _quiet:
            error(f"写入失败: {e}")
        return False


def create_file(filepath, content="", encoding='utf-8'):
    return write_file(filepath, content, encoding, append=False)


def append_file(filepath, content, encoding='utf-8'):
    return write_file(filepath, content, encoding, append=True)


def edit_file(filepath, encoding='utf-8'):
    _lazy_setup()
    p = Path(filepath)
    if p.exists():
        if not _quiet:
            info(f"编辑现有文件: {filepath}")
            separator(char='-')
            read_file(filepath)
            separator(char='-')
        else:
            with open(p, 'r', encoding=encoding) as f:
                content = f.read()
            print(content)
    else:
        if not _quiet:
            info(f"创建新文件: {filepath}")
    lines = []
    if not _quiet:
        info("输入内容（.save 保存, .quit 退出, .show 显示）:")
    while True:
        try:
            line = input("> ")
            if line == ".save":
                content = '\n'.join(lines)
                write_file(filepath, content, encoding)
                if not _quiet:
                    success("已保存")
                break
            elif line == ".quit":
                if not _quiet:
                    info("已退出，未保存")
                break
            elif line == ".show":
                if lines:
                    if not _quiet:
                        separator(char='-')
                    for i, l in enumerate(lines, 1):
                        print(f"{i:4d} | {l}")
                    if not _quiet:
                        separator(char='-')
                else:
                    if not _quiet:
                        info("暂无内容")
            else:
                lines.append(line)
                if not _quiet:
                    info(f"已添加: {line[:50]}")
        except KeyboardInterrupt:
            if not _quiet:
                info("\n已退出，未保存")
            break



def b64_encode(data, encoding='utf-8'):
    _lazy_setup()
    try:
        if isinstance(data, str):
            data = data.encode(encoding)
        encoded = base64.b64encode(data).decode('ascii')
        if not _quiet:
            info("Base64 编码")
            color_print_cyan(encoded[:200] + "..." if len(encoded) > 200 else encoded)
        return encoded
    except Exception as e:
        if not _quiet:
            error(f"编码失败: {e}")
        return None


def b64_decode(b64_str, as_text=True, encoding='utf-8'):
    _lazy_setup()
    try:
        raw = base64.b64decode(b64_str)
        if as_text:
            result = raw.decode(encoding)
            if not _quiet:
                info("Base64 解码 > 文本")
                color_print_cyan(result[:200] + "..." if len(result) > 200 else result)
            return result
        else:
            if not _quiet:
                info("Base64 解码 > 字节")
            return raw
    except Exception as e:
        if not _quiet:
            error(f"解码失败: {e}")
        return None


def b64_encode_file(filepath):
    _lazy_setup()
    p = Path(filepath)
    if not p.exists():
        if not _quiet:
            error(f"文件不存在: {filepath}")
        return None
    try:
        data = p.read_bytes()
        encoded = base64.b64encode(data).decode('ascii')
        if not _quiet:
            info(f"文件已编码: {filepath} ({len(data)} 字节)")
            color_print_cyan(encoded[:200] + "..." if len(encoded) > 200 else encoded)
        return encoded
    except Exception as e:
        if not _quiet:
            error(f"编码失败: {e}")
        return None


def b64_decode_to_file(b64_str, output_path):
    _lazy_setup()
    try:
        data = base64.b64decode(b64_str)
        Path(output_path).write_bytes(data)
        if not _quiet:
            success(f"已还原: {output_path}")
        return True
    except Exception as e:
        if not _quiet:
            error(f"还原失败: {e}")
        return False


__all__ = [
    "info", "success", "error", "warn",
    "color_print_red", "color_print_green", "color_print_yellow",
    "color_print_blue", "color_print_purple", "color_print_cyan",
    "color_print_white", "color_print_black",
    "slow_print", "typewriter", "color_typewriter",
    "typewriter_red", "typewriter_green", "typewriter_yellow",
    "typewriter_blue", "typewriter_purple", "typewriter_cyan",
    "typewriter_white", "typewriter_black",
    "random_typewriter",
    "rgb_to_ansi", "custom_print", "custom_typewriter",
    "gradient_text", "rainbow_text",
    "binary_output", "binary_text", "text_to_binary",
    "binary_exec", "binary_from_file", "binary_to_file", "binary_exec_file",
    "title_box", "separator", "table", "tree",
    "Live", "live", "highlight",
    "progress_bar", "spinner", "spinner_context", "list_item", "OK", "FAIL",
    "enable", "disable", "force_color",
    "hash_text", "hash_file",
    "Logger",
    "read_file", "write_file", "create_file", "append_file", "edit_file",
    "b64_encode", "b64_decode", "b64_encode_file", "b64_decode_to_file",
    "set_quiet", "set_verbose", "is_quiet",
    "COLOR_MAP", "END",
    "RED", "GREEN", "YELLOW", "BLUE", "PURPLE", "CYAN", "WHITE", "BLACK", "END"
]