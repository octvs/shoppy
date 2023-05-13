import sys
import os
import logging
from .main import ShoppingList

short_cmds = {"c": "check", "ls": "list", "e": "edit", "a": "add"}


def parse_args(args: list) -> list:
    if "--debug" in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove("--debug")
    if len(args) == 1:
        args.append("list")
    if long_version := short_cmds.get(args[1]):
        args[1] = long_version
    return args


def main(args=sys.argv):
    args = parse_args(args)
    logging.debug(f"Received args from shell {args}")
    shopping = ShoppingList()

    match args[1]:
        case "add":
            shopping.add_item()
        case "check":
            shopping.check_item()
        case "list":
            print(shopping)
        case "edit":
            os.system(f"$EDITOR {shopping.fpath}")
        case _:
            exit("Unexpected argument!")
