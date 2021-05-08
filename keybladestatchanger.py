import csv
import json
import os.path

#CSV format: 
# keyblade name, base str, base mag

csvPath = "keyblades.csv" #input('Enter the path for the CSV file: ')
jsonFolder = "keyblades/" #input('Enter the path for the folder containing the JSONs: ')
levelToChange = 0
autoLevelStats = True
namesFile = "names.json"
writeLog = True

#Data read from CSV (key:keyblade, value:[str, mag])
keybladeCsvData = {}

#Names stored from names.json
keybladeNamesKey = {}

#Read names from json file
def readNames(): 
	global namesFile
	if os.path.exists(namesFile):
		with open(namesFile, 'r') as names:
			namesData = names.read()
			namesJson = json.loads(namesData)
			for key, value in namesJson.items():
				global keybladeNamesKey
				keybladeNamesKey[key] = value

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
				if (configdict[0] == "namesFile"):
					global namesFile
					namesFile = configdict[1].rstrip('\n')
				if (configdict[0] == "writeLog"):
					global writeLog
					writeLog = bool(configdict[1].rstrip('\n'))

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
	global levelToChange
	str = int(keybladeCsvData[keyblade][0])
	mag = int(keybladeCsvData[keyblade][1])
	i = 0
	for levels in keybladeJsonData[keyblade]["levels"]:
		if i >= levelToChange:
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
		if (levelToChange == 0 or not "levels" in keybladeJsonData[keyblade]):
			message = keyblade + ": (" + str(keybladeJsonData[keyblade]["base_stats"]["str"]) + ", " + str(keybladeJsonData[keyblade]["base_stats"]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
			print(message)
			keybladeJsonData[keyblade]["base_stats"]["str"] = int(keybladeCsvData[keyblade][0])
			keybladeJsonData[keyblade]["base_stats"]["mag"] = int(keybladeCsvData[keyblade][1])
		else:
			message = keyblade + ": (" + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["str"]) + ", " + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
			print(message)
			keybladeJsonData[keyblade]["levels"][levelToChange-1]["str"] = int(keybladeCsvData[keyblade][0])
			keybladeJsonData[keyblade]["levels"][levelToChange-1]["mag"] = int(keybladeCsvData[keyblade][1])
		if autoLevelStats and "levels" in keybladeJsonData[keyblade]:
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

readNames()

validCSV = False
validJSON = False
validNames = False

if (os.path.exists(csvPath)):
	validCSV = True
else:
	print("Invalid CSV path: " + csvPath)
if (os.path.exists(jsonFolder)):
	validJSON = True
else:
	print("Invalid JSON folder path: " + jsonFolder)
if (os.path.exists(namesFile)):
	validNames = True
else:
	print("Invalid Names JSON: " + namesFile)

if validCSV and validJSON and validNames:
	processStats()

	succeeded = 0
	total = 0

	if confirm("Write new stats to json files?"):
		if writeToLog:
			writeToLog("Format - Keyblade: (strength, magic) -> (new strength, new magic)", True)
		for keyblade in keybladeCsvData:
			total += 1
			if writeJson(keyblade, jsonFolder):
				succeeded += 1
				if (levelToChange == 0):
					message = keyblade + ": (" + str(keybladeJsonData[keyblade]["base_stats"]["str"]) + ", " + str(keybladeJsonData[keyblade]["base_stats"]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
				else:
					message = keyblade + ": (" + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["str"]) + ", " + str(keybladeJsonData[keyblade]["levels"][levelToChange-1]["mag"]) + ") -> " + "(" + keybladeCsvData[keyblade][0] + ", " + keybladeCsvData[keyblade][1] + ")"
				if writeToLog:
					writeToLog(message, False)
		print("Successfully written to " + str(succeeded) + "/" + str(total) + " file(s)")