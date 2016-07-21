import urllib
import json
import os
import subprocess
import shutil
import argparse
import sys
import subprocess
from sys import platform as _platform




def log(text):
    if verbose :
        print(text)

def getMCDir():
    if _platform == "linux" or _platform == "linux2":
        return os.path.expanduser("~/.minecraft")
    elif _platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/minecraft")
    elif _platform == "win32":
        return os.path.realpath(os.getenv('APPDATA') + "\.minecraft")



def doStage(stageData) :
    for key in stageData :
        if stageData[key]["type"] == "resource":
            if not os.path.exists(modpackDir + stageData[key]["savedir"]) or stageData[key]["overwrite"] == True :
                if stageData[key]["dlmethod"] == "direct" :
                    testfile = urllib.FancyURLopener()
                    testfile.retrieve(stageData[key]["url"], modpackDir + stageData[key]["savedir"])
                elif stageData[key]["dlmethod"] == "inline":
                    with open(modpackDir + stageData[key]["savedir"], 'w') as file_:
                        file_.write(stageData[key]["data"])
                else :
                    print ("Could not find downlaod method for" + key)
        if stageData[key]["type"] == "mkdir" :
            if not os.path.exists(modpackDir + stageData[key]["dir"]):
                os.makedirs(modpackDir + stageData[key]["dir"])
        if stageData[key]["type"] == "rmdir" :
            if os.path.exists(modpackDir + stageData[key]["dir"]):
                shutil.rmtree(modpackDir + stageData[key]["dir"])
        if stageData[key]["type"] == "rm" :
            if os.path.exists(modpackDir + stageData[key]["dir"]):
                os.remove(modpackDir + stageData[key]["dir"])
        if stageData[key]["type"] == "addprofile" :
            with open(getMCDir() + "/launcher_profiles.json") as data_file:
                launcher_profiles = json.load(data_file)
            launcher_profiles["profiles"][stageData[key]["profile name"]] = stageData[key]["profile"]
            launcher_profiles["profiles"][stageData[key]["profile name"]]["gameDir"] = modpackDir
            with open(getMCDir() + "/launcher_profiles.json", 'w') as file_:
                    file_.write(json.dumps(launcher_profiles))
        if stageData[key]["type"] == "forge" :
            log("Detecting if '" + getMCDir() + "/versions/" + stageData[key]["vfoldername"] + "' exists!")
            if not os.path.exists(getMCDir() + "/versions/" + stageData[key]["vfoldername"]):
                if stageData[key]["dlmethod"] == "direct" :
                    testfile = urllib.FancyURLopener()
                    testfile.retrieve(stageData[key]["url"], modpackDir + "forge.jar")
                elif stageData[key]["dlmethod"] == "inline":
                    with open(modpackDir + "forge.jar", 'w') as file_:
                        file_.write(stageData[key]["data"])
                else :
                    print ("Could not find downlaod method for" + key)
                if os.path.exists(modpackDir + "forge.jar"):
                    subprocess.call(['java', '-jar', modpackDir + "forge.jar"])

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-m", "--modpackdir", help="Sets the directory the modpack will be installed to. (Default: cwd)",type=str)
parser.add_argument("-j", "--jsonfile", help="Sets the json file with the modpack data in. (Default: modpackdir/modpackData.json)",type=str)

args = parser.parse_args()

modpackDir = os.getcwd()


if args.modpackdir:
    modpackDir = args.modpackdir

jsonFileDir = modpackDir + "modpackData.json"

if args.jsonfile:
    jsonFileDir = args.jsonfile

verbose = args.verbose

log("Running modpack downloader");

log("Modpack installation directory is set to '" + modpackDir + "'");

log("Using '" + jsonFileDir +"' as JSON file.")
if not os.path.exists(jsonFileDir):
    sys.exit("Error: '" + jsonFileDir + "' is not a file.")

if not os.path.exists(modpackDir):
    log("'" + modpackDir + "' does not exist. Creating it now.");
    os.makedirs(modpackDir)


with open(jsonFileDir) as data_file:
    modpackData = json.load(data_file)

if not "stages" in modpackData:
    sys.exit("Error: The json file does not contain the element stages. Can not continue. Please report this to the author of the modpack.")

for stageData in modpackData["stages"]:
    doStage(stageData)
