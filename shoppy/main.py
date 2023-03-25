import json
import logging
from pathlib import Path

config_file = Path.home().joinpath(".config/shoppy/config.json")
if config_file.exists():
    with open(config_file, "r", encoding="utf-8") as file:
        data_dir = json.load(file)["data_dir"]
else:
    exit("Please define a data directory on the configuration file.")

data_path = Path.home().joinpath(data_dir)
order_file = data_path.joinpath("shoppy_order.txt")
store_file = data_path.joinpath("store-layout.txt")
list_file = data_path.joinpath("shoppy_list.md")
undefineds_file = data_path.joinpath("undefined-items.txt")


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
    with open(data_path.joinpath("categories.json"), "r", encoding="utf-8") as file:
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

    logging.debug(f"User input read: {user_inp}")
    shop_list = {}
    for itm in user_inp:
        ctg = item_map.get(itm.split(",")[0].strip(), "Undefined")
        if not shop_list.get(ctg):
            shop_list[ctg] = []
        shop_list[ctg].append(itm)

    return shop_list


def create_shoplist(res):
    """
    Prints the dict in shopping list format
    """
    # Get store order
    with open(store_file, "r", encoding="utf-8") as file:
        store_ctgs = file.read().splitlines()

    # Append non-existing categories to it
    for ctg in sorted(res.keys()):
        if ctg not in store_ctgs:
            store_ctgs.append(ctg)

    # Print to markdown format
    md_string = "# Shopping List\n\n"
    for ctg in store_ctgs:
        itm_list = res.get(ctg)
        if not itm_list:  # Don't print empty categories
            continue
        md_string += f"## {ctg}\n\n"
        for itm in sorted(itm_list):
            inp = itm.split(",")  # Split to check details
            md_string += f"- [ ] {inp[0]}\n"
            if len(inp) > 1:  # In case there are details
                md_string = md_string[:-1] + f" _{inp[1].strip()}_\n"
        md_string += "\n"

    print("Shopping list updated.")
    with open(list_file, "w", encoding="utf-8") as file:
        file.write(md_string)

    # Write undefined items to a list to be checked later
    if res.get("Undefined"):
        log_undefined_items(res)


def log_undefined_items(und):
    already_known = []
    if undefineds_file.exists():
        with open(undefineds_file, "r", encoding="utf-8") as file:
            already_known = file.read().splitlines()

    new_und = []
    for itm in und:
        if itm not in already_known:
            new_und.append(itm)

    with open(undefineds_file, "a", encoding="utf-8") as file:
        logging.debug(f"Added {len(new_und)} new items to undefineds file.")
        file.write("\n".join(new_und) + "\n")


def post_shop_update():
    """Cleans input file of shopped items, post shopping"""

    if not list_file.exists():
        exit("There is no shopping list to post process.")

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
