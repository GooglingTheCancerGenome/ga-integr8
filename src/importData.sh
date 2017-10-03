rm -rf ~/neo4j-3.3.2/packaging/standalone/target/neo4j-community-3.3.0-SNAPSHOT/data/databases/graph.db
sh ~/neo4j-3.3.2/packaging/standalone/target/neo4j-community-3.3.0-SNAPSHOT/bin/neo4j-import \
--into ~/neo4j-3.3.2/packaging/standalone/target/neo4j-community-3.3.0-SNAPSHOT/data/databases/graph.db \
--id-type string \
--nodes:Annotation ../data/neo4JCsvImport/annotations.csv \
--nodes:Region ../data/neo4JCsvImport/regions.csv \
--nodes:TAD ../data/neo4JCsvImport/tads.csv \
--nodes:Enhancer ../data/neo4JCsvImport/enhancers.csv \
--nodes:Gene ../data/neo4JCsvImport/genes.csv \
--nodes:HPO ../data/neo4JCsvImport/hpo.csv \
--relationships:has ../data/neo4JCsvImport/regions_annotations_rel.csv \
--relationships:type ../data/neo4JCsvImport/annotations_annotationTypes_rel.csv \
--relationships:has ../data/neo4JCsvImport/genes_hpo_rel.csv \
~/neo4j-3.3.2/packaging/standalone/target/neo4j-community-3.3.0-SNAPSHOT/bin/neo4j restart