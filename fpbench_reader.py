from fpbench_parser import parser
import sys


if __name__ == "__main__":
    if len(sys.argv) == 1:
        user_str = input("Enter an expression:\n")
        print(parser.parse(user_str))
    else:
        for e in sys.argv[1:]:
            print(e)
            with open(e, 'r') as f:
                print(parser.parse(f.read(),tracking=True))
