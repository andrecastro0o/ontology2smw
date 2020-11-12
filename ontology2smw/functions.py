import sys
from ontology2smw.classes import QueryOntology, \
    SMWCategoryORProp, \
    SMWImportOverview
from ontology2smw.cli_args import parser
args = parser.parse_args()


# def copied from Query Class (should reuse that one)
def query_graph(sparql_fn, graph):
    print(f'\n\n*** {sparql_fn} ***\n')
    with open(sparql_fn, 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    return printouts


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
    query = QueryOntology(sparql_fn=sparql_fn, format_=format_, source=source)
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
            smw_import_dict[term.namespace_prefix] = SMWImportOverview(
                ontology_ns=term.namespace,
                ontology_ns_prefix=term.namespace_prefix,
                iri=term.iri,
                ontology_url=term.namespace)
        smw_import_dict[term.namespace_prefix].properties.append(
            (term.subject_name, term.resource_type))

        # print(term.item_dict)
    create_smw_import_pages(importdict=smw_import_dict)
