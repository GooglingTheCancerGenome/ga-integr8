#Script in progress


#Parse the relevant information from MP_Genelist_HGNC_v2.txt to a csv format that can be loaded into Neo4J

#The regions and annotations will need to be appended to the existing annotation files

#Eventually it may be better to have a full pipeline that parses all data at once, not one by one


#Read input file

geneList = sys.argv[1] #gene list file


#Read file line by line
#Each entry will be a new region
#This region has an annotation, which is of type Gene
#The gene has the properties ensemblId, entrezId, pLi, RVIS, TSS, strand
#The gene links to HPO nodes, which have an ID and Name (make sure that these will be merged)

#celltype information is not available for these genes


def parseGeneList(geneList):
	
	regions = dict()
	regions['regionId:ID'] = [] #ID indicates to Neo4J that the property is to be used as node ID
	regions['start:int'] = [] #type int for querying
	regions['end:int'] = []
	regions['chromosome'] = []
	annotations = dict()
	annotations['annotationId:ID'] = []
	
	#List of information that we save for genes may not be complete, this is the information that we use for now to generate the heatmap
	genes = dict()
	genes['ensemblId:ID'] = []
	genes['entrezId'] = []
	genes['HGNCSymbol']
	genes['pLi:float'] = []
	genes['RVIS:float'] = []
	genes['TSS:int'] = []
	genes['strand'] = []
	
	hpoTerms = dict()
	hpoTerms['id:ID'] = []
	hpoTerms['phenotypeDescription'] = []
	
	#Defining the relations, start is the ID of the object and end is the ID of the subject
	regionsAnnotationsRelations = dict()
	regionsAnnotationsRelations[':START_ID'] = []
	regionsAnnotationsRelations[':END_ID'] = []
	
	#relations between annotations and their type (links annotations to genes)
	annotationsAnnotationTypeRelations = dict()
	annotationsAnnotationTypeRelations[':START_ID'] = [] #annotation ID
	annotationsAnnotationTypeRelations[':END_ID'] = [] #gene ID
	
	genesHpoTermsRelations = dict()
	genesHpoTermsRelations[':START_ID'] = [] #gene ID
	genesHpoTermsRelations['"END_ID'] = [] #HPO term ID
	
	#Read through the gene list and parse the information
	idCounter = 0
	
	
	with open(geneList, "r") as inFile:
		array = []
		for line in inFile:
			line = line.strip()
			splitLine = re.split("\t", line)
			
			hgncSymbol = splitLine[0]
			entrezId = splitLine[1]
			ensemblId = splitLine[2]
			chromosome = splitLine[4]
			start = splitLine[5]
			end = splitLine[6]
			TSS = splitLine[8]
			pLi = splitLine[9]
			RVIS = splitLine[10]
			HPOTerms = splitLine[12]
			HPOIds = splitLine[13]
			
			#Add the information to the dictionaries
			
			#Add the regions
			regionId = str(uuid.uuid4()) #unique IDs for nodes
			
			regions['regionsId:ID'].append(regionId)
			regions['start:int'].append(start)
			regions['end:int'].append(end)
			regions['chromosome'].append(chromosome)
			
			# 
			# splitFileName = re.split("\.", filename)
			# cellType = splitFileName[0]
			# 
			# annotationId = str(uuid.uuid4())
			# 
			# annotations['annotationId:ID'].append(annotationId)
			# annotations['cellType'].append(cellType)
			# 
			# regionsAnnotationsRelations[':START_ID'].append(regionId)
			# regionsAnnotationsRelations[':END_ID'].append(annotationId)
			# 
			# annotationsAnnotationTypeRelations[':START_ID'].append(annotationId)
			# annotationsAnnotationTypeRelations[':END_ID'].append(1)
			# 
			
	# 
	# writeToCsv(outputFolder + 'tads.csv', tad, False)			
	# writeToCsv(outputFolder + 'regions.csv', regions, False)
	# writeToCsv(outputFolder + 'annotations.csv', annotations, False)
	# writeToCsv(outputFolder + 'regions_annotations_rel.csv', regionsAnnotationsRelations, False)
	# writeToCsv(outputFolder + 'annotations_annotationTypes_rel.csv', annotationsAnnotationTypeRelations, False)

