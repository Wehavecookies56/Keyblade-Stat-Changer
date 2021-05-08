# Keyblade-Stat-Changer
## What this is for

This is a Keyblade stat changer script for [Kingdom Keys](https://github.com/Wehavecookies56/Kingdom-Keys), a Minecraft mod, this script will take the values from a CSV file and write them to the JSON files for each keyblade in the CSV allowing quick changes to the stats for the 120+ keyblades in Kingdom Keys. This was created somewhat quickly so it's fairly simple but figured it'd be useful for not only our dev team but anyone wanting to make a datapack.

## Basic Usage
Here's a quick guide on using the tool without the need to edit the config

1. Modify the `example.csv` to how you would like to change the stats to.
2. Rename `example.csv` to `keyblades.csv`
3. Extract the `data\kingdomkeys\keyblades\` folder from the latest Kingdom Keys `.jar` file. So that the `keyblades` folder is in the same folder as `keyblades.csv` and `keybladestatchanger.py`
4. Run `keybladestatchanger.py`
5. Enter `Y` to write the changes to the JSON files.

## CSV format

The CSV file you supply should have the format `name, strength, magic` for example `Kingdom Key, 1, 0`.
See `example.csv` in the repo which contains every keyblade.

## Config

- `csvPath=keyblades.csv` the path of the CSV file containing the stats to change to. Can be a full path like `C:/keyblades.csv`.
- `jsonFolderPath=keyblades/` the path of the folder that contains all the `.json` files from the mod. Can be a full path like `C:/keyblades/`.
- `levelToChange=0` the keyblade upgrade level stats to change, `0` for the base stats and `1-10` for the upgrade level stats.
- `autoLevelStats=True` If set to True the upgrade level stats will be automatically calculated from the stats given from the CSV. Only works if `levelToChange` is `0`.

## Future improvements

- Ability to change other parts of the JSON files
- Alternative way to enter config options when running the script instead of relying on the config file
- Ability to add keyblades to list of valid keyblade names
