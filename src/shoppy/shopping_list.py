import json
import logging
import os
from pathlib import Path

from pyfzf.pyfzf import FzfPrompt
from termcolor import colored


def reverse_dict(dct):
    """Reverse a dict"""
    return {i: k for k in dct for i in dct[k]}


class ShoppingList:
    DEFAULT_DIR = Path.home().joinpath("notes/.shoppy")

    def __init__(self):
        self.read_config()
        self.read_user_input()
        self.read_categories()

    def read_config(self):
        self.data_path = Path(
            os.environ.get("SHOPPY_DIR", str(self.DEFAULT_DIR))
        )
        if not self.data_path.is_dir():
            exit(f"Dir for shoppy doesn't exists!\nProvided: {self.data_path}")
        self.fpath = self.data_path.joinpath("shoppy_order.txt")
        self.cat_fpath = self.data_path.joinpath("categories.json")

    def read_user_input(self):
        """Read user input while filtering empty lines"""
        with open(self.fpath, "r", encoding="utf-8") as f:
            self.shop_list = list(filter(None, f.read().splitlines()))
        logging.debug(f"User input read: {self.shop_list}")

    def read_categories(self):
        """Reads categories file, returns item map"""
        with open(self.cat_fpath, "r", encoding="utf-8") as f:
            return json.load(f)

    def read_store_file(self):
        """Get store order"""
        file = self.data_path.joinpath("store-layout.txt")
        with open(file, "r", encoding="utf-8") as file:
            return file.read().splitlines()

    def parse_input(self):
        """
        Reads user input from a txt file
        Returns a dictionary separated into categories ignoring blank lines
        """
        item_map = reverse_dict(self.read_categories())

        shop_dict = {}
        for itm in self.shop_list:
            ctg = item_map.get(itm.split(",")[0].strip(), "Undefined")
            if not shop_dict.get(ctg):
                shop_dict[ctg] = []
            shop_dict[ctg].append(itm)
        return shop_dict

    def log_undefined_items(self, dct):
        """Write undefined items to a list to be checked later"""
        if not dct.get("Undefined"):
            return

        file = self.data_path.joinpath("undefined-items.txt")

        already_known = []
        if file.exists():
            with open(file, "r", encoding="utf-8") as f:
                already_known = f.read().splitlines()
        logging.debug(f"Undefined items already has items {already_known}")

        new_und = []
        for itm in dct.get("Undefined"):  # pyright: ignore
            item_name = itm.split(",")[0]
            if item_name not in already_known:
                logging.debug(f"{item_name} is a new undefined entry.")
                new_und.append(item_name)

        if new_und:
            with open(file, "w", encoding="utf-8") as file:
                logging.debug(
                    f"Added {len(new_und)} new items to undefined items file."
                )
                new_und = list(filter(None, already_known + new_und))
                file.write("\n".join(new_und) + "\n")

    def prompt(self, inp, args=""):
        fzf_return = FzfPrompt().prompt(inp, args)
        if fzf_return:
            return fzf_return[0]
        else:
            exit("Fzf returned nothing!")

    def check_item(self):
        fzf_return = self.prompt(self.shop_list)
        self.shop_list = [i for i in self.shop_list if not i == fzf_return]
        logging.debug(f"Removed item from shopping list: {fzf_return}")
        self.write()

    def add_item(self):
        fzf_return = self.prompt(
            reverse_dict(self.read_categories()).keys(),
            args="--bind=enter:replace-query+print-query",
        )
        self.shop_list.append(fzf_return)
        logging.debug(f"Added new item to shopping list: {fzf_return}")
        self.write()

    def write(self):
        logging.debug(f"Wrote list to {self.fpath}")
        with open(self.fpath, "w", encoding="utf-8") as file:
            file.write("\n".join(self.shop_list) + "\n")

    def __str__(self):
        """Prints the dict in shopping list format"""

        shop_dict = self.parse_input()

        if len(shop_dict) == 0:
            exit(colored("Shopping list is empty!", "light_cyan"))

        self.log_undefined_items(shop_dict)
        store_ctgs = self.read_store_file()

        # Append non-existing categories from order to the store configuration
        undefined_exists = False
        for ctg in sorted(shop_dict.keys()):
            if ctg == "Undefined":
                # Should be appended last, hold on for now
                undefined_exists = True
                continue
            if ctg not in store_ctgs:
                store_ctgs.append(ctg)

        if undefined_exists:
            store_ctgs.append("Undefined")

        # Print to terminal
        md_string = colored("# Shopping List\n\n", "cyan")
        for ctg in store_ctgs:
            itm_list = shop_dict.get(ctg)
            if not itm_list:  # Don't print empty categories
                continue
            md_string += colored(f"## {ctg}\n\n", "light_cyan")
            for itm in sorted(itm_list):
                inp = itm.split(",")  # Split to check details
                md_string += colored(f"- {inp[0]}", "yellow")
                if len(inp) > 1:  # In case there are details
                    md_string += colored(f", {inp[1].strip()}", "white")
                md_string += "\n"
            md_string += "\n"
        return md_string[:-1]
