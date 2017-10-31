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
import tarfile

#Separate class to do the overlap functionality.

#It would be great if all functionality to obtain annotations would each be in separate classes. These can then also be swapped out if needed. 
#Maybe it is good to also have some sort of interface to write against to make sure that all classes are always in the same format (with the same functions). 

class HiCFeatureHandler:
	
	#Annotate will accept all SVs that need to be annotated, and return the annotations for these SVs.
	#SVs format:
	#annotations format: a dictionary with annotations. {'featureName' : [values]}, where values is in the same order as the SVs. 
	
	#enabledFeatures is an optional parameter. A list can be provided that contains the names of features that are enabled in the settings. If necessary, certain features that have been disabled
	#do not need to be obtained from the file, or do not need to be computed to save computational time.
	def annotate(self, regions, enabledFeatures = None):
		
		#First, we read the Hi-C data from the flat files (for now this can be 1 test file on one chromosome)
		self.readInteractionMatrices()
		#We keep a matrix in memory with the interaction counts
		
		#Then for each SV, we can determine in which bin(s) it would fall.
		
		#All interactions with this bin are interupted.
		#How about interactions crossing this bin?

		annotations = 1+1

		return annotations
	
	def readInteractionMatrices(self):
		
		hiCArchive = settings.inputFiles['hiCArchive']
		hiCFile = settings.inputFiles['hiCFile']
		#Read this one file from the tar into a numpy-style matrix
		
		with tarfile.open(hiCArchive) as archive:
			for member in archive:
				if member.name == hiCFile: #we will use only this file for testing first
					print "Found file ", member.name
					#Convert this file into a numpy matrix
					
					#1. Read the file we are intersted in from the archive
					print "Reading the file: "
					f = archive.extractfile(member.name)
					
					#2. Open the file
					print "Obtaining the file content"
					print f.content
								
					
		
		
		
