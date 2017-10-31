#Testing of the Annotator script

import sys
import numpy as np

from annotator import Annotator


#Example region that has all features
annotator = Annotator()
# region = dict()
# region['chromosome'] = 'chr1'
# region['chromosome2'] = 'chr1'
# region['start'] = '3541566'
# region['end'] = '3541586'
# 
# annotator.annotate(region)



#This piece of code reads the regions from the true positive file
#it will need its own place in the code, for now keep it here quick and dirty

#Load the pancancer file
pancancerFile = sys.argv[1]

pancancerData = []
with open(pancancerFile, "r") as f:
	lineCount = 0
	for line in f:
		if lineCount < 2:
			lineCount += 1
			continue
		line = line.strip()
		splitLine = line.split("\t")
		#Convert the start and end positions to int here so that we do not need to do this in the loop, it slows down the code
		splitLine[1] = int(splitLine[1])
		splitLine[2] = int(splitLine[2])
		splitLine[5] = int(splitLine[5])
		splitLine[6] = int(splitLine[6])
		
		#chr 1, start, end, chr2, start2, end2
		pancancerData.append([splitLine[0], splitLine[1], splitLine[2], splitLine[4], splitLine[5], splitLine[6]])

#Convert the pancancerData to numpy format (probably even faster if we do this right away)
pancancerData = np.array(pancancerData)

# 
#Obtain the columns that we wish to sort by
chr1col = pancancerData[:,0]
chr2col = pancancerData[:,3]

sortedInd = np.lexsort((chr2col, chr1col)) #sort first by column 1, then by column 2. This works, but it is lexographical, so chromosome 11 comes before chromosome 2. For this purpose it is ok, since we only look for this
											#chromosome in other files to subset these, so the order in which we do that does not really matter. 

sortedPancancerData = pancancerData[sortedInd]
pancancerData = sortedPancancerData

annotator.annotate(pancancerData)