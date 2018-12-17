#may want to make this more modular for multiple things

import json
import os

#file load and save stuff
def fileSave(fileName,config):
    #print("Saving")
    f = open(fileName, 'w') #opens the file your saving to with write permissions
    f.write(json.dumps(config,sort_keys=True, indent=4 ) + "\n") #writes the string to a file
    f.close() #closes the file io

def fileLoad(fileName):#loads files
    with open(fileName, 'r') as handle:#loads the json file
        config = json.load(handle) 
    return config

def loadConf(file):
    file = fileLoad(file.format(os.sep))
    return file

def checkFolder(folderPath,folderName,logger):
    if os.path.isdir(folderPath) == False:
        logger.logger.info("{0} Folder Does Not Exist".format(folderName))
        logger.logger.info("Creating...")
        os.makedirs(folderPath)

def checkFile(examplePath,filePath,fileName,logger):
    if (os.path.isfile(filePath) == False):
        logger.logger.info("{0} File Does Not Exist".format(fileName))
        logger.logger.info("Creating...")
        data = fileLoad(examplePath)
        fileSave(filePath,data)