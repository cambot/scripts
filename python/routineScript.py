from string import *	## {find}
# import os   # don't want os.open overwriting standard open
from os import chdir,listdir,mkdir,rmdir,path,remove,system
import filecmp		## {cmp}
import time		## {clock}

# - find
#import re
#import operator
#import urllib, sgmllib

#############
# Demonstrates:
#   set, repr   ## try-except
#   file: open, readlines, write, close
#   os interactions {listdir, mkdir, chdir, remove}
#   os.path usage {isdir, isfile, join, exists}
#
# Expected namespace folder structure
#   namespace
#	+- INT
#	+- MAC
#	+- Routines  (built by processNamespace())
##################


##################
# Callable Functions
#   processAll()   - works with start^JCMExportRoutines
#    processNamespace()
#     processRoutine() 
# 
#   deleteAll()
#    deleteDuplicate()
#     compareRoutines()
#
#   countRoutines()
#   writeLog()
#   getNamespaces()
#
#  -----
#   buildSVNBase(buildFlag=False)  - works with startSVN^JCMExportRoutines
#
##################



##################
# 1) Loops over namespace folders
# 2) loop over routines in a folder
# 3) extract routine from XML into new folder
# 4) Remove duplicate copies of routines
##################

##################
# 10/10 - 
# 10/11 - 2 hrs on deleteAll, 
# 10/13 - ~30 min on refactorings
# 10/21 - ~40 min on refactoring countRoutines
# 10/24 - 30 min updating processAll,deleteAll to accept lists of namespaces
# 2/26 - 10 min use Path module functions
##################



################################################################################
#  Strip Code from XML
################################################################################


#########
# Loop over namespaces (folders) in the present directory
#########
def processAll(nsList=[]):
	# pass in list, grab listdir(".") if passed nothing
	log=[]
	if len(nsList)==0:
		nsList=getNamespaces()
	for namespace in nsList:
		print namespace
		start=time.clock()
		processNamespace(namespace)
		finish=time.clock()
		elapsed=finish-start
		print "elapsed time: ",(finish-start)
		log.append(namespace+"\t"+repr(elapsed))
	writeLog(log,"timing-processAll.txt")
	print
	return 



#########
# Loop over files in the namespace folder & convert each routine to .\Routines\*.M
# Assumes: you are in the namespace folder
#########
def processNamespace(namespace):
	chdir(namespace)
	if path.exists("Routines"):
		for file in listdir(".\Routines"):
			remove(path.join("C:","Routines",file))
	else:
		mkdir("Routines")
	##
	if path.exists("MAC"):
		for file in listdir(".\MAC"):
			processRoutine(file,"MAC","Routines")
	##
	if path.exists("INT"):
		for file in listdir(".\INT"):
			processRoutine(file,"INT","Routines")
	chdir("..")
	#
	return


################
# Take file from src,
# Extract the code (strip the first and last 3 lines)
# Store as *.M in the <dest> directory
################
def processRoutine(fname,src,dest):
	xmlFile=fname
	chdir(src)
	#print xmlFile
	f=open(xmlFile,'r')
	file=f.readlines() #line stored as tuple (line#,line)
	f.close()
	chdir("..")
	chdir(dest)
	cacheFile=fname[0:fname.find(".xml")] + ".M"
	f=open(cacheFile,'w')
	for line in range(3,len(file)-2):
		f.write(file[line])
	f.close()
	chdir("..")
	#return parser

#def clear():


################################################################################
#  Deleting duplicate routines
################################################################################


#########
# Loop over namespaces and delete exact duplicates
#########
def deleteAll(nsList=[]):
	# pass in list, grab listdir(".") if passed nothing
	log=[]
	if len(nsList)==0:
		nsList=getNamespaces()
	nsList2=getNamespaces()
	print "--< Before Delete >--"
	countRoutines("tally-before.txt")
	for namespaceA in nsList:
		nsList2.remove(namespaceA)
		for namespaceB in nsList2:
			deleteDuplicates(namespaceB,namespaceA)  #remove routines from Namespaces provided
	print "--< After Delete >--"
	countRoutines("tally-after.txt")
	print
	return 


#########
# Removes duplicates from the second nspace directory
#########
def deleteDuplicates(nspace1,nspace2):
	path1=path.join("c:",nspace1,"Routines")
	path2=path.join("c:",nspace2,"Routines")
	if( path.isdir(path1)==False or path.isdir(path2)==False):
		return
	list1=listdir(path1)
	list2=listdir(path2)
	common=set(list1)&set(list2)
	for routine in common:
		if compareRoutines(nspace1,nspace2,routine):
			remove(path.join("c:",nspace2,"Routines",routine))
	return

########
# Wrapper for filecmp.cmp
########
def compareRoutines(dir1,dir2,routine):
	path1=path.join("c:",dir1,"Routines",routine)
	path2=path.join("c:",dir2,"Routines",routine)
	return filecmp.cmp(path1,path2)


################################################################################
#  convert code back to XML
################################################################################

############
# Converts .m to MAC in .xml format
# copies into nspace folder
############
def revertNamespace(nspace):
	directory=path.join("c:",nspace,"Routines")
	if path.isdir(directory):
		chdir(directory)
		for file in listdir("."):
			cacheToXML(file,True)
		chdir("..")
		system('copy .\Routines\* .\*')   # want to replace with 'pure' python solution
		for file in listdir(".\Routines"):
			remove(path.join("C:","Routines",file))
		rmdir('.\Routines')
		chdir("..")
	return

###########
# Converts .m to MAC in .xml format
###########
def cacheToXML(fname,removeOld):
	routine=fname[0:fname.find(".")]
	xmlFile=routine + ".xml"
	f=open(fname,'r')
	file=f.readlines() #line stored as tuple (line#,line)
	f.close()
	#
	f=open(xmlFile,'w')
	f.write('<?xml version="1.0" encoding="UTF-8"?>'+"\n")
	f.write('<Export generator="Cache" version="22" zv="Cache for Windows (x86-32) 2008.1.1 (Build 578)" ts="2009-10-22 11:32:47">' + "\n")
	f.write('<Routine name="' + routine + '" type="MAC" languagemode="0" timestamp="61656,41300"><![CDATA[' + "\n")
	for line in file:
		f.write(line)
	f.write(']]></Routine>' + "\n")
	f.write('</Export>' + "\n")
	f.close()
	if removeOld:
		remove(fname)
	return



################################################################################
#  general utilities
################################################################################


########
# Counts routines in all namespaces
# logs to a file
def countRoutines(fname):
	sum=0
	log=[]
	rouTally={}
	for namespace in getNamespaces():
		directory=path.join("c:",namespace,"Routines")
		if path.isdir(directory):
			rouList=listdir(directory)
			count=len(rouList)
			print namespace+"\t",count
			sum=sum+count
			log.append(namespace+"\t"+repr(count))
			for routine in rouList:
				if rouTally.has_key(routine):
					rouTally[routine]+=1
				else:
					rouTally[routine]=1
	#print "Total\t",sum
	log.append("Total\t"+repr(sum))
	log.append("\n")
	log.append("Number of routines:\t"+repr(len(rouTally)))
	for routine in sorted(rouTally.keys()):
		log.append(routine+"\t"+repr(rouTally[routine]))
	if (fname):
		writeLog(log,fname)
	return


########
# wrapper for file output
def writeLog(log,fname):
	f=open(fname,'w')
	for line in log:
		f.write(line+"\n")
	f.close()
	return

#########
# filters directories 
def getNamespaces():
	nsList=[]
	for namespace in listdir("."):
		if (path.isdir(namespace)):
			nsList.append(namespace)
	return nsList

#######################################################################
# Builds cache base for repository
# - Converts routines to .MAC
# - generates list of files in the 4 source directories
# - if buildFlag=True:
#   - removes file conflicts
#   - then merges source directories into master .\MAC folder

def buildSVNBase(buildFlag=False):
	start=time.clock()
	if path.isdir('MAC'):   # clear out MAC folder from previous run
		for file in listdir(".\MAC"):
			remove(path.join("c:","MAC",file))
		rmdir('MAC')
	nsList=getNamespaces()
	if 'CLS' in nsList:	# Class sub-folder
		nsList.remove('CLS')

	print "begin conversion to *.mac"
	processAll(nsList)
	for namespace in nsList:
		print namespace
		revertNamespace(namespace)
	print ".MAC Conversion complete"
	#
	#getFileLists()  # >>> not needed any more 
	#
	if (buildFlag):
		print "Removing known file conflicts"
		for namespace in nsList:
			chdir(namespace)
			removeFiles('RemoveList.txt')
			chdir('..')
		print "Building SVN Base"
		if path.isdir('MAC'):
			rmdir('MAC')	# clear out
		mkdir('MAC')		# copy into master \MAC folder
		#system('copy .\LTSYS\Routines\* .\MAC\*')		# copy LTSys
		system('copy .\LTMASTER\Routines\* .\MAC\*')	# overlay LTMaster
		system('copy .\NS-63\Routines\* .\MAC\*')		# overlay NS-63
		system('copy .\NS-185\Routines\* .\MAC\*')	# overlay NS-185
	# <<<
	print "Process complete"
	finish=time.clock()
	print "total elapsed time: ",(finish-start)
	f=open('timing-processAll.txt','a')
	f.write("\n"+"total run time:"+"\t"+repr(finish-start)+"\n")
	f.close()

########
# Deletes pre-defined list of files from source directory
def removeFiles(fname):
	if (not path.isfile(fname)):
		return
	f=open(fname,'r')
	file=f.readlines()
	f.close()
	for routine in file:
		if path.isfile(path.join("c:","Routines",routine)):
			remove(path.join("c:","Routines",routine))

##########
# Produces file listings for pre-build comparison
def getFileLists():
	system('dir .\LTSYS\Routines\* /b > FileList-LTSys.txt')
	system('dir .\LTMaster\Routines\* /b > FileList-LTMaster.txt')
	system('dir .\NS-63\Routines\* /b > FileList-63.txt')
	system('dir .\NS-185\Routines\* /b > FileList-185.txt')
