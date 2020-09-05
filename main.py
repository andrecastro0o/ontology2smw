import rdflib, os, sys
from rdflib.namespace import OWL, RDF, RDFS
from urllib.parse import urldefrag
from pathlib import Path
from typing import Dict
from pprint import pprint
from cli_args import parser

args = parser.parse_args()


class Query:
    graph = rdflib.Graph()

    def __init__(self, resource_type: str, sparql_fn: str, source: str, 
                 format_: str):
        self.resource_type = resource_type
        self.sparql_fn = sparql_fn
        self.format = format_
        self.source = source
        self.graph.parse(source='aeon/aeon.ttl', format=self.format)

    def query_graph(self):
        query_path = Path.cwd() / 'queries' / self.sparql_fn
        print(f'\n\n*** {query_path} ***\n')
        with open(query_path, 'r') as query_fobj:
            sparq_query = query_fobj.read()
        self.printouts = self.graph.query(sparq_query,
                                        initNs={'rdf': RDF, 'rdfs': RDFS, 'owl': OWL})

    def return_printout(self):
        self.query_graph()
        for printout in self.printouts:
            yield printout


class SPARQLitem:
    def __init__(self, resource_type: str, item: Dict, ontology_ns: str):
        self.resource_type = resource_type
        self.item = item
        self.item_dict = item.asdict()
        self.subject = self.item_dict['subject']
        self.iri = self.subject.defrag()
        self.pagename = None
        pprint(self.item_dict)

    def create_wiki_item(self):
        self.pagename = urldefrag(url=self.item_dict['subject'])

        '''
        * Imported from [[Imported from::foaf:Organization]]
        * Equivalent URI [[Equivalent URI::http://xmlns.com/foaf/0.1/Organization]]

       smw_import_info
        [[Category:Imported vocabulary]]
        [[Category:aeon]]
        '''

        if self.resource_type.lower() == 'class':
            print('class')

    # def createsmwpage(self, printout: Dict):
    #     printout
        

if __name__ == '__main__':
    query = Query(resource_type='class',
                  sparql_fn='query_classes.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    for printout in query.return_printout():
        item = SPARQLitem(resource_type='class',
                          item=printout,
                          ontology_ns='aeon')
        item.create_wiki_item()


# subject = last_property['subject']
# iri_base = str(subject.defrag())
