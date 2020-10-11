from classes import Query, SMWCategoryORProp, SMWImportOverview, \
    instantiate_smwimport_overview, get_term_ns_prefix
from cli_args import parser
from pprint import pprint
from log import logger
args = parser.parse_args()


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
            # print(term.item_dict)
            print(term.wikipage_content)

        # CREATE Mediawiki:Smw_import_ content
        if term.namespace_prefix not in smw_import_dict.keys():
            smw_import_dict[term.namespace_prefix] = \
                instantiate_smwimport_overview(
                    ontology_ns=term.namespace,
                    ontology_ns_prefix=term.namespace_prefix,
                    sematicterm=term)

        smw_import_dict[term.namespace_prefix].properties.append(
                (term.subject_name, term.resource_type))

    # CREATE Mediawiki:Smw_import_ PAGES
    print(f"\n*** Mediawiki: Smw_import_ PAGES ***\n")
    for prefix, importoverview in smw_import_dict.items():
        print(f'\n{prefix}')
        # pprint(importoverview.__dict__)
        importoverview.create_smw_import()

        if args.write is True:
            importoverview.write_wikipage()  # ATTENTION: will write to wiki
        else:
            print(importoverview.wikipage_content)


if __name__ == '__main__':
    query2page(sparql_fn='query_class_prop.rq',
               format_='ttl',
               source='aeon/aeon.ttl',
               )
