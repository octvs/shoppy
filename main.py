from pathlib import Path
import json

from helpers import print_catalog

catalog_file = Path("categories.json")
with open(catalog_file, "r") as f:
    catalog = json.load(f)

print_catalog(catalog)
for k in catalog:
    print(f"{k=}")
    for i in catalog[k]:
        print(f"{i=}")

reverse_cat = {i: k for k in catalog for i in catalog[k]}
print_catalog(reverse_cat)
print(reverse_cat)

with open("test-input.txt", "r") as f:
    user_inp = f.read().splitlines()

# print(user_inp)


# parse input
# for itm in user_inp:
#    ctg = categories.get()
