#############
# Convert List to cache set statements that can be pasted into a terminal
#############
def convertToCache(fname,var):
	f=open(fname,'r')
	file=f.readlines()
	f.close()
	newFile=fname[0:fname.find(".")] + ".M"
	f=open(newFile,'w')
	if var.find('(') == -1:
		var=var+'('
	for line in file:
		if line.find("\n") != -1:
			line=line[0:line.find("\n")]
		if (line.find("\t") != -1):
			(index,value)=line.split('\t')
			value = '"' + value + '"'
		else:
			index=line
			value = '1'
		val = 's ' + var + '"' + index + '")=' + value + '\n'
		f.write(val)
	f.close
