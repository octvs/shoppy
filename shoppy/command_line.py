import sys
from . import read_user_input, create_shoplist, post_shop_update


def main():
    if len(sys.argv) == 1:
        shopping_list = read_user_input()
        create_shoplist(shopping_list)
    else:
        match sys.argv[1]:
            case ["p", "post"]:
                post_shop_update()
            case _:
                exit("Unexpected argument!")
