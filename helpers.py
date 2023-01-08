"""Some helper funcs for shoppy"""


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
        md_string += f"## {ctg} \n"
        for itm in sorted(itm_list):
            md_string += f"  - [ ] {itm}\n"
        md_string += "\n"
    with open("shopping_list.md", "w", encoding="utf-8") as file:
        file.write(md_string)
