"""shoppy, a simple script as a minimalist replacement for shopping list apps"""
from helpers import create_shoplist, read_user_input

if __name__ == "__main__":
    shopping_list = read_user_input()
    create_shoplist(shopping_list)
