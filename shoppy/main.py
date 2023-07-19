import json
import logging
from pathlib import Path
from pyfzf.pyfzf import FzfPrompt
from termcolor import colored


def reverse_dict(dct):
    """Reverse a dict"""
    return {i: k for k in dct for i in dct[k]}


class ShoppingList:
    config_dir = Path.home().joinpath(".config/shoppy")

    def __init__(self):
        self.read_config()
        self.read_user_input()

    def read_config(self):
        config_file = self.config_dir.joinpath("config.json")
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as file:
                self.data_dir = json.load(file)["data_dir"]
        else:
            exit("Please define a data directory on the configuration file.")

        self.data_path = Path.home().joinpath(self.data_dir)
        self.fpath = self.data_path.joinpath("shoppy_order.txt")

    def read_user_input(self):
        """Read user input while filtering empty lines"""
        with open(self.fpath, "r", encoding="utf-8") as f:
            self.shop_list = list(filter(None, f.read().splitlines()))
        logging.debug(f"User input read: {self.shop_list}")

    def read_categories(self):
        """Reads categories file"""
        file = self.data_path.joinpath("categories.json")
        with open(file, "r", encoding="utf-8") as f:
            item_map = reverse_dict(json.load(f))
        return item_map

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
        item_map = self.read_categories()

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
            if itm not in already_known:
                logging.debug(f"{itm} is a new undefined entry.")
                new_und.append(itm)

        new_und = list(filter(None, already_known + new_und))

        with open(file, "w", encoding="utf-8") as file:
            logging.debug(f"Added {len(new_und)} new items to undefined items file.")
            file.write("\n".join(new_und) + "\n")

    def check_item(self):
        fzf_return = FzfPrompt().prompt(self.shop_list)[0]
        self.shop_list = [i for i in self.shop_list if not i == fzf_return]
        logging.debug(f"Removed item from shopping list: {fzf_return}")
        self.write()

    def add_item(self):
        inp = input(f"Add item:\n")
        self.shop_list.append(inp)
        logging.debug(f"Added new item to shopping list: {inp}")
        self.write()

    def write(self):
        logging.debug(f"Wrote list to {self.fpath}")
        with open(self.fpath, "w", encoding="utf-8") as file:
            file.write("\n".join(self.shop_list))

    def __str__(self):
        """Prints the dict in shopping list format"""

        shop_dict = self.parse_input()
        self.log_undefined_items(shop_dict)
        store_ctgs = self.read_store_file()

        # Append non-existing categories to it
        for ctg in sorted(shop_dict.keys()):
            if ctg not in store_ctgs:
                store_ctgs.append(ctg)

        # TODO: Since we are iterating over categories this is a temporary
        # solution, better way would be to iterate over items instead of the
        # emtpy categories
        if len(shop_dict) ==0 :
            exit(colored("Shopping list empty!", "light_cyan"))

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
