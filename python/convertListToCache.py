import sys

#############
# Convert List to cache set statements that can be pasted into a terminal
#############
def convertToCache(fname, var = 'array'):
	fileData = getData(fname)
	commands = makeOrderedList(var, fileData)
	newFile = fname[0:fname.rfind(".")] + ".M"
	saveCommands(commands, newFile)


def makeIndexedList(var, data):
	commands = []
	if var.find('(') == -1:
		var = var + '('
	for line in file:
		if line.find("\n") != -1:
			line = line[0:line.find("\n")]
		if (line.find("\t") != -1):
			(index, value) = line.split('\t')
			value = '"' + value + '"'
		else:
			index = line
			value = '1'
		command = 's ' + var + '"' + index + '")=' + value + '\n'
		commands.append(command)
	return commands


def makeOrderedList(var, data):
	if var.find('(') == -1:
		var = var + '($i(' + var + '))'
	commands = []
	for line in data:
		if line.find("\n") != -1:
			line = line[0:line.find("\n")]
		command = 'set ' + var + '="' + line + '"'
		commands.append(command)
	return commands
	

def getData(fname):
	f = open(fname, 'r')
	file = f.readlines()
	f.close()
	return file


def saveCommands(commands, fileName):
	with open(fileName, 'w') as f:
		for line in commands:
			f.write(line + "\n")
		f.close


########
if __name__ == "__main__":
    if (len(sys.argv) > 2):
    	convertToCache(sys.argv[1], sys.argv[2])
    if (len(sys.argv) == 2):
    	convertToCache(sys.argv[1])
