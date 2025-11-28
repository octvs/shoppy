shoppy, a simple script as a minimalist replacement for shopping list apps

input format: a single item per line txt file, details can be added trailing
with a comma

ordering: edit the store-order.txt file with category names. might sound like a
weird feature but try to shop from a huge supermarket, it comes in handy.

config: place a config.py file at $HOME/.config/shoppy/

Config file arguments data_dir: str, path to where categories and the
input/output lists will be stored.

# TODO

- Recurrent mode
  - Add --single mode to only execute a single time otherwise behave as the
    dmenu-bluetooth which re-prompts all the time until user escapes with `ESC`
  - `parser.add_argument( "-s", "--single", action="store_true", help="do not run in recurrent mode")`
- Adding details
  - It should be a separate subcmd, with the following flow
    - Provide picker for all items on the list
    - Prompt user for providing details to add
    - Write list with the modification
- Handling duplicate entries
  - Check whether they are handled properly
  - A case: When there were two entries (in this instance they both had no
    detail) and asked to remove the entry from the list, shoppy removed both,
    which can be undesirable
- Missing files
  - Currently we don't cover the case where files are missing well
  - We can add the following block to covers missing order file but others need
    more treatment
  ````py
  if not self.fpath.exists():
      logging.warning("No order file is found, creating...")
      self.fpath.touch()
  ```
  ````
- Incorrect matches
  - When adding "Terea" it matches "Tuerkischer Kaffee"
