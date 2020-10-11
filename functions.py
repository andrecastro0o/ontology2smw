import sys
from rdflib import Graph
from pathlib import Path
from rdflib.namespace import Namespace
from rdflib import exceptions

from classes import Query, SMWCategoryORProp, SMWImportOverview
from cli_args import parser
args = parser.parse_args()


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


def get_term_ns_prefix(term, prefixes):
    term_ns = Namespace(term)
    for prefix, namespace in prefixes.items():
        if namespace in term_ns:
            return namespace, prefix
    # TODO:  get/create the prefixes when they are not declared in the ontology
    print(f'Error: The ontology you are parsing has no declared prefix for '
          f'the term: {term}', file=sys.stderr)
    sys.exit()


def instantiate_smwimport(ontology_ns,
                          ontology_ns_prefix,
                          sematicterm):
    '''
    Creates and instance inf SMWImportOverview
    Which will create the content of Mediawiki:SMW_import_page
    '''
    instance = SMWImportOverview(ontology_ns=ontology_ns,
                                 ontology_ns_prefix=ontology_ns_prefix)
    # TODO: turn into method
    instance.wikipage_name = f'Mediawiki:Smw_import_' \
                             f'{sematicterm.namespace_prefix}'
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


def query2page(sparql_fn: str, format_: str, source: str):
    smw_import_dict = {}  # will store SMWImportOverview instances
    query = Query(sparql_fn=sparql_fn,
                  format_=format_,
                  source=source)
    # loop through each ontology term resulting from SPARQL query
    for printout in query.return_printout():
        ns, ns_prefix = get_term_ns_prefix(term=printout.subject,
                                           prefixes=query.prefixes)
        term = SMWCategoryORProp(item_=printout,
                                 namespace=ns,
                                 namespace_prefix=ns_prefix)
        term.create_wiki_item()
        if args.write is True:
            term.write_wikipage()
        else:
            print(term.wikipage_content)
            # print(term.item_dict)

        # CREATE Mediawiki:Smw_import_ content
        if term.namespace_prefix not in smw_import_dict.keys():
            smw_import_dict[term.namespace_prefix] = instantiate_smwimport(
                    ontology_ns=term.namespace,
                    ontology_ns_prefix=term.namespace_prefix,
                    sematicterm=term)

        smw_import_dict[term.namespace_prefix].properties.append(
                (term.subject_name, term.resource_type))

    # CREATE Mediawiki:Smw_import_ PAGES
    print("\n*** Mediawiki: Smw_import_ PAGES ***\n")
    for prefix, importoverview in smw_import_dict.items():
        print(f'\n{prefix}')
        # pprint(importoverview.__dict__)
        importoverview.create_smw_import()

        if args.write is True:
            importoverview.write_wikipage()  # ATTENTION: will write to wiki
        else:
            print(importoverview.wikipage_content)
