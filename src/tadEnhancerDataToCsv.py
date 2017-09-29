#script to write the enhancer/tad annotations to csv

import uuid
import os
import re
import csv

outputFolder = '../data/neo4jCsvImport/'

#Read the data from the files and parse these to CSV structured files for bulk upload to Neo4J

#Give a dictionary, we use the keys as headers for the csv, and immediately dump this in a file.
def writeToCsv(file, information, append):
	
	if append is False:
	
		with open(file, "wb") as outfile:
			writer = csv.writer(outfile)
			writer.writerow(information.keys())
			writer.writerows(zip(*information.values()))
	else:
		with open(file, "a") as outfile: #here we use append for when we are adding the enhancer information. 
			writer = csv.writer(outfile)
			writer.writerows(zip(*information.values()))
	
#Read the TAD annotation data

#If we store the information in columns (each key has an array of values), it is easier to transport between functions

#We then need to iteratively go through the 'rows' in each column to obtain the information that matches. The positions need to be concordant!
#What we can do alternatively is make the relations separate on the level of parsing.
#So then we parse 'Regions' with their properties, which can immediately be stored as a csv-formatted file
#Then we do the same for 'Annotations' and TADs and their properties.
#Because we read the data line by line, we can associate an identifier with each line.
#These can be stored in separate 'relationships' formats. 

#Make one folder with all the TAD annotations, we will obtain the relevant information per file
tadAnnotationFolder = '../data/tads/'

def parseTadDataFromFiles(folder):
	
	#These are all the nodes and properties for region nodes and annotation nodes 
	regions = dict()
	regions['regionId:ID'] = [] #ID indicates to Neo4J that the property is to be used as node ID
	regions['start:int'] = [] #type int for querying
	regions['end:int'] = []
	regions['chromosome'] = []
	annotations = dict()
	annotations['annotationId:ID'] = []
	annotations['cellType'] = []
	
	tad = dict()
	tad['id:ID'] = [1] #dummy ID, there will be only one TAD, this has no properties for now so it can be 1 node for all TADs, should have been tad_1 to be more precise
	
	#Defining the relations, start is the ID of the object and end is the ID of the subject
	regionsAnnotationsRelations = dict()
	regionsAnnotationsRelations[':START_ID'] = []
	regionsAnnotationsRelations[':END_ID'] = []
	
	#relations between annotations and their type (for now TADs or enhancers)
	annotationsAnnotationTypeRelations = dict()
	annotationsAnnotationTypeRelations[':START_ID'] = []
	annotationsAnnotationTypeRelations[':END_ID'] = [] #link to dummy TAD ID
	
	#Read through the folder with the TAD and enhancer data, process the files into information objects that we can send to Neo4J
	idCounter = 0
	for filename in os.listdir(folder):
		
		with open(folder + filename, "r") as ins:
			array = []
			for line in ins:
				line = line.strip()
				splitLine = re.split("\t", line)
				
				chromosome = splitLine[0]
				start = splitLine[1]
				end = splitLine[2]
				
				regionId = str(uuid.uuid4()) #unique IDs for nodes
				
				
				regions['regionId:ID'].append(regionId)
				regions['start:int'].append(start)
				regions['end:int'].append(end)
				regions['chromosome'].append(chromosome)
				
				splitFileName = re.split("\.", filename)
				cellType = splitFileName[0]
				
				annotationId = str(uuid.uuid4())
				
				annotations['annotationId:ID'].append(annotationId)
				annotations['cellType'].append(cellType)
				
				regionsAnnotationsRelations[':START_ID'].append(regionId)
				regionsAnnotationsRelations[':END_ID'].append(annotationId)
				
				annotationsAnnotationTypeRelations[':START_ID'].append(annotationId)
				annotationsAnnotationTypeRelations[':END_ID'].append(1)
				
				
	
	writeToCsv(outputFolder + 'tads.csv', tad, False)			
	writeToCsv(outputFolder + 'regions.csv', regions, False)
	writeToCsv(outputFolder + 'annotations.csv', annotations, False)
	writeToCsv(outputFolder + 'regions_annotations_rel.csv', regionsAnnotationsRelations, False)
	writeToCsv(outputFolder + 'annotations_annotationTypes_rel.csv', annotationsAnnotationTypeRelations, False)
	
parseTadDataFromFiles(tadAnnotationFolder)


#Repeat parsing, but then do the same for the enhancer data. We need to append to the existing CSV files however
def parseEnhancerDataFromFiles(folder):
	
	regions = dict()
	regions['regionId:ID'] = []
	regions['start:int'] = []
	regions['end:int'] = []
	regions['chromosome'] = []
	annotations = dict()
	annotations['annotationId:ID'] = []
	annotations['cellType'] = []
	
	enhancer = dict()
	enhancer['id:ID'] = ['enh_1'] #dummy enhancer ID
	
	regionsAnnotationsRelations = dict()
	regionsAnnotationsRelations[':START_ID'] = []
	regionsAnnotationsRelations[':END_ID'] = []
	
	annotationsAnnotationTypeRelations = dict()
	annotationsAnnotationTypeRelations[':START_ID'] = []
	annotationsAnnotationTypeRelations[':END_ID'] = [] #link to dummy TAD ID
	
	#Read through the folder, process the files into information objects that we can send to Neo4J
	idCounter = 0
	for filename in os.listdir(folder):
		
		#do something with this file
		with open(folder + filename, "r") as ins:
			array = []
			for line in ins:
				line = line.strip()
				splitLine = re.split("\t", line)
				
				chromosome = splitLine[0]
				start = splitLine[1]
				end = start
				
				regionId = str(uuid.uuid4())
				
				regions['regionId:ID'].append(regionId)
				regions['start:int'].append(start)
				regions['end:int'].append(end)
				regions['chromosome'].append(chromosome)
				
				splitFileName = re.split("\.", filename)
				cellType = splitFileName[0]
				
				#Celltypes, we need to add a new entry for every different celltype
				celltypes = splitLine[2]
				splitCellTypes = re.split(",", celltypes)
				
				for splitCellType in splitCellTypes:
					annotationId = str(uuid.uuid4())
				
					annotations['annotationId:ID'].append(annotationId)
					annotations['cellType'].append(splitCellType)
					
					regionsAnnotationsRelations[':START_ID'].append(regionId)
					regionsAnnotationsRelations[':END_ID'].append(annotationId)
					
					annotationsAnnotationTypeRelations[':START_ID'].append(annotationId)
					annotationsAnnotationTypeRelations[':END_ID'].append('enh_1')
				
				
	writeToCsv(outputFolder + 'enhancers.csv', enhancer, False)			
	writeToCsv(outputFolder + 'regions.csv', regions, True)
	writeToCsv(outputFolder + 'annotations.csv', annotations, True)
	writeToCsv(outputFolder + 'regions_annotations_rel.csv', regionsAnnotationsRelations, True)
	writeToCsv(outputFolder + 'annotations_annotationTypes_rel.csv', annotationsAnnotationTypeRelations, True)

enhancerAnnotationFolder = '../data/enhancers/'
parseEnhancerDataFromFiles(enhancerAnnotationFolder)