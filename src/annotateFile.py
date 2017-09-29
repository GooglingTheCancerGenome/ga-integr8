#Provide file as input with the true positives

#Provide output file that will have all the features

#For each of these, query the database and obtain the relevant features (annotateRegion script)

#These features need to be stored in a way such that we can easily convert them to the machine learning format (this is optional, not sure if we will stay with this format, so for now it can be an easy column-based format)

import sys
import csv
from annotateRegion import annotate

inFile = sys.argv[1]
outFile = sys.argv[2]

#Read the input tsv file
#We want the chromosome columns and the start and end


allFeatures = dict()

lineCount = 0
header = []
with open(inFile) as tsv:
	for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
		#Obtain the header
		if lineCount == 0:
			lineCount += 1
			header = line
			continue
			
		if lineCount > 1000:
			break #check how long it takes to annotate
			
		else: #check if the chromosome positions are different, skip these for now since the annotation does not work with it yet
			
			chromosome = ["chr" + line[0]]
			chromosome2 = ["chr" + line[1]]
			start = [line[2]]
			end = [line[3]]
			
			#orientation = line[4] #This format is not correct yet, orientations differ between files
			
			#Call annotateRegion
			
			region = dict()
			region['start'] = start
			region['end'] = end #use the furthest away end for now, we only do overlap queries to get the features
			region['chromosomes'] = chromosome
			region['chromosomes2'] = chromosome2
			
			features = annotate(region)
			
			for key in features.keys():
				if key not in allFeatures.keys():
					allFeatures[key] = []
				allFeatures[key].append(features[key])
		
		lineCount += 1

#Write the features to a file

from csv import DictWriter
dictionary = allFeatures
zd = zip(*dictionary.values())
with open(outFile, 'w') as file:
	writer = csv.writer(file, delimiter='\t')
	writer.writerow(dictionary.keys())
	writer.writerows(zd)
	
#When writing the dictionary to a file, the order of the features will always be different
#We can read the columns into vectors by their key, and then use this key to compare the different SV types if we need to, otherwise they can stay in different order