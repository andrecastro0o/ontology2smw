from rdflib import Graph
from rdflib.namespace import NamespaceManager
from typing import Dict
# from pprint import pprint
from datetime import datetime
from ontology2smw.jinja_utils import url_termination, render_template
from ontology2smw.log import logger
from ontology2smw.mediawikitools import actions as mwactions


class MWpage:
    """
    Parent Class represents MW page:
    """

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
    """
    SPARQL query to Ontology Schema
    """
    def __init__(self, sparql_fn: str, source: str,
                 format_: str):
        self.sparql_fn = sparql_fn
        self.format = format_  # TODO: rm format and infer from source=*.ext
        self.source = source
        self.graph = Graph()
        self.graph.parse(source=self.source, format=self.format)
        self.printouts = None
        self.prefixes = None
        self.query = None  # TMP

    def get_graph_prefixes(self):
        namespace_manager = NamespaceManager(self.graph)
        all_prefixes = {n[0]: n[1] for n in namespace_manager.namespaces()}
        all_prefixes.pop('')  # remove '' key
        self.prefixes = all_prefixes

    def query_graph(self):
        print(f'\n\n*** {self.sparql_fn} ***\n')
        with open(self.sparql_fn, 'r') as query_fobj:
            self.query = query_fobj.read()  # TMP
            sparq_query = self.query  # query_fobj.read()
        self.printouts = self.graph.query(sparq_query)
        # TODO: handle errors

    def return_printout(self):
        self.query_graph()
        for printout_ in self.printouts:
            yield printout_


class SMWCategoryORProp(MWpage):
    """
    Class represents a SMW Category or Property
    """
    def __init__(self, item_: Dict, namespace: str,
                 namespace_prefix: str):
        self.namespace_prefix = namespace_prefix
        self.namespace = namespace
        self.item = item_
        self.item_dict = item_.asdict()
        self.resource_type = self.determine_smw_datatype()
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
        else:
            template_file = 'mw_property.j2'

        label = self.item_dict.get('label')
        if label and label.language:
            label_lang = label.language
        else:
            label_lang = 'en'
        self.wikipage_content = render_template(
            template=template_file,
            ns_prefix=self.namespace_prefix,
            item=self.item_dict,
            item_name=self.subject_name,
            page_info=None,
            term_description=label,
            term_description_lang=label_lang
        )

    def determine_smw_datatype(self):
        if str(self.item_dict['smw_datatype']) == 'Category':
            return 'Category'
        else:
            return 'Property'


class SMWImportOverview(MWpage):
    """
    Class represents the Ontology overview SMW page: Mediawiki:smw_import_XYZ
    """
    def __init__(self, ontology_ns: str, ontology_ns_prefix: str):
        self.ontology_ns = ontology_ns  # TODO: change to uri
        self.ontology_ns_prefix = ontology_ns_prefix  # TODO: change prefix
        self.categories = []
        self.properties = []
        self.ontology_name = None
        self.iri = None  # TODO: determine if is required
        self.iri_seperator = None  # TODO: determine if is required
        self.ontology_url = None  # TODO: determine if is required

    def create_smw_import(self):
        all_resources = self.categories + self.properties
        page_info_dict = {'ontology_iri': self.iri,
                          'ontology_iri_seperator': self.iri_seperator,
                          'ontology_url': self.ontology_url,
                          'ontology_ns': self.ontology_ns,
                          'ontology_ns_prefix': self.ontology_ns_prefix,
                          'ontology_name': self.ontology_name,
                          }
        self.wikipage_content = render_template(
            template='mw_smw_import.j2',
            ns_prefix=self.ontology_ns_prefix,
            item=all_resources,
            item_name=None,
            page_info=page_info_dict,
            # term_description=''
        )

# if __name__ == '__main__':
#
#     # properties
#     query = Query(resource_type='property',
#                   sparql_fn='query_properties.rq',
#                   format_='ttl',
#                   source='aeon/aeon.ttl')
#     query.get_graph_prefixes()
#     print('PREFIXES:', query.prefixes)
#     for printout in query.return_printout():
#         # print(printout)
#         subject = printout.subject
#         subject_ns = Namespace(subject)
#         for prefix, namespace in query.prefixes.items():
#             if namespace in subject_ns:
#                 subject_prefix = prefix
#                 break
#         print('subject:', subject, 'prefix:', prefix)
#
#         item = SMWCategoryORProp(resource_type=query.resource_type,
#                                  item_=printout,
#                                  namespace=prefix)
#         if item.item_dict.get('smw_datatype'):  # TODO add smw_datatype check
#             # item.create_wiki_item()
#             print(item.item_dict)
#             print(item.wikipage_content)
#         # else:
#         #     print(f'{item.subject} MISSING aeon:SMW_import_info value')
#             # TODO print -> log
