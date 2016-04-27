from os import listdir
from zipfile import *	## {is_zipfile, ZipFile, namelist, extract}
from string import *	## {find}

########
# search all zip files in the present directory for file names containing <string>
# and extract them to the present working directory
def zFileFind(string):
	for item in listdir("."):
		if is_zipfile(item):
			zFile=ZipFile(item, 'r')
			print ' -----< ' + item + ' >-----'
			for file in zFile.namelist():
				if find(file, string) > 0:
					print file
					zFile.extract(file)  # extract file to pwd
