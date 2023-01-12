"""shoppy, a simple script as a minimalist replacement for shopping list apps"""

import sys
import json
from pathlib import Path

# The following was on a config.py before but it was unnecessary
data_dir = Path.home().joinpath("git/notes/shoppy/")
order_file = data_dir.joinpath("shoppy_order.txt")
list_file = data_dir.joinpath("shoppy_list.md")


def print_dict(dct):
    """
    Pretty prints the dicts that have lists as values
    """
    for k in dct:
        print(f"Key:{k}")
        assert isinstance(dct[k], list)
        for i in dct[k]:
            print(f"\tValue:{i}")


def reverse_dict(dct):
    """Reverse a dict"""
    return {i: k for k in dct for i in dct[k]}


def read_categories():
    """Reads categories file"""
    with open(data_dir.joinpath("categories.json"), "r", encoding="utf-8") as file:
        item_map = reverse_dict(json.load(file))
    return item_map


def read_user_input():
    """
    Reads user input from a txt file
    Returns a dictionary separated into categories ignoring blank lines
    """
    item_map = read_categories()

    # Read user input while filtering empty lines
    with open(order_file, "r", encoding="utf-8") as file:
        user_inp = list(filter(None, file.read().splitlines()))

    print(f"User input read: {user_inp}")
    shop_list = {}
    for itm in user_inp:
        ctg = item_map.get(itm.split(",")[0], "Undefined")
        if not shop_list.get(ctg):
            shop_list[ctg] = []
        shop_list[ctg].append(itm)

    return shop_list


def create_shoplist(res):
    """
    Prints the dict in shopping list format
    """
    # Get store order
    with open(order_file, "r", encoding="utf-8") as file:
        store_order = file.read().splitlines()

    # Append non-existing categories to it
    for ctg in sorted(res.keys()):
        if ctg not in store_order:
            store_order.append(ctg)

    # Print to markdown format
    md_string = "# Shopping List\n\n"
    for ctg in store_order:
        itm_list = res.get(ctg)
        if not itm_list:  # Don't print empty categories
            continue
        md_string += f"## {ctg}\n\n"
        for itm in sorted(itm_list):
            inp = itm.split(",")  # split to check details
            md_string += f"- [ ] {inp[0]}\n"
            if len(inp) > 1:  # in case there are details
                md_string = md_string[:-1] + f" _{inp[1]}_\n"
        md_string += "\n"

    print("Shopping list updated.")
    with open(list_file, "w", encoding="utf-8") as file:
        file.write(md_string)


def post_shop_update():
    """Cleans input file of shopped items, post shopping"""
    with open(list_file, "r", encoding="utf-8") as file:
        old_list = list(filter(lambda x: x[:5] == "- [ ]", file.read().splitlines()))

    txt_string = ""
    for item in old_list:
        itm = item[6:].split("_")
        txt_string += f"{itm[0]}\n"
        if len(itm) > 1:
            txt_string = txt_string[:-2] + f",{itm[1]}\n"

    print("Post-shopping update is done.")
    with open(order_file, "w", encoding="utf-8") as file:
        file.write(txt_string[:-1])

    list_file.unlink()


if __name__ == "__main__":
    if sys.argv[1] != "post":
        shopping_list = read_user_input()
        create_shoplist(shopping_list)
    else:
        post_shop_update()
