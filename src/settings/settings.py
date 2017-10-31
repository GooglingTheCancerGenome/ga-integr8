#Settings for the annotation scripts

#Maybe it is a good idea to split the parser settings from the annotation scripts. 

#The output files need to be specified for the parsers
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
	
	database = 'flatFile' #type of database to use, idea is that it should be easy to switch between databases
)

#Connection information for Neo4J
neo4j = dict(
	
	httpPath = 'bolt://localhost:7687',
	user = 'neo4j',
	password = 'test'
	
)

#determine which features to enable. The idea is that features can be turned off if necessary without having to modify the code. 
features = dict(
	nearestTadDistance = True,
	nearestEnhancerDistance = True,
	numberOfOverlappingTads = True,
	numberOfOverlappingEnhancers = True,
	svLength = True,
	pLi = True,
	RVIS = True,
	nearestGeneDistance = True
)


#Locations of the input files
inputFiles = dict(
	geneList = '../data/Genes/MP_Genelist_HGNC_v2.txt',
	tads = '../data/tads/tads.csv',
	hiCArchive = '../../../../../Downloads/GSE87112_file/all_data_contact_maps.tgz', #keep in different location for now, file is too big for github. Somehow using ~ does also not work, we need the full relative path
	hiCFile = 'contact_maps/HiCNorm/primary_cohort/BL.nor.chr1.mat' #the first test file that we will use for Hi-C data
)

parameters = dict(
	geneDistance = 200000 #we look at genes within 2Mb of the SV
)