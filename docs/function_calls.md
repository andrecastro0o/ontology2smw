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




### SMWCategoryORProp vars
        self.ontology_ns = ontology_ns  https://github.com/tibonto/aeon#
        self.ontology_url = ontology_url  # https://github.com/tibonto/aeon#
        self.iri = iri   # https://github.com/tibonto/aeon

    USE only IRI


        self.ontology_ns_prefix = ontology_ns_prefix  # aeon
        self.categories = []
        self.properties = []
        self.ontology_name = None
        self.iri_seperator = None  # TODO: determine if is required
        
