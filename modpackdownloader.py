import urllib
import json
import os
import subprocess

with open('modpackData.json') as data_file:    
    modpackData = json.load(data_file)


def doStage(stageData) :
	for key in stageData :
		if stageData[key]["type"] == "resource":
			if stageData[key]["dlmethod"] == "direct" :
				testfile = urllib.FancyURLopener()
				testfile.retrieve(stageData[key]["url"], stageData[key]["savedir"])
			else :
				print ("Could not find downlaod method for" + key)
		if stageData[key]["type"] == "forge" :
			if stageData[key]["dlmethod"] == "direct" :
				testfile = urllib.FancyURLopener()
				testfile.retrieve(stageData[key]["url"],"forge.jar")
			else :
				print ("Could not find downlaod method for" + key)
		if stageData[key]["type"] == "mkdir" :
			if not os.path.exists(stageData[key]["dir"]):
				os.makedirs(stageData[key]["dir"])
		
			
for stageData in modpackData:
	doStage(stageData)
