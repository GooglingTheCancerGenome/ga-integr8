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
			
			

			
			