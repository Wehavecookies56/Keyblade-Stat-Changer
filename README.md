# Keyblade-Stat-Changer
## What this is for

This is a Keyblade stat changer script made in Python 3.7 for [Kingdom Keys](https://github.com/Wehavecookies56/Kingdom-Keys), a Minecraft mod, this script will take the values from a CSV file and write them to the JSON files for each keyblade in the CSV allowing quick changes to the stats for the 120+ keyblades in Kingdom Keys. This was created somewhat quickly so it's fairly simple but figured it'd be useful for not only our dev team but anyone wanting to make a datapack.

## Features
- Replace keyblade and organization weapon stats in the json files from Kingdom Keys with values in a CSV file
- Generate a CSV file from the json files
- Generate a log file showing the previous and the new stats, possibly useful for creating something like a changelog
- Automatically calculate the stats for all the levels for the upgrades
- Generate the code for the datagen with the stat changes to be used in the mod
- Downloads `names.json` from the repo automatically

## Basic Usage
Here's a quick guide on using the tool without the need to edit the config

1. Run `keybladestatchanger.py`, you'll need Python 3.x installed
2. Extract the `data\kingdomkeys\keyblades\` folder from the latest Kingdom Keys `.jar` file. So that the `keyblades` folder is in the same folder as `keybladestatchanger.py`
3. Enter `1` to generate a `.csv` file with all keyblades and stats from the `.json` files
3. Modify the values in the generated `.csv` file to your liking
4. Enter `0` to write the values in the `.csv` file to the `.json` files contained in the `keyblades` folder
5. Enter `Y` to write the changes to the `.json` files.

## CSV format

The CSV file you supply should have the format `name, strength, magic` for example `Kingdom Key, 1, 0`.
See `example.csv` in the repo which contains every keyblade.

## Config

- `csvPath=keyblades.csv` the path of the CSV file containing the stats to change to. Can be a full path like `C:/keyblades.csv`.
- `jsonFolderPath=keyblades/` the path of the folder that contains all the `.json` files from the mod. Can be a full path like `C:/keyblades/`.
- `levelToChange=0` the keyblade upgrade level stats to change, `0` for the base stats and `1-10` for the upgrade level stats.
- `autoLevelStats=True` If set to True the upgrade level stats after the `levelToChange` level will be automatically calculated from the stats given from the CSV.
- `namesFile=names.json` the path of the JSON file containing the names that will be mapped to the JSON file names. Can be a full path like `C:/names.json`.
- `writeLog=True` enable whether the log should be created
- `skipMenuChoice=-1` set value to one of the options on the menu to skip the choice when running the script, setting the value to anything else will cause it to display the options

## Future improvements

- Ability to change other parts of the JSON files
- Alternative way to enter config options when running the script instead of relying on the config file
- Interface
