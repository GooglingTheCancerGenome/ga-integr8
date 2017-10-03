#Class for connecting and querying Neo4J specifically

sys.path.append('settings/') #Add settings path
import settings

import Region

class Neo4J:
	
	handle = None #handle for interacting with the database
	
	def __init__():
		self.initiateConnection()
	
	#Initiates connection to the Neo4J database at the path provided in the settings file. Username and password are also there
	def initiateConnection():
		GraphDatabase.driver(settings.neo4j['httpPath'], auth=basic_auth(settings.neo4j['user'], settings.neo4j['password']))
		self.handle = driver.session()
	
	#Executes the given query and returns the results. 
	def executeQuery(query):
		
		with self.handle.begin_transaction() as tx:
			results = list(tx.run(query))
			
		return results
		
	#May need an additional function for bulk querying
	
	
	#This class knows how to format our queries to cypher format.
	#There are probably better and more general ways to set up specific types of query (like with the other driver), but it is restricting in what we can do and also time-consuming.
	#I will be generating the queries 'manually' here for now.
	
	def computeNearestTadDistance(region):
		tadDistanceQuery = self.generateTadDistanceQuery(region)
		
	#Generate the queries
	def generateTadDistanceQueries(region):
		
		matchTad = '"TAD" in labels(annotationType)' #specific part for TADs
		tadDistanceQuery = self.generateGeneralDistanceQuery(region, matchTad)
		return tadDistanceQuery
		
	def generateEnhancerDistanceQueries():
		
		1+1
		
	def generateTadOverlapQuery():
		
		1+1
		
	def generateEnhancerOverlapQuery():
		
		1+1
		
	#there will be large overlap in the above queries apart from the TAD/enhancer part, keep this in a simple function that can provide these queries with a few variables that may be different. 
	def generateGeneralDistanceQuery(region, matchType):
		
		queries = []
		
		matchChromosome = 'region.chromosome = "' + regions['chromosomes'][region] + '"'
		matchEnhancer = '"Enhancer" in labels(annotationType)'
		
		
		#Make this type of query if the two chromosomes are the same
		if regions['chromosomes'][region] == regions['chromosomes2'][region]:
			
			matchWithStart = 'with region, annotation, annotationType, abs(region.start - ' + regions['start'][region] + ') as difference order by difference asc'	
			matchWithEnd = 'with region, annotation, annotationType, abs(region.end - ' + regions['end'][region] + ') as difference order by difference asc'
			
			matchWithStartToEnd = 'with region, annotation, annotationType, abs(region.start - ' + regions['end'][region] + ') as difference order by difference asc'
			matchWithEndToStart = 'with region, annotation, annotationType, abs(region.end - ' + regions['start'][region] + ') as difference order by difference asc'	
			
			returnAnnotations = 'return difference limit 1'
			
			fullTadQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullTadQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
		
			fullTadQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullTadQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
		
			
		else: #Make 4 queries for translocations, include the correct chromosome match, the start and end positions are conceptually different than for the queries above
			
			matchChromosome2 = 'region.chromosome = "' + regions['chromosomes2'][region] + '"'
			
			matchWithStart = 'with region, annotation, annotationType, abs(region.start - ' + regions['start'][region] + ') as difference order by difference asc'	
			matchWithEnd = 'with region, annotation, annotationType, abs(region.end - ' + regions['end'][region] + ') as difference order by difference asc'
			
			matchWithStartToEnd = 'with region, annotation, annotationType, abs(region.start - ' + regions['end'][region] + ') as difference order by difference asc'
			matchWithEndToStart = 'with region, annotation, annotationType, abs(region.end - ' + regions['start'][region] + ') as difference order by difference asc'	
			
			returnAnnotations = 'return difference limit 1'
			
			fullTadQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullTadQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
		
			fullTadQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullTadQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchType + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
			
		
		queries.append(fullEnhancerQueryStart)
		queries.append(fullEnhancerQueryEnd)
		queries.append(fullEnhancerQueryStartToEnd)
		queries.append(fullEnhancerQueryEndToStart)
		
		return queries
		
		
	def generateGeneralOverlapQuery():
		
		1+1
	
	
	