import csv
import json
import os
import sys

from process import *

################################
# Developed on 3.9.6

def process(swaggerFile):
    print("Loading Swagger File.")
    swaggerSpecs = extractSwaggerData(swaggerFile)
    postmanCollections = loadPostmanCatalogue()
    fieldNames = ['url', 'type', 'applications', 'permissions check', 'permissions']
    tallyColumns = []
    postmanFields = ['url', 'queryString', 'type', 'name']
    for collection, file, column in postmanCollections:
        print("\nLoading " + collection)
        postmanRequests = extractPostmanCollection(os.path.join('.//data//', collection))
        saveToCSV(file, postmanFields, postmanRequests)
        fieldNames.append(column)
        tallyColumns.append(column)
        swaggerSpecs = tallyPostmanRequests(swaggerSpecs, postmanRequests, column)
    fieldNames = fieldNames + ['Total', 'summary', 'description']
    saveToCSV('.//API_Gap_Analysis.csv', fieldNames, swaggerSpecs)


def loadPostmanCatalogue(fileName = './/data//collections.csv'):
    postmanCollections = []
    with open(fileName, 'r', newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter='\t')
        for row in csvReader:
            record = {
                'collection': row[0],
                'csv_file': row[1],
                'subtally_column': row[2],
            }
            postmanCollections.append(row)
        csvFile.close()
    return postmanCollections


def tallyPostmanRequests(apiList, postmanCollection, tallyColumn):
    for request in postmanCollection:
        match = False
        for record in apiList:
            if tallyColumn not in record:
                record[tallyColumn] = 0
            if requestsMatch(record, request):
                #print("Matched: " + record['url'] + " to " + request['url'])
                record[tallyColumn] = record[tallyColumn] + 1
                record['Total'] = record['Total'] + 1
                match = True
                continue
        if (match == False):
            print("Could not match postman request for " + request['url'])
    return apiList


def extractSwaggerData(swaggerFile):
    jsonData = loadJSONRecord(swaggerFile)
    return processSwaggerRecord(jsonData)


def extractPostmanCollection(postmanFile):
    jsonData = loadJSONRecord(postmanFile)
    requests = processPostmanFolder(jsonData['item'])
    return requests

def processPostmanFolder(postmanFolder):
    output = []
    for request in postmanFolder:
        if 'item' in request:
            output += processPostmanFolder(request['item'])
        else:
            output.append(extractPostmanRecord(request))
    return output


def loadJSONRecord(file):
    with open(file, 'r') as fp:
        jsonData = json.load(fp)
        fp.close()
    return jsonData


def loadCSVrecord(fileName):
    with open(fileName, 'r', newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        header = None
        records = []
        for row in csvReader:
            if (header == None):
                header = row
            else:
                record = {
                    'url': row[0],
                    'type': None,
                    'applications': row[1],
                    'permissions': row[2],
                }
                records.append(record)
        csvFile.close()
    return (header, records)


def saveToCSV(outputCSV, fieldNames, dataRecords):
    with open(outputCSV, 'w', newline='', encoding='utf-8') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldNames)
        csvWriter.writeheader()
        for record in dataRecords:
            csvWriter.writerow(record)
        csvFile.close()


if __name__ == "__main__":
    #print(sys.argv)
    if (len(sys.argv) == 2):
        process(swaggerFile = sys.argv[1])
    else:
        print("Please supply a file name.")
