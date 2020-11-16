import json
import sys
from rdflib import Graph
from rdflib.namespace import NamespaceManager
from typing import Dict
# from pprint import pprint
from datetime import datetime
from rdflib import exceptions
from ontology2smw.jinja_utils import url_termination, render_template
from ontology2smw.log import logger
from ontology2smw.mediawikitools import actions as mwactions
from ontology2smw.file_utils import relative_read_f

xsd2smwdatatype = {
    'xsd:string': 'Text',
    'rdfs:Literal': 'Text',
    'xsd:Name': 'Text',
    'xsd:normalizedString': 'Text',
    'xsd:decimal': 'Number',
    'xsd:float': 'Number',
    'xsd:integer': 'Number',
    'xsd:nonNegativeInteger': 'Number',
    'xsd:positiveInteger': 'Number',
    'xsd:nonPositiveInteger': 'Number',
    'xsd:negativeInteger': 'Number',
    'xsd:int': 'Number',
    'xsd:double': 'Number',
    'xsd:long': 'Number',
    'xsd:short': 'Number',
    'xsd:unsignedLong': 'Number',
    'xsd:byte': 'Number',
    'xsd:boolean': 'Boolean',
    'xsd:dateTime': 'Date',
    'xsd:time': 'Text',
    'xsd:date': 'Date',
    'xsd:gYearMonth': 'Date',
    'xsd:gYear': 'Date',
    'xsd:gMonthDay': 'Text',
    'xsd:gDay': 'Text',
    'xsd:gMonth': 'Text',
    'xsd:anyURI': 'URL',
    'xsd:language': 'Text'
}


class MWpage:
    """
    Parent Class represents MW page:
    """
    def __init__(self):
        self.wikipage_name = None
        self.wikipage_content = None

    def write_wikipage(self):
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


class QueryOntology:
    """
    SPARQL query to Ontology Schema
    """
    def __init__(self, sparql_fn: str, source: str,
                 format_: str):
        self.sparql_fn = sparql_fn
        self.format = format_  # TODO: rm format and infer from source=*.ext
        self.source = source
        self.graph = Graph()
        self.bind_namespaces()
        self.graph.parse(source=self.source, format=self.format)
        self.printouts = None
        self.prefixes = None
        self.query = None  # TMP

    def bind_namespaces(self):
        all_ns_dict = relative_read_f('queries/all_ns_prefixes.json',
                                      format_='json')
        for prefix, ns in all_ns_dict.items():
            self.graph.bind(prefix, ns)

    def get_graph_prefixes(self):
        namespace_manager = NamespaceManager(self.graph)
        all_prefixes = {n[0]: n[1] for n in namespace_manager.namespaces()}
        # all_prefixes.pop('')  # remove '' key
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
    def __init__(self, item_: Dict, query_):
        self.item = item_
        self.item_dict = item_.asdict()
        self.namespace_prefix, self.namespace = self.get_term_ns_prefix(query_)
        self.resource_type = self.determine_smw_catORprop()
        self.subject = self.item_dict['term']
        self.subject_name = None
        # pprint(self.item_dict)

    def get_term_ns_prefix(self, query):
        """
        Based on term_uri and prefixes determine namespace and prefix of term
        """
        for prefix, namespace in query.prefixes.items():
            if namespace in self.item_dict['term']:
                return namespace, prefix
        # TODO:  get/create the prefixes when they are not declared in the
        #  ontology
        print(f'Error: The ontology you are parsing has no declared prefix for '
              f'the term: {self.item_dict["term"]}', file=sys.stderr)
        sys.exit()


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

    def determine_smw_catORprop(self):
        if 'smw_datatype' in self.item_dict.keys():
            if str(self.item_dict['smw_datatype']) == 'Category':
                return 'Category'
            else:
                return 'Property'
        else:
            termtype = url_termination(self.item_dict.get('termType')
                                       ).capitalize()
            if termtype == 'Class':
                return 'Category'
            else:
                return 'Property'


class SMWImportOverview(MWpage):
    """
    Class represents the Ontology overview SMW page: Mediawiki:smw_import_XYZ
    """
    def __init__(self, ontology_ns: str, ontology_ns_prefix: str):
        self.ontology_ns = ontology_ns
        self.ontology_ns_prefix = ontology_ns_prefix
        self.categories = []
        self.properties = []
        self.ontology_name = None
        self.wikipage_name = f'Mediawiki:Smw_import_{self.ontology_ns_prefix}'
        self.title, self.version, self.description = self.query_ontology()

    def create_smw_import(self):
        all_resources = self.categories + self.properties
        page_info_dict = {'ontology_ns': self.ontology_ns,
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

    def query_ontology(self):
        # print(f'Query ontology schema: {self.ontology_ns}')
        title, version, description = None, None, None  # default
        try:
            graph = Graph()
            graph.parse(location=self.ontology_ns,
                        format="application/rdf+xml")
            sparql_query = relative_read_f('queries/query_ontology_schema.rq')
            print(sparql_query)
            printouts = graph.query(sparql_query)
            if len(printouts) > 0:
                printout_dict = (list(printouts)[0]).asdict()
                title = printout_dict.get('title')
                version = printout_dict.get('version')
                description = printout_dict.get('description')
        except (exceptions.ParserError, TypeError) as pe:
            msg = f"{self.ontology_ns} failed to resolve to an RDF. Provide " \
                  f"infomartion about the ontology in ontologies.yml"
            print('Error: ', pe, '\n', msg)
        if not title:
            title = self.ontology_ns_prefix
        return title, version, description
