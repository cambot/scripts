from os import mkdir,path,makedirs,system,remove
from shutil import copy2,rmtree,move
import csv
import sys

def packageRelease(release="yyyymmdd"):
    # requires git be installed in the windows %PATH% variable
    print("Checking out the release branch")
    system('git checkout release')
    system('git diff master release --name-status > ForRelease.txt')
    fileList = 'ForRelease.txt'
    changedFiles = importFileList(fileList)
    releaseFolderRoot = "For_Release_" + release
    if path.exists(releaseFolderRoot):
        rmtree(releaseFolderRoot, True)
    mkdir(releaseFolderRoot)
    releaseFolderRoot = path.join(".", releaseFolderRoot)
    for file in changedFiles:
        if (file[0] in ["A", "M"]):
            copyUpdatedFile(file[1], releaseFolderRoot)
        if (file[0][0] == "R"):  # Rename situation.
            copyRenamedFile(file[1], file[2], releaseFolderRoot)
        if (file[0] == "D"):
            print("Deleted: " + file[1])
    writeChangeFile(changedFiles, releaseFolderRoot)
    remove(fileList)


def importFileList(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip().split('\t') for x in content]
    return content


def copyUpdatedFile(fname, releaseFolderRoot):
    fileName = fname.replace("/", "\\")
    src = path.join(".", fileName)
    print (fileName)
    copyFile(src, fname.split('/'), releaseFolderRoot)


def copyRenamedFile(oldName, fname, releaseFolderRoot):
    fileName = fname.replace("/", "\\")
    src = path.join(".", fileName)
    print (oldName.replace("/", "\\") + "\t --> " + fileName)
    copyFile(src, fname.split('/'), releaseFolderRoot)


def copyFile(src, filePath, releaseFolderRoot):
    dest = path.join(releaseFolderRoot, "\\".join(filePath[0:-1]))
    if (not path.exists(dest)):
        makedirs(dest)
    copy2(src, dest)
    copyClass(src, filePath, releaseFolderRoot)


def copyClass(src, filePath, releaseFolderRoot):
    if (len(filePath) > 2):
        if ((filePath[0] == "cacheSources") and (filePath[1]=="cls")):
            fileName = ".".join(filePath[2:])
            dest = path.join(releaseFolderRoot, "\\".join(filePath[0:2]), fileName)
            copy2(src, dest)


def writeChangeFile(fileList, releaseFolderRoot):
    outputFile = path.join(releaseFolderRoot, 'changeList.tsv')
    with open(outputFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        for file in fileList:
            writer.writerow(file)


if __name__ == "__main__":
    packageRelease(sys.argv[1])
