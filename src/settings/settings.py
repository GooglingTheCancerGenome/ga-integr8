#Settings for the parsers

#The output files need to be specified
#The output folder location is relative to the main file! This may not be the ideal way of keeping the paths. 
outputFiles = dict(
	neo4jImportFolder = '../data/neo4jCsvImport/',
	regions = 'regions.csv', 
	annotations = 'annotations.csv',
	enhancers = 'enhancers.csv',
	tads = 'tads.csv',
	genes = 'genes.csv',
	hpo = 'hpo.csv',
	regionsAnnotations = 'regions_annotations_rel.csv',
	annotationsAnnotationTypes = 'annotations_annotationTypes_rel.csv',
	genesHpo = 'genes_hpo_rel.csv'
	
	
)

database = dict(
	
	database = 'neo4j' #type of database to use, idea is that it should be easy to switch between databases
)

#Connection information for Neo4J
neo4j = dict(
	
	httpPath = 'bolt://localhost:7687',
	user = 'neo4j',
	password = 'test'
	
)