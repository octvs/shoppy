"""Some helper funcs for shoppy"""

import json


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


def read_user_input():
    """
    Reads user input from a txt file returns a dictionary separated into categories ignoring blank lines
    """
    with open("categories.json", "r", encoding="utf-8") as file:
        item_map = reverse_dict(json.load(file))

    # Read user input while filtering empty lines
    with open("input.txt", "r", encoding="utf-8") as file:
        user_inp = list(filter(None, file.read().splitlines()))

    print(f"User input read: {user_inp}")
    shopping_list = {}
    for itm in user_inp:
        ctg = item_map.get(itm.split(",")[0], "Undefined")
        if not shopping_list.get(ctg):
            shopping_list[ctg] = []
        shopping_list[ctg].append(itm)

    return shopping_list


def print_to_md(res):
    """
    Prints the dict in shopping list format
    This format is simply headers for categories and checklist for each items
    """
    # Get store order
    with open("store-order.txt", "r", encoding="utf-8") as file:
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
            line = f"- [ ] {inp[0]}\n"
            if len(inp) > 1:  # in case there are details
                line = line[:-1] + f" *{inp[1]}*\n"
            md_string += line
        md_string += "\n"

    print("Shopping list updated.")
    with open("shopping_list.md", "w", encoding="utf-8") as file:
        file.write(md_string)
