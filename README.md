 
Setting up Neo4J:
1.     Download Neo4J version 3.3: https://github.com/neo4j/neo4j/tree/3.3
2.     Follow installation instructions on GitHub page, use -DskipTests
3.     Move Neo4J if desired (Script importData.sh accesses Neo4J from ~/Documents/neo4j-3.3, paths can be updated in scripts accordingly)
4.     Navigate to neo4j-3.3/packaging/standalone/target/neo4j-community-3.3.0-SNAPSHOT/bin
5.     Run ./neo4j start to start the server
6.     In the browser, navigate to the link that is provided in the terminal
7.     Login with default username neo4j and default password neo4j
8.     Follow the interface instructions to set the password (the scripts connect with username neo4j and password test)
 
Importing TADs and enhancers into Neo4J:
1.     Run python tadEnhancerDataToCsv.py from the src directory to generate csv files in data/neo4jCsvImport
2.     Run ./importData.sh from the src directory (the paths may be different depending on the installation directory) to import the data into Neo4J
3.     You can run this query to check if all nodes and relationships are present:
 
match (region:Region)-[:has]->(annotation)-[:type]->(annotationType)
return region, annotation, collect(distinct annotationType) limit 20;
 
This should show at least 1 TAD node, 1 enhancer node, annotation nodes and region nodes, where regions have annotations, and annotations either have the type TAD or Enhancer. Regions have a start, end and chromosome property. Annotations have a cellType property. 
 
 
Querying Neo4J for features for a true positive and true negative test set:
1.     Run python annotateFile.py ../data/TPTNTestSet/TP.txt ../data/TPTNTestSet/TP_annotations.txt to annotate the true positives and write the features to TP_annotations.txt


Data sources:
 
TAD annotations - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5478386/, Table S3
Enhancers - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4449149/, Table S2
