#!/usr/bin/env python

__author__ = "Marleen Nieboer"
__credits__ = []
__maintainer__ = "Marleen Nieboer"
__email__ = "m.m.nieboer@umcutrecht.nl"
__status__ = "Development"

import sys
sys.path.append('settings/') #Add settings path
import settings
import numpy as np
import time

#Separate class to do the overlap functionality.

#It would be great if all functionality to obtain annotations would each be in separate classes. These can then also be swapped out if needed. 
#Maybe it is good to also have some sort of interface to write against to make sure that all classes are always in the same format (with the same functions). 

class TADFeatureHandler:
	
	#Annotate will accept all SVs that need to be annotated, and return the annotations for these SVs.
	#SVs format:
	#annotations format: a dictionary with annotations. {'featureName' : [values]}, where values is in the same order as the SVs. 
	
	#enabledFeatures is an optional parameter. A list can be provided that contains the names of features that are enabled in the settings. If necessary, certain features that have been disabled
	#do not need to be obtained from the file, or do not need to be computed to save computational time.
	def annotate(self, regions, enabledFeatures = None):
		
		#1. read the TAD file
		tadData = self.readTADFile()
		#2. Overlap the regions with the TADs
		
		
		#3. Compute how much of the TAD is disrupted

		
		annotations = self.computeTADFeatures(regions, tadData)
		
		
		return annotations
	
	def readTADFile(self):
		
		tadFile = settings.inputFiles['tads']
		
		#Read the gene list data into a list
		tadData = []
		with open(tadFile, "r") as f:
			lineCount = 0
			for line in f:
				if lineCount < 2: #skip header
					lineCount += 1
					continue
				line = line.strip()
				splitLine = line.split("\t")
				
				
				#We are interested in the positional information to see which gene is closest. (Add more later)
				
				#Convert the numbers to integers for quicker comparison. 0 is chromosome, 1 is start, 2 is end. Celltypes are not used for now. 
				splitLine[1] = int(splitLine[1])
				splitLine[2] = int(splitLine[2])
				
				#chr, start, end
				tadData.append([splitLine[0], splitLine[1], splitLine[2]])
		
		#Also convert the other dataset to numpy
		tadData = np.array(tadData, dtype='object')
	
		return tadData
		
	
	#This is the simple overlap that can be done quickly, then we can compute how much of a TAD is affected
	#1. Find the number of TADs that are disrupted
	#2. Find the number of disrupted boundaries
	#3. Find the distance to the nearest TAD (this will again be relatively slow since we need to use distance queries. Is there still a way to speed it up?)
	def computeTADFeatures(self, regions, tadData):
		annotations = dict()
		
		#1. How many tads overlap with each region?
		annotations['overlappingTadCount'] = self.computeNumberOfOverlappingTADs(regions, tadData)
		
		#2. How many boundaries are disrupted by an SV?
		#- for this query, we need to check if the SV directly overlaps with either a start or end coordinate, so cases where the SV is within the TAD should not count. 
		
		return annotations
	
	def computeNumberOfOverlappingTADs(self, regions, tadData):
		
		overlappingTads = []
		
		#Do the actual filtering. Make sure that all files have been pre-processed to save time here
		previousChr1 = None
		previousChr2 = None
		
		#len(regions)
		for lineCount in range(0, len(regions)):
			#print lineCount
			#Make sure to filter the dataset per chromosome! Good when sorted, we can keep it until we hit the next chromosome
			#The genes are not cross-chromosomal, but translocations can be, so we need to check both chromosome entries!
			
			#Obtain start and end positions and chromosome (chr 1 and 2)
			lineList = regions[lineCount,:]
			
			#We should check the chromosome of the previous line.
			#This would work nicely if the input file has been properly sorted! We probably need a pre-sorting to make this work. 
			if str(lineList[0]) != previousChr1 and str(lineList[3]) != previousChr2:
				
				#Find the two subsets that match on both chromosomes. 
				matchingChr1Ind = tadData[:,0] == 'chr' + lineList[0]
				matchingChr2Ind = tadData[:,0] == 'chr' + lineList[3] #The tad entry is here the same since the genes are only on 1 chromosome. 
				
				#It is not even necessary to make 2 lists if both chromosomes are the same, we could use a reference without re-allocating
				chr1Subset = tadData[np.where(matchingChr1Ind)]
				if lineList[0] == lineList[3]:
					chr2Subset = chr1Subset
				else:
					chr2Subset = tadData[np.where(matchingChr2Ind)]
				
				#Make sure to update the previous chromosome when it changes
				previousChr1 = 'chr' + str(lineList[0])
				previousChr2 = 'chr' + str(lineList[3])
			
			if np.size(chr1Subset) < 1 and np.size(chr2Subset) < 1:
				continue #no need to compute the distance, there are no genes on these chromosomes
			
			startTime = time.time()
			#Now compute how many TADs overlap
			#The start should be before the end of the tad, and the end after the start of the tad. This detects 4 scenarios of overlap (currently without using the overlap parameter). 
			startOverlapChr1 = int(lineList[1]) < chr1Subset[:,2] #I'm not sure if these indices are correct? 0 is chromosome right? 
			endOverlapChr1 = int(lineList[5]) > chr1Subset[:,1]
			
			#Now find where both of these are true (multiply because both conditions need to be true)
			overlappingSvsChr1 = startOverlapChr1 * endOverlapChr1
			
			#Overlap chr2 as well
			startOverlapChr2 = int(lineList[1]) < chr2Subset[:,2] #I'm not sure if these indices are correct? 0 is chromosome right? 
			endOverlapChr2 = int(lineList[5]) > chr2Subset[:,1]
			
			#Now find where both of these are true (multiply because both conditions need to be true)
			overlappingSvsChr2 = startOverlapChr2 * endOverlapChr2
			
			#Get the indices where both the start and end match the overlap criteria
			overlappingSvIndsChr1 = np.argwhere(overlappingSvsChr1 == True)
			overlappingCountChr1 = np.size(overlappingSvIndsChr1)
			overlappingSvIndsChr2 = np.argwhere(overlappingSvsChr2 == True)
			overlappingCountChr2 = np.size(overlappingSvIndsChr2)
			
			overlappingCount = overlappingCountChr1 + overlappingCountChr2
			
			overlappingTads.append(overlappingCount)
			
		
		return overlappingTads