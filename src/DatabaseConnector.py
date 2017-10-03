
#Interface for connecting to the database
#It should be easy to switch out the actual database for a new one if Neo4J is not sufficient for our purpose

sys.path.append('settings/') #Add settings path
import settings

class DatabaseConnector:
	
	database = None
	
	#Will do things including connecting to the database only once, accepting and executing queries
	
	def __init__():
		
		if settings.database == 'neo4j':
			self.database = Neo4J() #initialize connection to Neo4J
			
			