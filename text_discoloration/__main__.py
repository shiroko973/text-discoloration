#!/usr/bin/env python3

import argparse
import re
from text_discoloration import *


def parse_rgb(s):
    match = re.match(r'rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)', s)
    if match:
        return tuple(map(int, match.groups()))
    return None


def main():
    parser = argparse.ArgumentParser(
        description="text_discoloration - 终端彩色输出工具",
        prog="tcd"
    )
    parser.add_argument("text", nargs="?", help="要输出的文本")
    parser.add_argument("-c", "--color", help="颜色: red/green/yellow/blue/purple/cyan/white/black 或 rgb(R,G,B)")
    parser.add_argument("-t", "--typewriter", action="store_true", help="打字机效果")
    parser.add_argument("-r", "--rainbow", action="store_true", help="彩虹色")
    parser.add_argument("-g", "--gradient", nargs=2, metavar=('START', 'END'),
                        help="渐变色，格式: rgb(255,0,0) rgb(0,255,0)")
    parser.add_argument("-d", "--delay", type=float, default=0.05, help="打字机延迟（秒）")
    parser.add_argument("--version", action="store_true", help="显示版本号")

    args = parser.parse_args()

    if args.version:
        print(f"text_discoloration {__version__}")
        return

    if not args.text:
        parser.print_help()
        return

    if args.rainbow:
        rainbow_text(args.text, delay=args.delay)
        return

    if args.gradient:
        start = parse_rgb(args.gradient[0])
        end = parse_rgb(args.gradient[1])
        if start and end:
            gradient_text(args.text, start, end, delay=args.delay)
        else:
            print("渐变色格式错误，请使用: rgb(255,0,0) rgb(0,255,0)")
        return

    if args.typewriter:
        if args.color:
            rgb = parse_rgb(args.color)
            if rgb:
                color_typewriter(args.text, delay=args.delay, r=rgb[0], g=rgb[1], b=rgb[2])
                return
            else:
                color_typewriter(args.color, args.text, delay=args.delay)
        else:
            typewriter(args.text, delay=args.delay)
        return

    if args.color:
        rgb = parse_rgb(args.color)
        if rgb:
            custom_print(args.text, r=rgb[0], g=rgb[1], b=rgb[2])
        else:
            color_map = {
                "red": color_print_red,
                "green": color_print_green,
                "yellow": color_print_yellow,
                "blue": color_print_blue,
                "purple": color_print_purple,
                "cyan": color_print_cyan,
                "white": color_print_white,
                "black": color_print_black,
            }
            if args.color.lower() in color_map:
                color_map[args.color.lower()](args.text)
            else:
                print(f"未知颜色: {args.color}")
    else:
        print(args.text)


if __name__ == "__main__":
    main()