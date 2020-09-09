import rdflib
from rdflib.namespace import OWL, RDF, RDFS
from pathlib import Path
from typing import Dict
from pprint import pprint
from jinja_utils import render_template
from datetime import datetime
from mediawikitools.wiki import actions as mwactions
from jinja_utils import url_termination


class SMWontology:
    def __init__(self):
        self.wikipage_name = None
        self.wikipage_content = None

    def write_wikipage(self):  # TODO: do not repeate this function declaration
        now = datetime.now()
        now = now.isoformat()
        mwactions.edit(page=self.wikipage_name,
                       content=self.wikipage_content,
                       summary=f'Edited by Bot at {now}',
                       append=False,
                       newpageonly=False)


class Query:
    graph = rdflib.Graph()

    def __init__(self, resource_type: str, sparql_fn: str, source: str,
                 format_: str):
        self.resource_type = resource_type
        self.sparql_fn = sparql_fn
        self.format = format_
        self.source = source
        self.graph.parse(source='aeon/aeon.ttl', format=self.format)
        self.printouts = None

    def query_graph(self):
        query_path = Path.cwd() / 'queries' / self.sparql_fn
        print(f'\n\n*** {query_path} ***\n')
        with open(query_path, 'r') as query_fobj:
            sparq_query = query_fobj.read()
        self.printouts = self.graph.query(sparq_query,
                                          initNs={'rdf': RDF, 'rdfs': RDFS,
                                                  'owl': OWL})

    def return_printout(self):
        self.query_graph()
        for printout_ in self.printouts:
            yield printout_


class SMWCategoryORProp(SMWontology):
    def __init__(self, resource_type: str, item_: Dict, ontology_ns: str):
        self.resource_type = resource_type
        self.ontology_ns = ontology_ns
        self.item = item_
        self.item_dict = item_.asdict()
        self.subject = self.item_dict['subject']
        self.subject_name = None
        self.iri = self.subject.defrag()

        # pprint(self.item_dict)

    def create_wiki_item(self):
        self.subject_name = url_termination(self.item_dict['subject'])
        self.wikipage_name = f'{self.resource_type.capitalize()}:' \
                             f'{self.subject_name}'
        if self.resource_type.lower() == 'category':
            template_file = 'mw_category.j2'
        elif self.resource_type.lower() == 'property':
            template_file = 'mw_property.j2'
        self.wikipage_content = render_template(
            template=template_file,
            ns=self.ontology_ns,
            item=self.item_dict,
            item_name=self.subject_name,
            page_info=None
        )


class SMWImportOverview(SMWontology):
    def __init__(self, ontology_ns: str):
        self.ontology_ns = ontology_ns
        self.categories = []
        self.properties = []
        self.ontology_name = None
        self.iri = None
        self.iri_seperator = None
        self.ontology_url = None

    def create_smw_import(self):
        all_resources = self.categories + self.properties
        page_info_dict = {'ontology_iri': self.iri,
                          'ontology_iri_seperator': self.iri_seperator,
                          'ontology_url': self.ontology_url,
                          'ontology_ns': self.ontology_ns,
                          'ontology_name': self.ontology_name,
                          }
        self.wikipage_content = render_template(template='mw_smw_import.j2',
                                                ns=self.ontology_ns,
                                                item=all_resources,
                                                item_name=None,
                                                page_info=page_info_dict)




'''
MediaWiki:Smw_import_foaf

http://xmlns.com/foaf/0.1/|[http://www.foaf-project.org/ Friend Of A Friend]
 Organization|Category
 Person|Category
 Project|Category
 name|Type:Text
 homepage|Type:URL
 mbox|Type:Email
 mbox_sha1sum|Type:Text
 depiction|Type:URL
 phone|Type:Text
 knows|Type:Page
 member|Type:Page
 maker|Type:Page
 made|Type:Page 

[[Category:Imported vocabulary]]
'''


if __name__ == '__main__':

    # properties
    query = Query(resource_type='property',
                  sparql_fn='query_properties.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    for printout in query.return_printout():
        item = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 ontology_ns='aeon')
        if item.item_dict.get('smw_datatype'):  # TODO add smw_datatype check
            # item.create_wiki_item()
            print(item.item_dict)
            print(item.wikipage_content)
        # else:
        #     print(f'{item.subject} MISSING aeon:SMW_import_info value')
            # TODO print -> log


    # query = Query(resource_type='category',
    #               sparql_fn='query_classes.rq',
    #               format_='ttl',
    #               source='aeon/aeon.ttl')
    # for printout in query.return_printout():
    #     item = SPARQLitem(resource_type=query.resource_type,
    #                       item_=printout,
    #                       ontology_ns='aeon')
    #     if item.item_dict.get('smw_import_info'):
    #         item.create_wiki_item()
    #         print(item.wikipage_content)
    #     else:
    #         print(f'{item.subject} MISSING aeon:SMW_import_info value')
    #         # TODO print -> log
