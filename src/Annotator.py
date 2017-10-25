#Class which will have the different functions for different queries.
#The final result will be the full annotation (TAD distance, enhancer overlap, gene distance, etc)

from databaseConnector import DatabaseConnector
from utilities import writeToCsv

import time

class Annotator:
	
	databaseConnector = None
	
	#Functions to define:
	#- obtaining a database connection
	#- all the different queries
	#- combining the query results
	
	
	#What is difficult is the conversion of query style between databases. What is the best place to make this conversion?
	#I think this class, annotator, knows which queries it wants to make, or at least which features to obtain. It can gather the right data to build a query
	#The database connector serves as mid-point for providing us with the right database connector variable.
	#Then, Neo4J, knows how to execute queries, but it also knows how to format the queries to cypher format. 
	
	def __init__(self):
		self.obtainDatabaseConnection()
	
	def obtainDatabaseConnection(self):
		self.databaseConnector = DatabaseConnector() #this will automatically provide the right database connection for us depending on the settings
	
	#I have changed the setup a little bit, now we should be able to provide multiple SVs at once (or simply call these regions to be uniform)
	#The features are dynamically obtained depending on which have been enabled in the settings. 
	def annotate(self, regions):
		
		startTime = time.time()
		#1. Query for individual features
		
		nearestGeneFeatures = self.databaseConnector.database.computeNearestGeneFeatures(regions)
		tadFeatures = self.databaseConnector.database.computeTADFeatures(regions)
		# 
		# #2. Collect features and write these to an output annotation file
		allAnnotations = dict(nearestGeneFeatures.items() + tadFeatures.items())
		self.writeAnnotationsToFile(regions, allAnnotations)
		# 
		# 
		endTime = time.time()
		print "finished annotating ", len(regions), " in ", endTime - startTime, " seconds"
		#We could put this in separate functions as well if we need to process the regions input, but for now, it is not necessary so we can directly ask the Neo4J class. 
		
		#Ask the Neo4J class to format the right query for us and to execute it
		# nearestTadDistance = self.databaseConnector.database.computeNearestTadDistance(region)
		# nearestEnhancerDistance = self.databaseConnector.database.computeNearestEnhancerDistance(region)
		# 
		# print "Distance to nearest TAD: ", nearestTadDistance
		# print "Distance to nearest enhancer: ", nearestEnhancerDistance
	
		#Query for number of overlapping TADs and enhancers
		
		
	
		#Query gene features
		
		#Querying for gene features is not at all efficient, it would be better to obtain all features for a gene at once, since this can be done in one query
		#I will later add something in the settings where we can enable/disable specific features, the script will read that and generate the query dynamically
		#and determine based on that which features we wish to query on. 
		
		#For the gene features, we first need the nearest gene. It may be better to first obtain the identifier, and then with that obtain newer features.
		#The distance queries are a bit dubious, if we get the identifier of the gene, we also get the distance to this gene.
		#I will do this at once for now, because it saves time
		# [nearestGeneId, nearestGeneDistance] = self.databaseConnector.database.obtainNearestGeneIdAndDistance(region)
		# 
		# print "nearest gene identifier: ", nearestGeneId
		# print "nearest gene distance: ", nearestGeneDistance
		# 
		# #Use the identifier to obtain other features (merge into one query? Does not help with easily turning off features)
		# #Merging is faster, but if we then decide to not use the pLI or RVIS, it is more difficult to turn off these queries
		# pLi = self.databaseConnector.database.obtainPliScore(nearestGeneId)
		# RVIS = self.databaseConnector.database.obtainRvisScore(nearestGeneId)
		# 
		# print pLi
		# print RVIS
		
		
		####! new setup for querying gene features
		
		#The gene name should be returned for sure, but if no gene features are enabled, we do not need to make any query
		
	#Write the annotations to a file, such that each SV still has a chromosome, start, end, and behind that columns with the annotations that we are interested in. 
	def writeAnnotationsToFile(self, regions, annotations):

		regionsDict = dict()
		regionsDict['chr1'] = regions[:,0]
		regionsDict['s1'] = regions[:,1]
		regionsDict['e1'] = regions[:,2]
		regionsDict['chr2'] = regions[:,3]
		regionsDict['s2'] = regions[:,4]
		regionsDict['e2'] = regions[:,5]
		
		#merge the regions and annotations
		annotatedRegions = dict(regionsDict.items() + annotations.items())

		#write the merged dictionary to csv, the order of the annotations and regions should column-wise be the same. 
		writeToCsv('test.csv', annotatedRegions, False)	
		
		
		1+1
		