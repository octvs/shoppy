from os import wait
from pathlib import Path
import json

from helpers import *

UNDEFINED_CAT = "ZZ-Undefined"

catalog_file = Path("categories.json")
with open(catalog_file, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print("Catalog loaded...")
print_catalog(catalog)
reverse_cat = reverse_catalog(catalog)
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


def print_to_md(res):
    # implement custom sorting
    print(sorted(res.keys()))
    md_string = "# Shopping List \n\n"
    for ctg in sorted(res.keys()):
        md_string += f"## {ctg} \n"
        for itm in sorted(res[ctg]):
            md_string += f"  - [ ] {itm}\n"
        md_string += "\n"
    with open("shopping_list.md", "w", encoding="utf-8") as f:
        f.write(md_string)


print_to_md(shopping_list)
