import sys
from rdflib import Graph
from rdflib.namespace import OWL, RDF, RDFS, Namespace, NamespaceManager
from rdflib import exceptions
from pathlib import Path
from typing import Dict
from pprint import pprint
from jinja_utils import render_template
from datetime import datetime
from mediawikitools.wiki import actions as mwactions
from jinja_utils import url_termination
from log import logger

class SMWontology:
    def __init__(self):
        self.wikipage_name = None
        self.wikipage_content = None

    def write_wikipage(self):  # TODO: do not repeate this function declaration
        now = datetime.now()
        now = now.isoformat()
        logger.debug(
            msg=f'Attempting to write {self.wikipage_name} to wiki')
        edit_response = mwactions.edit(page=self.wikipage_name,
                                       content=self.wikipage_content,
                                       summary=f'Edited by Bot at {now}',
                                       append=False,
                                       newpageonly=False)
        if edit_response:
            logger.debug(
                msg=f'Wrote {self.wikipage_name} to wiki')
        else:
            logger.warning(
                msg=f'Failed to write {self.wikipage_name} to wiki')


class Query:
    graph = Graph()
    # namespace_manager = NamespaceManager(Graph())
    # graph.namespace_manager = namespace_manager
    # all_ns = [n for n in graph.namespace_manager.namespaces()]
    def __init__(self, resource_type: str, sparql_fn: str, source: str,
                 format_: str):
        self.resource_type = resource_type
        self.sparql_fn = sparql_fn
        self.format = format_
        self.source = source
        self.graph.parse(source='aeon/aeon.ttl', format=self.format)
        self.printouts = None
        self.get_graph_prefixes()

    def get_graph_prefixes(self):
        namespace_manager = NamespaceManager(self.graph)
        all_prefixes = {n[0]: n[1] for n in namespace_manager.namespaces()}
        all_prefixes.pop('')  # remove '' key
        self.prefixes = all_prefixes

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
    def __init__(self, resource_type: str, item_: Dict, namespace: str,
                 namespace_prefix: str):
        self.resource_type = resource_type
        self.namespace_prefix = namespace_prefix
        self.namespace = namespace
        self.item = item_
        self.item_dict = item_.asdict()
        self.subject = self.item_dict['subject']
        self.subject_name = None
        self.iri = self.subject.defrag()

        # pprint(self.item_dict)
        # how to get the namespace of a property?


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
            ns_prefix=self.namespace_prefix,
            item=self.item_dict,
            item_name=self.subject_name,
            page_info=None
        )


class SMWImportOverview(SMWontology):
    def __init__(self, ontology_ns: str, ontology_ns_prefix: str):
        self.ontology_ns = ontology_ns
        self.ontology_ns_prefix = ontology_ns_prefix
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
                          'ontology_ns_prefix': self.ontology_ns_prefix,
                          'ontology_name': self.ontology_name,
                          }
        self.wikipage_content = render_template(template='mw_smw_import.j2',
                                                ns_prefix=self.ontology_ns_prefix,
                                                item=all_resources,
                                                item_name=None,
                                            page_info=page_info_dict)


# def copied from Query Class (should reuse that one)
def query_graph(sparql_fn, graph):
    query_path = Path.cwd() / 'queries' / sparql_fn
    print(f'\n\n*** {query_path} ***\n')
    with open(query_path, 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    return printouts


def query_ontology_schema(ontology_ns):
    print(f'Query ontology schema: {ontology_ns}')
    title, version, description = None, None, None  # default
    try:
        graph = Graph()
        graph.parse(location=ontology_ns,
                    format="application/rdf+xml")
        printouts = query_graph(sparql_fn='query_ontology_schema.rq',
                                graph=graph)
        if len(printouts) > 0:
            printout_dict = (list(printouts)[0]).asdict()
            title, version, description = printout_dict.get('title'), \
                                          printout_dict.get('version'),\
                                          printout_dict.get('description')

    except (exceptions.ParserError, TypeError) as pe:
        msg = f"{ontology_ns} failed to resolve to an RDF. Provide " \
              f"infomartion about the ontology in ontologies.yml"
        # TODO: Create the structure of ontologies.yml. Read it and store info
        # fill: title, version, description
        # TODO: Ask user if she want to continue
        print('Error: ',pe, '\n', msg)
    return title, version, description


def instantiate_smwimport_overview(ontology_ns,
                                   ontology_ns_prefix,
                                   sematicterm):
    instance = SMWImportOverview(ontology_ns=ontology_ns,
                                 ontology_ns_prefix=ontology_ns_prefix)
    # TODO: turn into method
    instance.wikipage_name = f'Mediawiki:Smw_import_{sematicterm.namespace_prefix}'
    title, version, description = query_ontology_schema(ontology_ns=ontology_ns)
    # TODO: get from ontology
    instance.ontology_name = title
    instance.iri = sematicterm.iri  # TODO: determin if can be removed
    # TODO: get from ontology
    instance.ontology_url = ontology_ns
    return instance


def get_term_ns_prefix(term, prefixes):
    term_ns = Namespace(term)
    for prefix, namespace in prefixes.items():
        if namespace in term_ns:
            return namespace, prefix
    # TODO:  get/create the prefixes when they are not declared in the ontology
    print(f'Error: The ontology you are parsing has no declared prefix for the '
          f'term: {term}', file=sys.stderr)
    sys.exit()


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
    query.get_graph_prefixes()
    print('PREFIXES:', query.prefixes)
    for printout in query.return_printout():
        # print(printout)
        subject = printout.subject
        subject_ns = Namespace(subject)
        for prefix, namespace in query.prefixes.items():
            if namespace in subject_ns:
                subject_prefix = prefix
                break
        print('subject:', subject, 'prefix:', prefix)

        item = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 namespace=prefix)
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
