from string import split,find

#############
# Convert List to cache set statements that can be pasted into a terminal
#############
def convertToCache(fname,var):
	f=open(fname,'r')
	file=f.readlines()
	f.close()
	newFile=fname[0:fname.find(".")] + ".M"
	f=open(newFile,'w')
	if find(var,'(') == -1:
		var=var+'('
	for line in file:
		if find(line,"\n") <> -1:
			line=line[0:find(line,"\n")]
		if (find(line,"\t") <> -1):
			index,value=split(line,'\t',1)
			value = '"' + value + '"'
		else:
			index=line
			value = '1'
		val = 's ' + var + '"' + index + '")=' + value + '\n'
		f.write(val)
	f.close
