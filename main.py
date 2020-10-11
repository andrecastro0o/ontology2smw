from typing import Dict
from classes import Query, SMWCategoryORProp, SMWImportOverview, \
    instantiate_smwimport_overview, get_term_ns_prefix
from cli_args import parser
from pprint import pprint
from log import logger
args = parser.parse_args()

# TODO: REMOVE resource_type and use the rdf:type or ?smw_datatype to
#  determine when needed
def query2page(resource_type: str, sparql_fn: str, format_: str,
               source: str, smw_import_dict: dict) -> Dict:
    query = Query(resource_type=resource_type,
                  sparql_fn=sparql_fn,
                  format_=format_,
                  source=source)

    for printout in query.return_printout():
        ns, ns_prefix = get_term_ns_prefix(term=printout.subject,
                                           prefixes=query.prefixes)
        term = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
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

        if resource_type == 'property':
            smw_import_dict[term.namespace_prefix].properties.append(
                (term.subject_name, str(term.item_dict.get('smw_datatype'))))
        elif resource_type == 'category':
            smw_import_dict[term.namespace_prefix].properties.append(
                (term.subject_name, 'Category'))

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
    smw_import_overview_dict = {}  # will store SMWImportOverview instances
    query2page(resource_type='property',
               sparql_fn='query_class_prop.rq',
               format_='ttl',
               source='aeon/aeon.ttl',
               smw_import_dict=smw_import_overview_dict,
               )