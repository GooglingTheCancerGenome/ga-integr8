#Class for connecting and querying Neo4J specifically

import sys
sys.path.append('settings/') #Add settings path
import settings
from neo4j.v1 import GraphDatabase, basic_auth

import Region

class Neo4J:
	
	#handle = None #handle for interacting with the database
	handle = None
	
	def __init__(self):
		self.initiateConnection()
	
	#Initiates connection to the Neo4J database at the path provided in the settings file. Username and password are also there
	####! This does not work from a function, if it is set, and later the handle is accessed, the connection has been closed. Not very neat. 
	def initiateConnection(self):
		driver = GraphDatabase.driver(settings.neo4j['httpPath'], auth=basic_auth(settings.neo4j['user'], settings.neo4j['password']))
		self.handle = driver.session()
	
	#Executes the given query and returns the results. 
	def executeQuery(self, query):
		######! I need to put the connection code here for some reason, otherwise the connection is closed according to Neo4J. Why?
		driver = GraphDatabase.driver(settings.neo4j['httpPath'], auth=basic_auth(settings.neo4j['user'], settings.neo4j['password']))
		self.handle = driver.session()
		######
		
		with self.handle.begin_transaction() as tx:
			results = list(tx.run(query))
			
		return results
		
	#May need an additional function for bulk querying
	
	
	#This class knows how to format our queries to cypher format.
	#There are probably better and more general ways to set up specific types of query (like with the other driver), but it is restricting in what we can do and also time-consuming.
	#I will be generating the queries 'manually' here for now.
	
	#Compute the nearest tad distance feature
	def computeNearestTadDistance(self, region):
		#Generate the queries
		tadDistanceQueries = self.generateTadDistanceQueries(region)
		#Execute the queries
		results = dict()
		for query in tadDistanceQueries:
			results[query] = self.executeQuery(query)
			
		#Process the results and obtain the nearest TAD distance
		nearestTadDistance = self.computeGeneralDistanceToAnnotation(results)
		
		return nearestTadDistance
		
	#Generate the queries
	def generateTadDistanceQueries(self, region):
		
		matchTad = '"TAD" in labels(annotationType)' #specific part for TADs
		tadDistanceQueries = self.generateGeneralDistanceQueries(region, matchTad)
		return tadDistanceQueries
	
	#Still lots of overlap with the nearest TAD distance function, but ok for now
	def computeNearestEnhancerDistance(self, region):
		#Generate the queries
		enhancerDistanceQueries = self.generateEnhancerDistanceQueries(region)
		#Execute the queries
		results = dict()
		for query in enhancerDistanceQueries:
			results[query] = self.executeQuery(query)
			
		#Process the results and obtain the nearest TAD distance
		nearestEnhancerDistance = self.computeGeneralDistanceToAnnotation(results)
		
		return nearestEnhancerDistance
		
		
	def generateEnhancerDistanceQueries(self, region):
		matchEnhancer = '"Enhancer" in labels(annotationType)' #specific part for TADs
		enhancerDistanceQueries = self.generateGeneralDistanceQueries(region, matchEnhancer)
		return enhancerDistanceQueries
		
	def generateTadOverlapQuery():
		
		1+1
		
	def generateEnhancerOverlapQuery():
		
		1+1
		
	def obtainNearestGeneIdAndDistance(self, region):
		
		geneDistanceQueries = self.generateGeneDistanceQueries(region)
		#Execute the queries
		results = dict()
		for query in geneDistanceQueries:
			results[query] = self.executeQuery(query)
			
		#Process the results and obtain the nearest TAD distance
		nearestGeneDistance = self.computeGeneralDistanceToAnnotation(results)
		nearestGeneId = self.getNearestGeneId(results)
		
		return [nearestGeneId, nearestGeneDistance]
	
	#Again quite duplicate, maybe fix this later
	def generateGeneDistanceQueries(self, region):
		matchGene = '"Gene" in labels(annotationType)' #specific part for TADs
		geneDistanceQueries = self.generateGeneralDistanceQueries(region, matchGene)
		return geneDistanceQueries
	
	def obtainPliScore(self, nearestGeneId):
		
		
	#Provide the query output from the nearest distance to enhancer or tad, and compute the actual distance regardless of annotation type. 
	def computeGeneralDistanceToAnnotation(self, results):
		
		queries = results.keys()
		
		nearestDistanceFromStart = results[queries[0]][0]["difference"]
		nearestDistanceFromEnd = results[queries[1]][0]["difference"]
		nearestDistanceFromStartToEnd = results[queries[2]][0]["difference"]
		nearestDistanceFromEndToStart = results[queries[3]][0]["difference"]
		
		nearestDistance = min(nearestDistanceFromStart, nearestDistanceFromEnd, nearestDistanceFromStartToEnd, nearestDistanceFromEndToStart)
		
		return nearestDistance
	
	def getNearestGeneId(self, results):
		queries = results.keys()
		
		#The way to obtain the values is a bit weird, previously using "difference" as key worked, but not anymore
		nearestGeneId = results[queries[0]][0]["id"]
		
		return nearestGeneId
	
	#there will be large overlap in the above queries apart from the TAD/enhancer part, keep this in a simple function that can provide these queries with a few variables that may be different. 
	def generateGeneralDistanceQueries(self, region, matchType):
		
		matchRegion = 'match (region:Region)-[:has]->(annotation)-[:type]->(annotationType)'
		queries = []
		
		matchChromosome = 'region.chromosome = "' + region['chromosome'] + '"'
		matchEnhancer = '"Enhancer" in labels(annotationType)'
		
		returnAnnotations = 'return difference, ID(annotationType) as id limit 1' #Also return the ID so that we can use this query for genes as well and obtain the nearest gene
		
		#Make this type of query if the two chromosomes are the same
		if region['chromosome'] == region['chromosome2']:
			
			matchWithStart = 'with region, annotation, annotationType, abs(region.start - ' + region['start'] + ') as difference order by difference asc'	
			matchWithEnd = 'with region, annotation, annotationType, abs(region.end - ' + region['end'] + ') as difference order by difference asc'
			
			matchWithStartToEnd = 'with region, annotation, annotationType, abs(region.start - ' + region['end'] + ') as difference order by difference asc'
			matchWithEndToStart = 'with region, annotation, annotationType, abs(region.end - ' + region['start'] + ') as difference order by difference asc'	
			
			fullQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
		
			fullQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
		
			
		else: #Make 4 queries for translocations, include the correct chromosome match, the start and end positions are conceptually different than for the queries above
			
			matchChromosome2 = 'region.chromosome = "' + region['chromosome2'] + '"'
			
			matchWithStart = 'with region, annotation, annotationType, abs(region.start - ' + region['start'] + ') as difference order by difference asc'	
			matchWithEnd = 'with region, annotation, annotationType, abs(region.end - ' + region['end'] + ') as difference order by difference asc'
			
			matchWithStartToEnd = 'with region, annotation, annotationType, abs(region.start - ' + region['end'] + ') as difference order by difference asc'
			matchWithEndToStart = 'with region, annotation, annotationType, abs(region.end - ' + region['start'] + ') as difference order by difference asc'	
			
			fullQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
		
			fullQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
			
		
		queries.append(fullQueryStart)
		queries.append(fullQueryEnd)
		queries.append(fullQueryStartToEnd)
		queries.append(fullQueryEndToStart)
		
		return queries
		
		
	def generateGeneralOverlapQuery():
		
		1+1
	
	
	