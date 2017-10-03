#Class for connecting and querying Neo4J specifically

sys.path.append('settings/') #Add settings path
import settings

class Neo4J:
	
	handle = None #handle for interacting with the database
	
	def __init__():
		self.initiateConnection()
	
	#Initiates connection to the Neo4J database at the path provided in the settings file. Username and password are also there
	def initiateConnection():
		GraphDatabase.driver(settings.neo4j['httpPath'], auth=basic_auth(settings.neo4j['user'], settings.neo4j['password']))
		self.handle = driver.session()
	
	#Executes the given query and returns the results. 
	def executeQuery(query):
		
		with self.handle.begin_transaction() as tx:
			results = list(tx.run(query))
			
		return results
		
	#May need an additional function for bulk querying
	