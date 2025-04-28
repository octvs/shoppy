# Make CLI runnable from source tree with `python src/package`
if not __package__:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import logging
import os

from shoppy import ShoppingList

# TODO: Sort all json keys everytime the file is written or read
# TODO: Remove the TODO from README, maybe add it to trackdown
# TODO: Write a story about bring and why we choose to have categories
# TODO: Add commands to manipulate existing categories `shoppy add
# --categories` add an item to a category `shoppy add --categories --new` adds
# a new a category. Althought the last one might be a bit tricky since we might
# need to add it to store order, or maybe not


def _list(_shop_list, cat):
    if not cat:
        print(_shop_list)
    else:
        os.system(f"cat {_shop_list.cat_fpath} | jq")


def _edit(_shop_list, cat):
    _file = _shop_list.fpath
    if cat:
        _file = _shop_list.cat_fpath
    os.system(f"$EDITOR {_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="verbose output"
    )
    parser.add_argument(
        "-c",
        "--categories",
        action="store_true",
        help="work with categories file",
    )

    shopping = ShoppingList()

    cmds = parser.add_subparsers(title="commands", dest="f")
    cmds.add_parser(
        "add", aliases=["a"], help="add new item to the list"
    ).set_defaults(f=lambda _: shopping.add_item())
    cmds.add_parser(
        "check", aliases=["c"], help="check an item from the list"
    ).set_defaults(f=lambda _: shopping.check_item())
    cmds.add_parser(
        "list", aliases=["l"], help="display the shopping list"
    ).set_defaults(f=lambda cat: _list(shopping, cat))
    cmds.add_parser(
        "edit", aliases=["e"], help="open the list on $EDITOR"
    ).set_defaults(f=lambda cat: _edit(shopping, cat))

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)
    logging.debug(f"Received args from shell {args}")
    if args.f is None:
        args.f = lambda cat: _list(shopping, cat)

    args.f(args.categories)


if __name__ == "__main__":
    main()
