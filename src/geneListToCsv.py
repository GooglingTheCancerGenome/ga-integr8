#Script in progress

import sys
import re
import uuid

sys.path.append('settings/') #Add settings path
import settings
from utilities import writeToCsv

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
	annotations['cellType'] = [] #We don't have this value for the genes, but because it is CSV, we need to fill in something. 
	
	#List of information that we save for genes may not be complete, this is the information that we use for now to generate the heatmap
	genes = dict()
	genes['ensemblId:ID'] = []
	genes['entrezId'] = []
	genes['HGNCSymbol'] = []
	genes['pLi'] = [] #Both pLi and RVIS are float, but these can be NA so we can only store it as string in the CSV import
	genes['RVIS'] = []
	genes['TSS:int'] = []
	genes['strand'] = []
	
	hpoTerms = dict()
	hpoTerms['id:ID'] = [] #we cannot parse the actual term due to bad comma separation in the input file, only use IDs for now
	
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
	genesHpoTermsRelations[':END_ID'] = [] #HPO term ID
	
	#Read through the gene list and parse the information
	idCounter = 0
	
	
	with open(geneList, "r") as inFile:
		array = []
		for line in inFile:
			
			if idCounter < 1:
				idCounter += 1
				continue
			line = line.strip()
			splitLine = re.split("\t", line)
			
			hgncSymbol = splitLine[0]
			entrezId = splitLine[1]
			ensemblId = splitLine[2]
			chromosome = 'chr' + splitLine[4] #add chr to be consistent with the rest of the database
			start = splitLine[5]
			end = splitLine[6]
			strand = splitLine[7]
			TSS = splitLine[9]
			pLi = splitLine[10]
			RVIS = splitLine[11]
			HPOTermsString = splitLine[13]
			HPOIdsString = splitLine[14]
			
			#Add the information to the dictionaries
			
			#Add the region
			regionId = str(uuid.uuid4()) #unique IDs for nodes
			
			regions['regionId:ID'].append(regionId)
			regions['start:int'].append(start)
			regions['end:int'].append(end)
			regions['chromosome'].append(chromosome)
			
			#Add the annotation
			annotationId = str(uuid.uuid4())
			annotations['annotationId:ID'].append(annotationId)
			annotations['cellType'].append('NA')
			
			#Add the gene
			genes['ensemblId:ID'].append(ensemblId)
			genes['entrezId'].append(entrezId)
			genes['HGNCSymbol'].append(hgncSymbol)
			
			#In the ideal case, we skip NA values so that a node does not need to be in the database. However, with the CSV import, this cannot work. There needs to be a value for every column at every row. 
			
			#if pLi != 'NA': #only add the node if the value is not NA. 
			genes['pLi'].append(pLi)
			#if RVIS != 'NA':
			genes['RVIS'].append(RVIS)
			genes['TSS:int'].append(TSS)
			genes['strand'].append(strand)
			
			#Add all HPO terms for this gene
			
			#Split the HPO terms
			HPOIds = re.split(",", HPOIdsString)
			
			#For every HPO term, we add a new node
			if HPOIds[0] != 'NA': #For the HPO terms, we can skip NA values, because these are not properties but new nodes that we do not need to link to if absent.
				for hpoTermNum in range(0, len(HPOIds)):
					#hpoTerms['term'].append(HPOTerms[hpoTermNum])
					if HPOIds[hpoTermNum] not in hpoTerms['id:ID']: #avoid duplicates
						hpoTerms['id:ID'].append(HPOIds[hpoTermNum])
					
					#Also add relationships between each HPO term and the gene that is associated to it
					genesHpoTermsRelations[':START_ID'].append(ensemblId)
					genesHpoTermsRelations[':END_ID'].append(HPOIds[hpoTermNum])
			
			#Add the relationships between regions and annotations	
			
			regionsAnnotationsRelations[':START_ID'].append(regionId)
			regionsAnnotationsRelations[':END_ID'].append(annotationId)
			
			#Add the relationships between annotations and genes
			annotationsAnnotationTypeRelations[':START_ID'].append(annotationId)
			annotationsAnnotationTypeRelations[':END_ID'].append(ensemblId)

	#Write the output to the CSV files
	outputFolder = settings.outputFiles['neo4jImportFolder']
	
	#Append the data to existing files (the TADs and enhancer files have already been created.)
	writeToCsv(outputFolder + settings.outputFiles['regions'], regions, True)
	writeToCsv(outputFolder + settings.outputFiles['annotations'], annotations, True)
	writeToCsv(outputFolder + settings.outputFiles['genes'], genes, False) #Append needs to be false here to make sure that the keys are written as header in new files
	writeToCsv(outputFolder + settings.outputFiles['hpo'], hpoTerms, False)
	
	writeToCsv(outputFolder + settings.outputFiles['regionsAnnotations'], regionsAnnotationsRelations, True)
	writeToCsv(outputFolder + settings.outputFiles['annotationsAnnotationTypes'], annotationsAnnotationTypeRelations, True)
	writeToCsv(outputFolder + settings.outputFiles['genesHpo'], genesHpoTermsRelations, False)

parseGeneList(geneList)