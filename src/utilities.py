#Script which can hold all functions that are used by multiple scripts.
import csv


#Give a dictionary, we use the keys as headers for the csv, and immediately dump this in a file.
def writeToCsv(file, information, append):
	
	if append is False:
	
		with open(file, "wb") as outfile:
			writer = csv.writer(outfile)
			writer.writerow(information.keys())
			writer.writerows(zip(*information.values()))
	else:
		with open(file, "a") as outfile: #here we use append for when we are adding the enhancer information. 
			writer = csv.writer(outfile)
			writer.writerows(zip(*information.values()))
			
			

#This function is here because the above one does somehow not work anymore, fix this later!
def writeToCsvManual(outFile, annotatedRegions):
	with open(outFile, "wb") as f:
		
		for annotationInd in range(0, len(annotatedRegions[annotatedRegions.keys()[0]])):
			
			line = annotatedRegions['chr1'][annotationInd] + '\t'
			line += annotatedRegions['s1'][annotationInd] + '\t'
			line += annotatedRegions['e1'][annotationInd] + '\t'
			line += annotatedRegions['chr2'][annotationInd] + '\t'
			line += annotatedRegions['s2'][annotationInd] + '\t'
			line += annotatedRegions['e2'][annotationInd] + '\t'
			
			line += str(annotatedRegions['nearestGeneDistance'][annotationInd]) + '\t'
			line += str(annotatedRegions['pLI'][annotationInd]) + '\t'
			line += str(annotatedRegions['RVIS'][annotationInd]) + '\t'
			#line += str(annotatedRegions['HPO'][annotationInd]) + '\t'
			line += str(annotatedRegions['overlappingTadCount'][annotationInd]) + '\t'
			
			f.write(line)
			f.write('\n')
			
			