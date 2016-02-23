import csv

def getFieldNames():
	return ['Student', 'Reviewer', 'Student Activities', 'Leadership', 'Media Experience', 'Personal Statment', 'Notes']

def getNumValColumns():
	return ['Student Activities', 'Leadership', 'Media Experience', 'Personal Statment']


def processFile(file_name, output_file):
	data = loadCSVFile(file_name)
	reformattedData = scrubDataSet(data)  # Returns dictionary of students
	(keyList, newData) = recombineData(reformattedData)
	createCSVFile(newData, keyList, output_file)

def recombineData(studentDict):
	returnData = []
	numValCols = getNumValColumns()
	keyList = ['Student']
	#
	for student in studentDict:
		newRow = {}
		newRow['Student'] = student
		total = 0.0
		n = 0.0
		for review in studentDict[student]:
			reviewer = review['Reviewer']
			#
			for numField in getNumValColumns():
				if (len(review[numField]) == 1):
					total += int(review[numField])
					n +=1
				fieldName = numField + "_" +reviewer
				if (fieldName not in keyList):
					keyList.append(fieldName)
				newRow[fieldName] = review[numField]
			newRow['Average Score'] = total / n
			#
			notesField = "notes_" + reviewer
			newRow[notesField] = review['Notes']
			if (notesField not in keyList):
				keyList.append(notesField)
		#
		returnData.append(newRow)
	keyList.append('Average Score')
	noteFields = []
	for key in keyList:
		if ("notes_" in key):
			noteFields.append(key)
			keyList.remove(key)
	keyList.extend(noteFields)
	return (keyList, returnData)

def scrubData(entry):
	# Student, reviewer name, Student Activities,Leadership,Media Experience,Personal Statment,Notes
	data = {}
	mapping = ['Student', 'Student Activities', 'Leadership', 'Media Experience', 'Personal Statment', 'Notes']
	cleanup = getNumValColumns()
	if ('Reviewer Name' in entry):
		data['Reviewer'] = entry['Reviewer Name']
	else:
		data['Reviewer'] = 'missing'
	#
	for field in mapping:
		data[field] = entry[field]
	for field in cleanup:
		if (data[field] == '1 (Low)'):
			data[field] = '1'
		elif (data[field] == '4 (High)'):
			data[field] = '4'
	return data

def scrubDataSet(data):
	tempArray = {}
	for entry in data:
		entry = scrubData(entry)
		if (entry['Student'] not in tempArray):
			tempArray[entry['Student']] = []
		tempArray[entry['Student']].append(entry)
	return tempArray

# Load a *.tsv file and return a list of dictionaries of the values
#    tsv = Tab separated values
def loadCSVFile(file_name):
	with open(file_name) as file_handle:
		return [row for row in csv.DictReader(file_handle, delimiter=",")]

def createCSVFile(data, fieldnames, file_name):
	with open(file_name, 'w') as file_handle:
		writer = csv.DictWriter(file_handle, fieldnames = fieldnames, extrasaction='ignore')
		writer.writeheader()
		for entry in data:
			writer.writerow(entry)
