import argparse
import logging
import os

from main import ShoppingList


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="verbose output"
    )

    shopping = ShoppingList()

    cmds = parser.add_subparsers(title="commands", dest="f")
    cmds.add_parser(
        "add", aliases=["a"], help="add new item to the list"
    ).set_defaults(f=shopping.add_item)
    cmds.add_parser(
        "check", aliases=["c"], help="check an item from the list"
    ).set_defaults(f=shopping.check_item)
    cmds.add_parser(
        "list", aliases=["l"], help="display the shopping list"
    ).set_defaults(f=lambda: print(shopping))
    cmds.add_parser(
        "edit", aliases=["e"], help="open the list on $EDITOR"
    ).set_defaults(f=lambda: os.system(f"$EDITOR {shopping.fpath}"))

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)
    logging.debug(f"Received args from shell {args}")
    if args.f is None:
        args.f = lambda: print(shopping)

    args.f()


if __name__ == "__main__":
    main()
