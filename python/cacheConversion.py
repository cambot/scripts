from string import *
# import os   # don't want os.open overwriting standard open
from os import walk, path, remove


def processAll(deleteFlag = False):
    processFolder('ManualExport', deleteFlag)
    processFolder('uat-sync', deleteFlag)
    processFolder('prod-sync', deleteFlag)
    return


def processFolder(folder, deleteFlag = False):
    target = '.\\' + folder + '\\cacheSources\\'
    print(target)
    for root, dirList, fileList in walk(target):
        if (len(fileList) > 0): print(root)
        fileType = root.split('\\')[3]
        for file in fileList:
            processFile(path.join(root, file), fileType)
        if (deleteFlag):
            for file in fileList:
                remove(path.join(root, file))
    return


################
# Take file <fname>,
# Extract the M/Cache code from the encompasing XML
# Store as *.M in the same directory
# For Mac, INC, and CSP files: (3, 2)
# For Classes: (2, 1)
################
def processFile(fname, fileType):
    xmlFile=fname
    with open(xmlFile,'r') as f:
        file=f.readlines() #line stored as tuple (line#,line)
    #
    extStart=fname.find(".xml")
    if (extStart == -1): return
    #
    cacheFile=fname[0:extStart] + ".M"
    leadingLines = 3
    trailingLines = 2
    if (fileType == "cls"):
        leadingLines = 2
        trailingLines = 1
    with open(cacheFile,'w') as f:
        for line in range(leadingLines, len(file)-trailingLines):
            f.write(file[line])
    return
    

############
# Need a function that outputs new/different/same comparison between files.
############

def compareFolders(dirA, dirB):
    return


########
# wrapper for file output
def writeLog(log,fname):
    with open(fname,'w') as f:
        for line in log:
            f.write(line+"\n")
    return

