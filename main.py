"""shoppy, a simple script as a minimalist replacement for shopping list apps"""
from helpers import print_to_md, read_user_input

if __name__ == "__main__":
    shopping_list = read_user_input()
    print_to_md(shopping_list)
