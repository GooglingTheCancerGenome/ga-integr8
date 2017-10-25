
#1. Read the folder with the TAD data

#2. Process the separate files to a csv with headers (start, end, celltypes)

import os
import re
import numpy as np
from utilities import writeToCsv

tadAnnotationFolder = '../data/tads/'


def writeTADsToCsv(file, tads):
	
	header = 'chromosome\tstart\tend\tcelltypes\n'
	
	with open(file, "wb") as outfile:
		outfile.write(header)
		
		for row in range(0, len(tads)):
			line = tads[row][0] + '\t' + tads[row][1] + '\t' + tads[row][2] + '\t' + tads[row][3] + '\n'
			outfile.write(line)

def parseTadDataFromFiles(folder):
	
	tads = dict()
	tads['start'] = []
	tads['end'] = []
	tads['chromosome'] = []
	tads['celltypes'] = []
	
	tads = []
	
	#keep a separate index through which we can quickly search if the start/end/chr combination already exists and in which position
	indexList = []
	
	#Read through the folder with the TAD data and merge these into one file
	count = 0
	for filename in os.listdir(folder):
		
		# count += 1
		# if count > 2:
		# 	break
		
		with open(folder + filename, "r") as ins:
			array = []
			for line in ins:
				line = line.strip()
				splitLine = re.split("\t", line)
				
				chromosome = splitLine[0]
				start = splitLine[1]
				end = splitLine[2]
				
				splitFileName = re.split("\.", filename)
				cellType = splitFileName[0]
				
				indexKey = chromosome + '_' + start + '_' + end
				print indexKey
				if indexKey not in indexList:
					indexList.append(indexKey)
					# position = index.keys().index(indexKey)
					# print "can be found at: ", tads['start'][position]
					# print "can be found at: ", tads['end'][position]
					# print "can be found at: ", tads['chromosome'][position]
					#Also add the new tad information
					#tads['start'].append(start)
					#tads['end'].append(end)
					#tads['chromosome'].append(chromosome)
					#tads['celltypes'].append(cellType)
					
					tads.append([chromosome, start, end, cellType])
					
				else:
					#find the index at which this position is stored
					#append the celltype.
					position = indexList.index(indexKey)
				#	print "appending at: "
				#	print "can be found at: ", tads['start'][position]
				#	print "can be found at: ", tads['end'][position]
				#	print "can be found at: ", tads['chromosome'][position]
					#tads['celltypes'][position] = tads['celltypes'][position] + ", " + cellType #add the celltype, the rest of the information about start and end is already in place
					tads[position][3] = tads[position][3] + ", " + cellType			
	
	#Sort the file by chromosome and positions as well, this saves time when searching through the file.
	tads = np.array(tads)
	
	#Obtain the columns that we wish to sort by
	chr1col = tads[:,0]
	chr2col = tads[:,1]
	
	sortedInd = np.lexsort((chr2col, chr1col)) #sort first by column 1, then by column 2. This works, but it is lexographical, so chromosome 11 comes before chromosome 2. This is ok for this purpose, but maybe not for others!
	
	sortedTads = tads[sortedInd]
	
	writeTADsToCsv('../data/tads.csv', sortedTads)
	# writeToCsv(outputFolder + 'tads.csv', tad, False)			
	# writeToCsv(outputFolder + 'regions.csv', regions, False)
	# writeToCsv(outputFolder + 'annotations.csv', annotations, False)
	# writeToCsv(outputFolder + 'regions_annotations_rel.csv', regionsAnnotationsRelations, False)
	# writeToCsv(outputFolder + 'annotations_annotationTypes_rel.csv', annotationsAnnotationTypeRelations, False)
	# 
parseTadDataFromFiles(tadAnnotationFolder)

			