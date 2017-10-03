 
**Setting up Neo4J:**

1.     Download Neo4J version 3.3.2: *https://github.com/neo4j/neo4j/tree/3.3*

2.     Follow installation instructions on GitHub page, use -DskipTests

3.     Move Neo4J if desired (Script *importData.sh* accesses Neo4J from *~/neo4j-3.3.2*, paths can be updated in scripts accordingly)

4.     Navigate to *neo4j-3.3.2/packaging/standalone/target/neo4j-community-3.3.0-SNAPSHOT/bin*

5.     Run *./neo4j start* to start the server

6.     In the browser, navigate to the link that is provided in the terminal

7.     Login with default username *neo4j* and default password *neo4j*

8.     Follow the interface instructions to set the password (the scripts connect with username *neo4j* and password *test*)


**Importing TADs, enhancers  and genes into Neo4J:**

1.     Run *python tadEnhancerDataToCsv.py* from the *src* directory to generate csv files in *data/neo4jCsvImport*

2. Run *python geneListToCsv.py ../data/Genes/MP_Genelist_HGNC_v2.txt* from the *src* directory to generate the additional gene-related csv files in *data/neo4jCsvImport*

3.     Run *./importData.sh* from the *src* directory (the paths may be different depending on the installation directory) to import the data into Neo4J

4.     You can run this query to check if all nodes and relationships are present regarding TADs and enhancers:
 

*match (region:Region)-[:has]->(annotation)-[:type]->(annotationType)*
*return region, annotation, collect(distinct annotationType) limit 20;*
 

This should show at least 1 TAD node, 1 enhancer node, annotation nodes and region nodes, where regions have annotations, and annotations either have the type TAD or Enhancer. Regions have a start, end and chromosome property. Annotations have a cellType property. 

5. You can run this query to check if all nodes and relationships are present:
 

*match (region:Region)-[:has]->(annotation)-[:type]->(annotationType)-[:has]->(hpo)*
*return region, annotation, hpo, collect(distinct annotationType) limit 20;*

This will return genes and associated HPO terms. There are still NA values in the gene data, because in CSV every column needs to be filled. This creates unnecessary property nodes, CSV is not the best format!

 
**Querying Neo4J for features for a true positive and true negative test set (may be broken since introduction of genes):**

1.     Run *python annotateFile.py ../data/TPTNTestSet/TP.txt ../data/TPTNTestSet/TP_annotations.txt* to annotate the true positives and write the features to TP_annotations.txt



**Data sources:**
 
TAD annotations - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5478386/, Table S3
Enhancers - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4449149/, Table S2
