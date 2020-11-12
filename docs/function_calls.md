BEFORE REFACTORING
* def sparql2smwpage
    * (loop): 
        * def append_smw_import_content
            * instantiate_smwimport
                * def query_ontology  KEEP
    * def create_smw_import_pages
    
    
AFTER REFACTORING

* def sparql2smwpage
    * (loop): 
        * def query_ontology  KEEP
    * def create_smw_import_pages


