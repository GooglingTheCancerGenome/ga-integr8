
#Interface for connecting to the database
#It should be easy to switch out the actual database for a new one if Neo4J is not sufficient for our purpose
import sys
sys.path.append('settings/') #Add settings path
import settings
from neo4J import Neo4J

class DatabaseConnector:
	
	database = None
	
	#Will do things including connecting to the database only once, accepting and executing queries
	
	def __init__(self):
		
		if settings.database['database'] == 'neo4j':
			self.database = Neo4J() #initialize connection to Neo4J
			
			