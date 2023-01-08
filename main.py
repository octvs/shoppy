import json

from helpers import print_to_md, reverse_dict

if __name__ == "__main__":
    with open("categories.json", "r", encoding="utf-8") as f:
        item_map = reverse_dict(json.load(f))

    with open("input.txt", "r", encoding="utf-8") as f:
        user_inp = f.read().splitlines()

    print(f"User input read: {user_inp}")
    shopping_list = {}
    for itm in user_inp:
        ctg = item_map.get(itm, "Undefined")
        if not shopping_list.get(ctg):
            shopping_list[ctg] = []
        shopping_list[ctg].append(itm)

    print_to_md(shopping_list)
