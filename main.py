from typing import Dict
from classes import Query, SMWCategoryORProp, SMWImportOverview
from cli_args import parser
from log import logger
args = parser.parse_args()


def query2page(resource_type: str, sparql_fn: str, format_: str,
               source:str) -> Dict:
    query = Query(resource_type=resource_type,
                  sparql_fn=sparql_fn,
                  format_=format_,
                  source=source)

    for printout in query.return_printout():
        item = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 ontology_ns='aeon')
        if item.item_dict.get('smw_datatype') not in [None, '']:
            item.create_wiki_item()
            smw_import_overview.properties.append(
                (item.subject_name, str(item.item_dict['smw_datatype'])))
            print(item.item_dict)
            print(item.wikipage_content)
            if args.write is True:
                logger.debug(msg=f'Wrote {item.wikipage_name} to wiki')
                item.write_wikipage()
        else:
            logger.warning(
                msg=f'{item.wikipage_name} MISSING aeon:SMW_datatype val. '
                    f'Not imported to wiki')
    last_item = item
    return last_item


if __name__ == '__main__':

    smw_import_overview = SMWImportOverview(ontology_ns='aeon')
    # # properties
    query2page(resource_type='property',
               sparql_fn='query_properties.rq',
               format_='ttl',
               source='aeon/aeon.ttl')

    lastclass = query2page(resource_type='category',
                           sparql_fn='query_classes.rq',
                           format_='ttl',
                           source='aeon/aeon.ttl')

    smw_import_overview.wikipage_name = \
        f'Mediawiki:Smw_import_{lastclass.ontology_ns}'
    smw_import_overview.ontology_name = 'Academic Event Ontology (AEON)'
    smw_import_overview.iri = lastclass.iri+'#'
    smw_import_overview.ontology_url = 'http://ontology.tib.eu/aeon/'
    smw_import_overview.create_smw_import()
    smw_import_overview.write_wikipage()


# subject = last_property['subject']
# iri_base = str(subject.defrag())
