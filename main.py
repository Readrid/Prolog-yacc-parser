from typing import List
import sys

from parser import Parser

def main(args_str: List[str]):
    p = Parser(args_str[0])
    p.parse()


if __name__ == '__main__':
    main(sys.argv[1:])