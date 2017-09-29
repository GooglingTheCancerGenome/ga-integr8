
#Input to the script is a list of start and end positions
#For every one of these regions, we wish to obtain a set of features

#First, we obtain the raw annotation data
#From these annotations, we make a set of features
#Load modules
from neo4j.v1 import GraphDatabase, basic_auth
import sys
import re

#Import the session, if I do this in a function the session is not accessible anymore in the script
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "test"))
session = driver.session()




#We need functions for:
#- parsing the input
#- connecting to the database
#- building the queries for the database
#- actually querying the database
#- parsing the database results into features

#THis does not work!!! Session is lost if returned, could not connect to database error. 
def connectToNeo4J():
	
	driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "test"))
	session = driver.session()
	
	return session

def queryNeo4J(session, queries):
	
	results = dict()
	
	for query in queries:

		with session.begin_transaction() as tx:
			results[query] = list(tx.run(query))
			
	return results

#Obsolete
def obtainRegionsFromInput():
	
	#list of start positions and end positions
	
	#ideal is to make this a dictionary to have only 1 variable
	
	startPositions = sys.argv[1].split(",")
	endPositions = sys.argv[2].split(",")
	chromosomes = sys.argv[3].split(",")
	
	#startPositions = [int(x) for x in startPositions]
	#endPositions = [int(x) for x in endPositions]


	regions = dict()
	regions['start'] = startPositions
	regions['end'] = endPositions
	regions['chromosomes'] = chromosomes
	
	return regions

#Define a few queries
#Definitely not the best way, but mostly hardcoded for now to test if Neo4J returns the output that we wish to obtain
def generateQueries(regions):
	
	#match a region and also query the annotations that we wish to request
	matchRegion = 'match (region:Region)-[:has]->(annotation)-[:type]->(annotationType)'
	
	queries = []
	
	#The queries that we want to execute are:
	
	#1. What is the distance to the nearest TAD? (2 queries) - to start position and to end position, to all start and end positions in the database
	#2. What is the distance to the nearest enhancer? (again 2 queries)
	for region in range(0, len(regions['chromosomes'])):
		matchChromosome = 'region.chromosome = "' + regions['chromosomes'][region] + '"'
		matchEnhancer = '"Enhancer" in labels(annotationType)'
		matchTad = '"TAD" in labels(annotationType)'
		
		#Make this type of query if the two chromosomes are the same
		if regions['chromosomes'][region] == regions['chromosomes2'][region]:
			
			matchWithStart = 'with region, annotation, annotationType, abs(region.start - ' + regions['start'][region] + ') as difference order by difference asc'	
			matchWithEnd = 'with region, annotation, annotationType, abs(region.end - ' + regions['end'][region] + ') as difference order by difference asc'
			
			matchWithStartToEnd = 'with region, annotation, annotationType, abs(region.start - ' + regions['end'][region] + ') as difference order by difference asc'
			matchWithEndToStart = 'with region, annotation, annotationType, abs(region.end - ' + regions['start'][region] + ') as difference order by difference asc'	
			
			returnAnnotations = 'return difference limit 1'
		
			fullEnhancerQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchEnhancer + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullEnhancerQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchEnhancer + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
			fullEnhancerQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchEnhancer + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullEnhancerQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchEnhancer + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
			
			fullTadQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullTadQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
		
			fullTadQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullTadQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
		
			
		else: #Make 4 queries for translocations, include the correct chromosome match, the start and end positions are conceptually different than for the queries above
			
			matchChromosome2 = 'region.chromosome = "' + regions['chromosomes2'][region] + '"'
			
			matchWithStart = 'with region, annotation, annotationType, abs(region.start - ' + regions['start'][region] + ') as difference order by difference asc'	
			matchWithEnd = 'with region, annotation, annotationType, abs(region.end - ' + regions['end'][region] + ') as difference order by difference asc'
			
			matchWithStartToEnd = 'with region, annotation, annotationType, abs(region.start - ' + regions['end'][region] + ') as difference order by difference asc'
			matchWithEndToStart = 'with region, annotation, annotationType, abs(region.end - ' + regions['start'][region] + ') as difference order by difference asc'	
			
			returnAnnotations = 'return difference limit 1'
		
			fullEnhancerQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchEnhancer + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullEnhancerQueryEnd = matchRegion + ' where ' + matchChromosome2 + ' and ' + matchEnhancer + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
			fullEnhancerQueryStartToEnd = matchRegion + ' where ' + matchChromosome2 + ' and ' + matchEnhancer + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullEnhancerQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchEnhancer + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
			
			fullTadQueryStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithStart + ' ' + returnAnnotations + ';'
			fullTadQueryEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithEnd + ' ' + returnAnnotations + ';'
		
			fullTadQueryStartToEnd = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithStartToEnd + ' ' + returnAnnotations + ';'
			fullTadQueryEndToStart = matchRegion + ' where ' + matchChromosome + ' and ' + matchTad + ' ' + matchWithEndToStart + ' ' + returnAnnotations + ';'
			
		
		queries.append(fullEnhancerQueryStart)
		queries.append(fullEnhancerQueryEnd)
		queries.append(fullEnhancerQueryStartToEnd)
		queries.append(fullEnhancerQueryEndToStart)
		queries.append(fullTadQueryStart)
		queries.append(fullTadQueryEnd)
		queries.append(fullTadQueryStartToEnd)
		queries.append(fullTadQueryEndToStart)
	
	
	#3. What is the number of disrupted TADs in this region?
	#4. What is the number of disrupted enhancers in this region? 
	for region in range(0, len(regions['chromosomes'])):
		
		#Normal breakpoints
		if regions['chromosomes'][region] == regions['chromosomes2'][region]:
		
			matchChromosome = 'region.chromosome = "' + regions['chromosomes'][region] + '"'
			matchPositions = 'region.start <= ' + regions['end'][region] + ' and region.end >= ' + regions['start'][region]
			
			returnAnnotations = 'return region.chromosome, region.start, region.end, collect(distinct annotation.cellType), labels(annotationType) as type, count(labels(annotationType)) as count'
			
			fullQuery = matchRegion + ' where ' + matchChromosome + ' and ' + matchPositions + ' ' + returnAnnotations + ';'
		else: #Query for translocations
			
			matchChromosome1 = 'region.chromosome = "' + regions['chromosomes'][region] + '"'
			matchChromosome1Positions = 'region.start <= ' + regions['start'][region] + ' and region.end >= ' + regions['start'][region]
			matchChromosome2 = 'region.chromosome = "' + regions['chromosomes2'][region] + '"'
			matchChromosome2Positions = 'region.start <= ' + regions['end'][region] + ' and region.end >= ' + regions['end'][region]
			
			returnAnnotations = 'return region.chromosome, region.start, region.end, collect(distinct annotation.cellType), labels(annotationType) as type, count(labels(annotationType)) as count'
			
			fullQuery = matchRegion + ' where ' + matchChromosome1 + ' and ' + matchChromosome1Positions + ' or ' + matchChromosome2 + ' and ' + matchChromosome2Positions + ' ' + returnAnnotations + ';'
		
		queries.append(fullQuery)


	return queries


def annotate(regions): #for now support only one region, give it a region and the features will be returned. Should be fixed in the future to be more bulk-compatible
	
	features = dict()
	features['length'] = []
	#Add a feature for the length of SVs
	
	start = int(regions['start'][0])
	end = int(regions['end'][0])
	length = end-start #may not be the best variable
	#For negative ones, the end is likely before the start
	if start > end:
		length = start-end
	
	features['length'] = length
	features['start'] = start
	features['end'] = end
	
	#regions = obtainRegionsFromInput #for when using cmd input
	#handler = connectToNeo4J() #function does not work for whatever reason, the connection is then no longer accessible
	
	import time
	
	startTime = time.time()
	queries = generateQueries(regions)
	

	results = queryNeo4J(session, queries)
	endTime = time.time()
	print "time to query: ", endTime - startTime
	
	##########Test code: this will only work if the queries are the same as defined, all queries are indexed and need to be in the same place, which is not good! Fix this later if Neo4J is the way to go. 

	#parse the results and obtain the feature values. We need to do this per region!
	#print results
	#print queries
	
	
	nearestEnhancerDistanceFromStart = results[queries[0]][0][0]
	nearestEnhancerDistanceFromEnd = results[queries[1]][0][0]
	nearestEnhancerDistanceFromStartToEnd = results[queries[2]][0][0]
	nearestEnhancerDistanceFromEndToStart = results[queries[3]][0][0]
	
	nearestEnhancerDistance = min(nearestEnhancerDistanceFromStart, nearestEnhancerDistanceFromEnd, nearestEnhancerDistanceFromStartToEnd, nearestEnhancerDistanceFromEndToStart)
	
	print "Linear distance to nearest enhancer: ", nearestEnhancerDistance
	
	nearestTadDistanceFromStart = results[queries[4]][0][0]
	nearestTadDistanceFromEnd = results[queries[5]][0][0]
	nearestTadDistanceFromStartToEnd = results[queries[6]][0][0]
	nearestTadDistanceFromEndToStart = results[queries[7]][0][0]
	
	nearestTadDistance = min(nearestTadDistanceFromStart, nearestTadDistanceFromEnd, nearestTadDistanceFromStartToEnd, nearestTadDistanceFromEndToStart)
	
	print "Linear distance to nearest TAD: ", nearestTadDistance
	
	#Number of enhancers and TADs
	query = queries[8] #simple solution for now to select the right result set
	numberOfEnhancers = 0
	numberOfTads = 0
	for result in results[query]:
		if re.match("Enhancer", str(result["type"][0])):
			#numberOfEnhancers += int(result["count"])
			numberOfEnhancers += 1 #all regions are unique, so we can do + 1, the count now indicates the number of cell types as well
		if re.match("TAD", str(result["type"][0])):
			numberOfTads += 1
	
	print "Number of enhancers within region: ", numberOfEnhancers
	print "Number of TADS within region: ", numberOfTads
	
	
	features['Nearest enhancer distance'] = nearestEnhancerDistance
	features['Nearest TAD distance'] = nearestTadDistance
	features['Number of enhancers'] = numberOfEnhancers
	features['Number of TADs'] = numberOfTads
	

	
	return features
	
# #Distance to nearest TAD
# 
# regions = obtainRegionsFromInput()
# #handler = connectToNeo4J() #function does not work for whatever reason, the connection is then no longer accessible
# queries = generateQueries(regions)
# results = queryNeo4J(session, queries)
# 
# #parse the results and obtain the feature values. We need to do this per region!
# 
# nearestEnhancerDistanceFromStart = results[queries[0]][0]["difference"]
# nearestEnhancerDistanceFromEnd = results[queries[1]][0]["difference"]
# nearestEnhancerDistanceFromStartToEnd = results[queries[2]][0]["difference"]
# nearestEnhancerDistanceFromEndToStart = results[queries[3]][0]["difference"]
# 
# nearestEnhancerDistance = min(nearestEnhancerDistanceFromStart, nearestEnhancerDistanceFromEnd, nearestEnhancerDistanceFromStartToEnd, nearestEnhancerDistanceFromEndToStart)
# 
# print "Linear distance to nearest enhancer: ", nearestEnhancerDistance
# 
# nearestTadDistanceFromStart = results[queries[4]][0]["difference"]
# nearestTadDistanceFromEnd = results[queries[5]][0]["difference"]
# nearestTadDistanceFromStartToEnd = results[queries[6]][0]["difference"]
# nearestTadDistanceFromEndToStart = results[queries[7]][0]["difference"]
# 
# nearestTadDistance = min(nearestTadDistanceFromStart, nearestTadDistanceFromEnd, nearestTadDistanceFromStartToEnd, nearestTadDistanceFromEndToStart)
# 
# print "Linear distance to nearest TAD: ", nearestTadDistance
# 
# #Number of enhancers and TADs
# query = queries[8] #simple solution for now to select the right result set
# numberOfEnhancers = 0
# numberOfTads = 0
# for result in results[query]:
# 	if re.match("Enhancer", str(result["type"][0])):
# 		numberOfEnhancers = int(result["count"])
# 	if re.match("TAD", str(result["type"][0])):
# 		numberOfTads = int(result["count"])
# 
# print "Number of enhancers within region: ", numberOfEnhancers
# print "Number of TADS within region: ", numberOfTads
# 
# #Distance to nearest TAD
