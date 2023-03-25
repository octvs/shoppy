import sys
import logging
from .main import read_user_input, create_shoplist, post_shop_update


def parse_args(args: list) -> list:
    if "--debug" in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove("--debug")
    return args


def main():
    args = parse_args(sys.argv)

    if len(sys.argv) == 1:
        shopping_list = read_user_input()
        create_shoplist(shopping_list)
    else:
        match sys.argv[1]:
            case "p" | "post":
                post_shop_update()
            case _:
                exit("Unexpected argument!")
