from typing import Dict
from classes import Query, SMWCategoryORProp, SMWImportOverview, \
    instantiate_smwimport_overview
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
        term = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 ontology_ns='aeon')
        term.create_wiki_item()
        if term.ontology_ns not in smw_import_dict.keys():
            smw_import_instance = instantiate_smwimport_overview(
                ontology_ns=term.ontology_ns, sematicterm=term)
            smw_import_dict[term.ontology_ns] = smw_import_instance
        if resource_type == 'property':
            smw_import_dict[term.ontology_ns].properties.append(
                (term.subject_name, str(term.item_dict.get('smw_datatype'))))
        elif resource_type == 'category':
            smw_import_dict[term.ontology_ns].properties.append(
                (term.subject_name, 'Category'))
            
        # TODO: create_smw_import to all instances in smw_import_dict
        # After queries are terminated,
        # smw_import_overview.create_smw_import()
        # smw_import_overview.write_wikipage()
        
        if args.write is True:
            term.write_wikipage()
        else:
            print(term.item_dict)
            print(term.wikipage_content)


    last_term = term
    return last_term


if __name__ == '__main__':
    smw_import_overview_dict = {}  # will store SMWImportOverview instances

    # # properties
    query2page(resource_type='property',
               sparql_fn='query_properties.rq',
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
