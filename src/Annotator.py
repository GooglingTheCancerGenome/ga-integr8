#Class which will have the different functions for different queries.
#The final result will be the full annotation (TAD distance, enhancer overlap, gene distance, etc)

from databaseConnector import DatabaseConnector


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
	
	#A region is provided (maybe later this can be multiple regions), and the function goes through all the queries that we wish to make
	#Then, the queries are executed and all information is gathered and reported back. 
	def annotate(self, region): 
		#1. Query for individual features
		
		#We could put this in separate functions as well if we need to process the regions input, but for now, it is not necessary so we can directly ask the Neo4J class. 
		
		#Ask the Neo4J class to format the right query for us and to execute it
		nearestTadDistance = self.databaseConnector.database.computeNearestTadDistance(region)
		nearestEnhancerDistance = self.databaseConnector.database.computeNearestEnhancerDistance(region)
		
		print "Distance to nearest TAD: ", nearestTadDistance
		print "Distance to nearest enhancer: ", nearestEnhancerDistance
	
		#Query for number of overlapping TADs and enhancers
		
		
	
		#Query gene features
		
		#Querying for gene features is not at all efficient, it would be better to obtain all features for a gene at once, since this can be done in one query
		#I will later add something in the settings where we can enable/disable specific features, the script will read that and generate the query dynamically
		#and determine based on that which features we wish to query on. 
		
		#For the gene features, we first need the nearest gene. It may be better to first obtain the identifier, and then with that obtain newer features.
		#The distance queries are a bit dubious, if we get the identifier of the gene, we also get the distance to this gene.
		#I will do this at once for now, because it saves time
		[nearestGeneId, nearestGeneDistance] = self.databaseConnector.database.obtainNearestGeneIdAndDistance(region)
		
		print "nearest gene identifier: ", nearestGeneId
		print "nearest gene distance: ", nearestGeneDistance
		
		#Use the identifier to obtain other features (merge into one query? Does not help with easily turning off features)
		#Merging is faster, but if we then decide to not use the pLI or RVIS, it is more difficult to turn off these queries
		pLi = self.databaseConnector.database.obtainPliScore(nearestGeneId)
		RVIS = self.databaseConnector.database.obtainRvisScore(nearestGeneId)
		
		print pLi
		print RVIS
		
		
	#Add functions for other features