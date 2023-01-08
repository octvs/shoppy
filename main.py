from os import wait
from pathlib import Path
import json

from helpers import *

UNDEFINED_CAT = "ZZ-Undefined"

catalog_file = Path("categories.json")
with open(catalog_file, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print("Catalog loaded...")
print_dict(catalog)
reverse_cat = reverse_dict(catalog)
print(reverse_cat)

with open("test-input.txt", "r", encoding="utf-8") as f:
    user_inp = f.read().splitlines()

print(f"User input read: {user_inp}")
shopping_list = {}
for itm in user_inp:
    ctg = reverse_cat.get(itm)
    if not ctg:
        print(f"{itm}>Undefined")
        ctg = UNDEFINED_CAT
    if not shopping_list.get(ctg):
        shopping_list[ctg] = []
    shopping_list[ctg].append(itm)


print_to_md(shopping_list)
