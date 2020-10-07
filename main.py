from typing import List

from parser import Parser

def main(args_str: List[str]):
    p = Parser()
    p.parse(args_str[0])


if __name__ == '__main__':
    main(sys.argv[1:])