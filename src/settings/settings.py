#Settings for the parsers

#The output files need to be specified
#The output folder location is relative to the main file! This may not be the ideal way of keeping the paths. 
outputFiles = dict(
	neo4jImportFolder = '../data/neo4jCsvImport',
	regions = 'regions.csv', 
	annotations = 'annotations.csv',
	enhancers = 'enhancers.csv',
	tads = 'tads.csv',
	genes = 'genes.csv',
	hpo = 'hpo.csv',
	regionsAnnotations = 'regions_annotations_rel.csv',
	annotationsAnnotationTypes = 'annotations_annotationTypes_rel.csv',
	genes_hpo = 'genes_hpo_rel.csv'
	
	
)