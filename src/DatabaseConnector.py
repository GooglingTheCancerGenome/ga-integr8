
#Interface for connecting to the database
#It should be easy to switch out the actual database for a new one if Neo4J is not sufficient for our purpose
import sys
sys.path.append('settings/') #Add settings path
import settings
from neo4J import Neo4J
from flatFileDb import FlatFileDB

class DatabaseConnector:
	
	database = None
	
	#Will do things including connecting to the database only once, accepting and executing queries
	
	#We either have to make sure that the functions all have the same names so that we can easily call it from the annotator,
	#or from here a link between the function names should be defined. For now I will stick with the first. 
	
	def __init__(self):
		
		if settings.database['database'] == 'neo4j':
			self.database = Neo4J() #initialize connection to Neo4J
			
		if settings.database['database'] == 'flatFile':
			self.database = FlatFileDB()