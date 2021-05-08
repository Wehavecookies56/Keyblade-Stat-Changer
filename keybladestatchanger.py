import csv
import json
import os.path

#CSV format: 
# keyblade name, base str, base mag

csvPath = "keyblades.csv" #input('Enter the path for the CSV file: ')
jsonFolder = "keyblades/" #input('Enter the path for the folder containing the JSONs: ')
levelToChange = 0
autoLevelStats = True

#Data read from CSV (key:keyblade, value:[str, mag])
keybladeCsvData = {}

#Manually added here (key:keyblade localised name, value:keyblade file name)
keybladeNamesKey = {
	"Abaddon Plasma": "abaddon_plasma",
	"Abyssal Tide": "abyssal_tide",
	"Aced's Keyblade": "aceds_keyblade",
	"All For One": "all_for_one",
	"Astral Blast": "astral_blast",
	"Aubade": "aubade",
	"Ava's Keyblade": "avas_keyblade",
	"Bond of Flame": "bond_of_flame",
	"Bond of the Blaze": "bond_of_the_blaze",
	"Brightcrest": "brightcrest",
	"Chaos Ripper": "chaos_ripper",
	"Circle of Life": "circle_of_life",
	"Counterpoint": "counterpoint",
	"Crabclaw": "crabclaw",
	"Crown of Guilt": "crown_of_guilt",
	"Darker than Dark": "darker_than_dark",
	"Darkgnaw": "darkgnaw",
	"Decisive Pumpkin": "decisive_pumpkin",
	"Destiny's Embrace": "destinys_embrace",
	"Diamond Dust": "diamond_dust",
	"Divewing": "divewing",
	"Divine Rose": "divine_rose",
	"Dual Disc": "dual_disc",
	"Earthshaker": "earthshaker",
	"End of Pain": "end_of_pain",
	"Ends of the Earth": "ends_of_the_earth",
	"Fairy Harp": "fairy_harp",
	"Fairy Stars": "fairy_stars",
	"Fatal Crest": "fatal_crest",
	"Fenrir": "fenrir",
	"Ferris Gear": "ferris_gear",
	"Follow the Wind": "follow_the_wind",
	"Frolic Flame": "frolic_flame",
	"Glimpse of Darkness": "glimpse_of_darkness",
	"Guardian Bell": "guardian_bell",
	"Guardian Soul": "guardian_soul",
	"Gula's Keyblade": "gulas_keyblade",
	"Gull Wing": "gull_wing",
	"Hero's Crest": "heros_crest",
	"Hidden Dragon": "hidden_dragon",
	"Hyperdrive": "hyperdrive",
	"Incomplete X-blade": "incomplete_kiblade",
	"Invi's Keyblade": "invis_keyblade",
	"Ira's Keyblade": "iras_keyblade",
	"Jungle King": "jungle_king",
	"Keyblade of People's Hearts": "keyblade_of_peoples_hearts",
	"X-blade": "kiblade",
	"Kingdom Key": "kingdom_key",
	"Kingdom Key D": "kingdom_key_d",
	"Knockout Punch": "knockout_punch",
	"Lady Luck": "lady_luck",
	"Leviathan": "leviathan",
	"Lionheart": "lionheart",
	"Lost Memory": "lost_memory",
	"Lunar Eclipse": "lunar_eclipse",
	"Mark of a Hero": "mark_of_a_hero",
	"Master's Defender": "masters_defender",
	"Maverick Flare": "maverick_flare",
	"Metal Chocobo": "metal_chocobo",
	"Midnight Roar": "midnight_roar",
	"Mirage Split": "mirage_split",
	"Missing Ache": "missing_ache",
	"Monochrome": "monochrome",
	"Moogle O' Glory": "moogle_o_glory",
	"Mysterious Abyss": "mysterious_abyss",
	"Nightmare's End": "nightmares_end",
	"Combined Keyblade": "nightmares_end_and_mirage_split",
	"No Name": "no_name",
	"No Name (BBS)": "no_name_bbs",
	"Oathkeeper": "oathkeeper",
	"Oblivion": "oblivion",
	"Ocean's Rage": "oceans_rage",
	"Olympia": "olympia",
	"Omega Weapon": "omega_weapon",
	"Ominous Blight": "ominous_blight",
	"One Winged Angel": "one_winged_angel",
	"Pain of Solitude": "pain_of_solitude",
	"Photon Debugger": "photon_debugger",
	"Pixie Petal": "pixie_petal",
	"Pumpkinhead": "pumpkinhead",
	"Rainfell": "rainfell",
	"Rejection of Fate": "rejection_of_fate",
	"Royal Radiance": "royal_radiance",
	"Rumbling Rose": "rumbling_rose",
	"Shooting Star": "shooting_star",
	"Sign of Innocence": "sign_of_innocence",
	"Silent Dirge": "silent_dirge",
	"Skull Noise": "skull_noise",
	"Sleeping Lion": "sleeping_lion",
	"Soul Eater": "soul_eater",
	"Spellbinder": "spellbinder",
	"Star Seeker": "star_seeker",
	"Starlight": "starlight",
	"Stormfall": "stormfall",
	"Stroke of Midnight": "stroke_of_midnight",
	"Sweet Dreams": "sweet_dreams",
	"Sweet Memories": "sweet_memories",
	"Sweetstack": "sweetstack",
	"Three Wishes": "three_wishes",
	"Total Eclipse": "total_eclipse",
	"Treasure Trove": "treasure_trove",
	"True Light's Flight": "true_lights_flight",
	"Twilight Blaze": "twilight_blaze",
	"Two Become One": "two_become_one",
	"Ultima Weapon (BBS)": "ultima_weapon_bbs",
	"Ultima Weapon (DDD)": "ultima_weapon_ddd",
	"Ultima Weapon (KH1)": "ultima_weapon_kh1",
	"Ultima Weapon (KH2)": "ultima_weapon_kh2",
	"Ultima Weapon (KH3)": "ultima_weapon_kh3",
	"Umbrella": "umbrella",
	"Unbound": "unbound",
	"Victory Line": "victory_line",
	"Void Gear": "void_gear",
	"Void Gear (Remnant)": "void_gear_remnant",
	"Way to the Dawn": "way_to_the_dawn",
	"Wayward Wind": "wayward_wind",
	"Winner's Proof": "winners_proof",
	"Wishing Lamp": "wishing_lamp",
	"Wishing Star": "wishing_star",
	"Young Xehanort's Keyblade": "young_xehanorts_keyblade",
	"Zero/One": "zero_one"
}

#JSON data read from json files (key:keyblade name, value:json data)
keybladeJsonData = {}

#Load config if it exists format:key=value
def loadConfig():
	if os.path.exists("config.cfg"):
		with open("config.cfg", 'r') as cfgFile:
			config = cfgFile.readlines()
			for line in config:
				configdict = str(line).split("=")
				if (configdict[0] == "csvPath"):
					global csvPath
					csvPath = configdict[1].rstrip('\n')
				if (configdict[0] == "jsonFolderPath"):
					global jsonFolder
					jsonFolder = configdict[1].rstrip('\n')
				if (configdict[0] == "levelToChange"):
					global levelToChange
					levelToChange = int(configdict[1].rstrip('\n'))
				if (configdict[0] == "autoLevelStats"):
					global autoLevelStats
					autoLevelStats = bool(configdict[1].rstrip('\n'))

#Converts the localised keyblade names from the csv to the file name for the jsons
def buildFileName(name, folder):
	if not folder.endswith('/'):
		folder+='/'
	return folder + keybladeNamesKey[name] + ".json"

#Reads the csv file and stores all the data in the dictionary
def readCSV():
	with open(csvPath, newline='') as csvfile:
		datareader = csv.reader(csvfile)
		for row in datareader:
			keybladeCsvData[row[0]] = [row[1], row[2]]

#Reads the given json file and stores the data in the dictionary
def readJSON(name, folder):
	fileName = buildFileName(name, folder)
	with open(fileName, 'r') as file:
		data = file.read()
		jsondata = json.loads(data)
		keybladeJsonData[name] = jsondata;

#Takes the base stats from the csv and sets the level stats mag+1 every even, str+1 every odd
def calculateLevelStats(keyblade):
	str = int(keybladeCsvData[keyblade][0])
	mag = int(keybladeCsvData[keyblade][1])
	i = 0
	for levels in keybladeJsonData[keyblade]["levels"]:
		if i % 2 == 0:
			mag += 1
			levels["mag"] = mag
			levels["str"] = str
		else:
			str += 1
			levels["str"] = str
			levels["mag"] = mag
		i += 1

#Write a given message to log file, new param to create the file or clear an old one
def writeToLog(message, new):
	if os.path.exists("changes.log"):
		if not new:
			with open("changes.log", 'a') as log:
				log.write(message + "\n")
		else:
			with open("changes.log", 'w') as log:
				log.seek(0)
				log.write(message + "\n")
				log.truncate()
	elif new:
		with open("changes.log", 'x') as log:
			log.write(message + "\n")

#Reads all the data and sets the new stats ready for writing to the files, displays the base stat changes
def processStats():
	readCSV()
	for keyblade in keybladeCsvData:
		readJSON(keyblade, jsonFolder)
		global autoLevelStats, levelToChange
		if (levelToChange == 0):
			message = keyblade + ": (" + str(keybladeJsonData[keyblade]["base_stats"]["str"]) + ", " + str(keybladeJsonData[keyblade]["base_stats"]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
			print(message)
			keybladeJsonData[keyblade]["base_stats"]["str"] = int(keybladeCsvData[keyblade][0])
			keybladeJsonData[keyblade]["base_stats"]["mag"] = int(keybladeCsvData[keyblade][1])
		else:
			message = keyblade + ": (" + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["str"]) + ", " + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
			print(message)
			keybladeJsonData[keyblade]["levels"][levelToChange-1]["str"] = int(keybladeCsvData[keyblade][0])
			keybladeJsonData[keyblade]["levels"][levelToChange-1]["mag"] = int(keybladeCsvData[keyblade][1])
		if autoLevelStats and levelToChange == 0:
			calculateLevelStats(keyblade)

#bool confirm input
def confirm(message):
	confirmInput = input(message + " (Y/N) ")
	if (confirmInput == "Y" or confirmInput == "y"):
		return True
	elif (confirmInput == "N" or confirmInput == "n"):
		return False
	else:
		print("Invalid input")
		return confirm(message)

#writes the json data to the given file
def writeJson(keyblade, folder):
	fileName = buildFileName(keyblade, folder)
	with open(fileName, 'w') as file:
		tofile = json.dumps(keybladeJsonData[keyblade], indent=4)
		file.seek(0)
		file.write(tofile)
		file.truncate()
		return True
	return False

loadConfig()

validCSV = False
validJSON = False

if (os.path.exists(csvPath)):
	validCSV = True
else:
	print("Invalid CSV path: " + csvPath)
if (os.path.exists(jsonFolder)):
	validJSON = True
else:
	print("Invalid JSON folder path: " + jsonFolder)

if validCSV and validJSON:
	processStats()

	succeeded = 0
	total = 0

	if confirm("Write new stats to json files?"):
		writeToLog("Format - Keyblade: (strength, magic) -> (new strength, new magic)", True)
		for keyblade in keybladeCsvData:
			total += 1
			if writeJson(keyblade, jsonFolder):
				succeeded += 1
				if (levelToChange == 0):
					message = keyblade + ": (" + str(keybladeJsonData[keyblade]["base_stats"]["str"]) + ", " + str(keybladeJsonData[keyblade]["base_stats"]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
				else:
					message = keyblade + ": (" + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["str"]) + ", " + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
				writeToLog(message, False)
		print("Successfully written to " + str(succeeded) + "/" + str(total) + " file(s)")