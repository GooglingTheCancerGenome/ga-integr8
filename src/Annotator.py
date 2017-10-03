#Class which will have the different functions for different queries.
#The final result will be the full annotation (TAD distance, enhancer overlap, gene distance, etc)

import DatabaseConnector


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
	
	def obtainDatabaseConnection():
		self.databaseConnector = DatabaseConnector() #this will automatically provide the right database connection for us depending on the settings
		
	
	#A region is provided (maybe later this can be multiple regions), and the function goes through all the queries that we wish to make
	#Then, the queries are executed and all information is gathered and reported back. 
	def annotate(region): 
		
		#1. Query for individual features
		
		#We could put this in separate functions as well if we need to process the regions input, but for now, it is not necessary so we can directly ask the Neo4J class. 
		
		#Ask the Neo4J class to format the right query for us and to execute it
		nearestTadDistance = self.databaseConnector.database.generateTadDistanceQuery(region)
	
	
		
		
		
	#Add functions for other features