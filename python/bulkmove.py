from os import listdir,mkdir,path
from shutil import move
from string import find

###
# move list of files into a subfolder
# Usage:
#  fileList=readInList(<file Name>)
#  moveList(fileList,<folder>)
###



#######
# read list from file
def readInList(fname):
	f=open(fname,'r')
	file=f.readlines()
	f.close()
	fileList=[]
	for line in file:
		if find(line,"\n") <> -1:
			line=line[0:find(line,"\n")]
		fileList.append(line)
	return fileList


########
# moves list of files into subfolder
def moveList(fileList,folder):
	if path.isdir(folder)==False:
		mkdir(folder)
	dirList=getfiles()
	for item in dirList:
		if item in fileList:
			move(item,folder)
			fileList.remove(item)
	for item in fileList:
		print item+" not found"


#########
# filters files from directories 
def getfiles():
	nsList=[]
	for item in listdir("."):
		if (path.isfile(item)):
			nsList.append(item)
	return nsList	
