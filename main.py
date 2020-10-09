from typing import Dict
from classes import Query, SMWCategoryORProp, SMWImportOverview, \
    instantiate_smwimport_overview, get_term_ns_prefix
from cli_args import parser
from log import logger
args = parser.parse_args()


def query2page(resource_type: str, sparql_fn: str, format_: str,
               source:str, smw_import_dict: dict) -> Dict:
    query = Query(resource_type=resource_type,
                  sparql_fn=sparql_fn,
                  format_=format_,
                  source=source)

    for printout in query.return_printout():
        ns, ns_prefix = get_term_ns_prefix(term=printout.subject,
                                           prefixes=query.prefixes)
        print('NS:', ns, ns_prefix)
        term = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 ontology_ns=ns,
                                 ontology_ns_prefix=ns_prefix)
        term.create_wiki_item()

        print(term.ontology_ns_prefix)
        if term.ontology_ns_prefix not in smw_import_dict.keys():
            smw_import_dict[term.ontology_ns_prefix] = instantiate_smwimport_overview(
                ontology_ns=term.ontology_ns,
                ontology_ns_prefix=term.ontology_ns_prefix,
                sematicterm=term)

        if resource_type == 'property':
            smw_import_dict[term.ontology_ns_prefix].properties.append(
                (term.subject_name, str(term.item_dict.get('smw_datatype'))))
        elif resource_type == 'category':
            smw_import_dict[term.ontology_ns_prefix].properties.append(
                (term.subject_name, 'Category'))

        # TODO: create_smw_import to all instances in smw_import_dict
        # After queries are terminated,
        # smw_import_overview.create_smw_import()
        # smw_import_overview.write_wikipage()
        #
        # if args.write is True:
        #     term.write_wikipage()
        # else:
        #     print(term.item_dict)
        #     print(term.wikipage_content)

    print(smw_import_dict)
    last_term = term   # TODO: remove
    return last_term    # TODO: remove


if __name__ == '__main__':
    smw_import_overview_dict = {}  # will store SMWImportOverview instances

    # # properties
    query2page(resource_type='property',
               sparql_fn='query_class_prop.rq',
               format_='ttl',
               source='aeon/aeon.ttl',
               smw_import_dict=smw_import_overview_dict,
               )

    # lastclass = query2page(resource_type='category',
    #                        sparql_fn='query_classes.rq',
    #                        format_='ttl',
    #                        source='aeon/aeon.ttl')
    #



# subject = last_property['subject']
# iri_base = str(subject.defrag())
