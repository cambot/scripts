from string import *
# import os   # don't want os.open overwriting standard open
from os import walk, path, remove
import filecmp
import sys


def allEnvironments():
    return ['prod-sync', 'uat-sync', 'ManualExport']


def processAll(envList, deleteFlag = True):
    for env in envList:
        processFolder(env, deleteFlag)
    if ('prod-sync' not in envList): return
    if ('ManualExport' in envList):
        compareFolders('prod-sync', 'ManualExport', 'prod-vs-local_diff-only.tsv')
    if ('uat-sync' in envList):
        compareFolders('prod-sync', 'uat-sync', 'prod-vs-uat_diff-only.tsv')
    return


def processFolder(folder, deleteFlag = True):
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
def compareFolders(dirA, dirB, logFileName="CompareLog.tsv", diffOnly = True):
    targetA = '.\\' + dirA + '\\cacheSources\\'
    targetB = '.\\' + dirB + '\\cacheSources\\'
    compareDirectories(filecmp.dircmp(targetA, targetB), ".", logFileName, diffOnly)
    return


def compareDirectories(dcmp, refPath, logFileName="CompareLog.tsv", diffOnly = True):
    log = []
    refPath = refPath + "\\"
    #
    log.extend([refPath + file + "\tA Only" for file in dcmp.left_only])
    log.extend([refPath + file + "\tB Only" for file in dcmp.right_only])
    log.extend([refPath + file + "\tA <> B" for file in dcmp.diff_files])
    if (not diffOnly): log.extend([refPath + file + "\tA == B" for file in dcmp.same_files])
    writeLog(log, logFileName)
    for subFolder in dcmp.subdirs:
        compareDirectories(dcmp.subdirs[subFolder], refPath + subFolder, logFileName)
    return


########
# wrapper for file output
def writeLog(log,fname):
    with open(fname,'a') as f:
        for line in log:
            f.write(line+"\n")
    return

########
if __name__ == "__main__":
    envList = ['git-release-branch', 'git-master-branch']
    if (len(sys.argv) > 1):
        envList.append(sys.argv[1])
    processAll(envList)
