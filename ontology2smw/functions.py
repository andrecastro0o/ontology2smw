import sys
from rdflib import Graph
from rdflib import exceptions

from ontology2smw.classes import Query, SMWCategoryORProp, SMWImportOverview
from ontology2smw.cli_args import parser
args = parser.parse_args()


# def copied from Query Class (should reuse that one)
def query_graph(sparql_fn, graph):
    print(f'\n\n*** {sparql_fn} ***\n')
    with open(sparql_fn, 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    return printouts


def query_ontology_schema(ontology_ns):
    print(f'Query ontology schema: {ontology_ns}')
    title, version, description = None, None, None  # default
    try:   # TODO: try logic moved to Query.query_graph with error handling
        graph = Graph()
        graph.parse(location=ontology_ns,
                    format="application/rdf+xml")

        printouts = query_graph(
            sparql_fn='ontology2smw/queries/query_ontology_schema.rq',
            graph=graph)
        if len(printouts) > 0:
            printout_dict = (list(printouts)[0]).asdict()
            title = printout_dict.get('title')
            version = printout_dict.get('version')
            description = printout_dict.get('description')

    except (exceptions.ParserError, TypeError) as pe:
        msg = f"{ontology_ns} failed to resolve to an RDF. Provide " \
              f"infomartion about the ontology in ontologies.yml"
        # TODO: Create the structure of ontologies.yml. Read it and store info
        # fill: title, version, description
        # TODO: Ask user if she want to continue
        print('Error: ', pe, '\n', msg)
    return title, version, description


def get_term_ns_prefix(term_uri, allprefixes):
    """
    Based on term_uri and prefixes determine namespace and prefix of term
    """
    for prefix, namespace in allprefixes.items():
        if namespace in term_uri:
            return namespace, prefix
    # TODO:  get/create the prefixes when they are not declared in the ontology
    print(f'Error: The ontology you are parsing has no declared prefix for '
          f'the term: {term_uri}', file=sys.stderr)
    sys.exit()


def instantiate_smwimport(ontology_ns,
                          ontology_ns_prefix,
                          sematicterm):
    '''
    Creates and instance inf SMWImportOverview
    Which will create the content of Mediawiki:SMW_import_page
    '''
    # TODO: REFACTOR: remove class and turn variable assigments into
    #  Class methods
    instance = SMWImportOverview(ontology_ns=ontology_ns,
                                 ontology_ns_prefix=ontology_ns_prefix)
    # instance.wikipage_name = f'Mediawiki:Smw_import_' \
    #                          f'{sematicterm.namespace_prefix}'
    title, version, description = query_ontology_schema(
        ontology_ns=ontology_ns)
    if title:
        instance.ontology_name = title
    else:
        instance.ontology_name = ontology_ns_prefix
    # TODO: add version and descrippipt to instance, if they exist
    instance.iri = sematicterm.iri  # TODO: determine if can be removed
    instance.ontology_url = ontology_ns
    return instance



def create_smw_import_pages(importdict):
    """
    Creates Mediawiki:smw_import_ONTO page
        For each of the ontologies in importdict (SMWCategoryORProp
        instance)
    """
    print("\n*** Mediawiki: Smw_import_ PAGES ***\n")
    for prefix, importoverview in importdict.items():
        print(f'\n{prefix}')
        # pprint(importoverview.__dict__)
        importoverview.create_smw_import()
        if args.write is True:
            importoverview.write_wikipage()  # ATTENTION: will write to wiki
        else:
            print(importoverview.wikipage_content)


def sparql2smwpage(sparql_fn: str, format_: str, source: str):
    """
    Performs the calls necessary to turn SPARQL query to SMW pages required
    to import the ontology
    """
    smw_import_dict = {}  # will store SMWImportOverview instances
    query = Query(sparql_fn=sparql_fn, format_=format_, source=source)
    query.get_graph_prefixes()
    for printout in query.return_printout():
        # loop through each ontology schema term, resulting from SPARQL query
        ns, ns_prefix = get_term_ns_prefix(term_uri=printout.subject,
                                           allprefixes=query.prefixes)
        term = SMWCategoryORProp(item_=printout,
                                 namespace=ns,
                                 namespace_prefix=ns_prefix)
        term.create_wiki_item()
        print(f'\n----------------------------------\n{term.wikipage_name}')
        if args.write is True:
            term.write_wikipage()
        else:
            print(term.wikipage_content)

        if term.namespace_prefix not in smw_import_dict.keys():
            # TODO: REFACTOR remove def instantiate_smwimport turn actions into
            #  class methods
            smw_import_dict[term.namespace_prefix] = instantiate_smwimport(
                ontology_ns=term.namespace,
                ontology_ns_prefix=term.namespace_prefix,
                sematicterm=term)
        smw_import_dict[term.namespace_prefix].properties.append(
            (term.subject_name, term.resource_type))

        # print(term.item_dict)
    create_smw_import_pages(importdict=smw_import_dict)
