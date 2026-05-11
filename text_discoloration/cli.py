#!/usr/bin/env python3
import sys
from text_discoloration.core import ra_key

def main():
    args = sys.argv[1:]

    if not args:
        print("用法: ra [模式...] -i 长度")
        print("模式: 1=关数字 2=关小写 3=关大写 4=关符号")
        print("示例: ra 1 -i 32")
        return

    length = 20
    no_num = False
    no_lower = False
    no_upper = False
    no_symbol = False

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '-i' and i + 1 < len(args):
            try:
                length = int(args[i + 1])
                i += 2
                continue
            except ValueError:
                pass
        elif arg == '1':
            no_num = True
        elif arg == '2':
            no_lower = True
        elif arg == '3':
            no_upper = True
        elif arg == '4':
            no_symbol = True
        elif arg in ('-h', '--help'):
            print("用法: ra [模式...] -i 长度")
            print("模式: 1=关数字 2=关小写 3=关大写 4=关符号")
            print("示例: ra 1 -i 32")
            return
        i += 1

    if length > 10000:
        print("错误：长度不能超过 10000")
        return

    key = ra_key(length=length, no_num=no_num, no_lower=no_lower, no_upper=no_upper, no_symbol=no_symbol)
    print(key)

if __name__ == "__main__":
    main()