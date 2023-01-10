"""Some helper funcs for shoppy"""

import json
from pathlib import Path


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


def read_config():
    """Reads user config.json for data_dir"""
    config_dir = Path.home().joinpath(".config/shoppy/")
    with open(config_dir.joinpath("config.json"), "r", encoding="utf-8") as file:
        config = json.load(file)
    with open(config_dir.joinpath("categories.json"), "r", encoding="utf-8") as file:
        item_map = reverse_dict(json.load(file))

    return Path(config["data_dir"]), item_map


def read_user_input():
    """
    Reads user input from a txt file
    Returns a dictionary separated into categories ignoring blank lines
    """
    data_dir, item_map = read_config()

    # Read user input while filtering empty lines
    with open(data_dir.joinpath("shoppy_order.txt"), "r", encoding="utf-8") as file:
        user_inp = list(filter(None, file.read().splitlines()))

    print(f"User input read: {user_inp}")
    shopping_list = {}
    for itm in user_inp:
        ctg = item_map.get(itm.split(",")[0], "Undefined")
        if not shopping_list.get(ctg):
            shopping_list[ctg] = []
        shopping_list[ctg].append(itm)

    return shopping_list


def create_shoplist(res):
    """
    Prints the dict in shopping list format
    """
    data_dir, _ = read_config()
    # Get store order
    with open(data_dir.joinpath("shoppy_order.txt"), "r", encoding="utf-8") as file:
        store_order = file.read().splitlines()

    # Append non-existing categories to it
    for ctg in sorted(res.keys()):
        if ctg not in store_order:
            store_order.append(ctg)

    # Print to markdown format
    md_string = "# Shopping List \n\n"
    for ctg in store_order:
        itm_list = res.get(ctg)
        if not itm_list:  # Don't print empty categories
            continue
        md_string += f"## {ctg} \n\n"
        for itm in sorted(itm_list):
            inp = itm.split(",")  # split to check details
            line = f"{inp[0]}\n"
            # line = f"- [ ] {inp[0]}\n"
            if len(inp) > 1:  # in case there are details
                line = line[:-1] + f" _{inp[1]}_\n"
            md_string += line
        md_string += "\n"

    print("Shopping list updated.")
    with open(data_dir.joinpath("shoppy_list.md"), "w", encoding="utf-8") as file:
        file.write(md_string)


def post_shop_update():
    """Cleans input file of shopped items, post shopping"""
    data_dir, _ = read_config()
    with open(data_dir.joinpath("shoppy_list.md"), "r", encoding="utf-8") as file:
        old_list = list(filter(None, file.read().splitlines()))
    old_list = [a for a in old_list if a[0] != "#"]
    res = ""
    for item in old_list:
        if "_" in item:
            prod, detail = item.split()
            res += f"{prod},{detail[1:-1]}\n"
        else:
            res += f"{item}\n"

    print("Post-shopping update is done.")
    with open(data_dir.joinpath("shoppy_order.txt"), "w", encoding="utf-8") as file:
        file.write(res[:-1])
