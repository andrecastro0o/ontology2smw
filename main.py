from classes import Query, SMWCategoryORProp, SMWImportOverview
from cli_args import parser
args = parser.parse_args()


if __name__ == '__main__':

    smw_import_overview = SMWImportOverview(ontology_ns='aeon')
    # properties
    query = Query(resource_type='property',
                  sparql_fn='query_properties.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    for printout in query.return_printout():
        item = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 ontology_ns='aeon')
        if item.item_dict.get('smw_datatype') not in [None, '']:
            item.create_wiki_item()
            smw_import_overview.properties.append(
                (item.subject_name,
                 str(item.item_dict['smw_datatype'])))
            print(item.item_dict)
            print(item.wikipage_content)
            if args.write is True:
                print('Writing Wiki Page')  # TODO: print -> log
                item.write_wikipage()
        else:
            print(f'{item.subject} MISSING aeon:SMW_datatype  value')
            # TODO print -> log

    query = Query(resource_type='category',
                  sparql_fn='query_classes.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    for printout in query.return_printout():
        item = SMWCategoryORProp(resource_type=query.resource_type,
                                 item_=printout,
                                 ontology_ns='aeon')
        if item.item_dict.get('smw_import_info'):
            item.create_wiki_item()
            smw_import_overview.categories.append(
                (item.subject_name,
                 'Category'))
            if args.write is True:
                print('Writing Wiki Page')  # TODO: print -> log
                item.write_wikipage()
            # TODO print -> log
            print(f'*****************{item.wikipage_name}*****************\n'
                  f'{item.wikipage_content}\n*****************\n')
        else:
            print(f'{item.subject} MISSING aeon:SMW_import_info value')
            # TODO print -> log
    smw_import_overview.wikipage_name = \
        f'Mediawiki:Smw_import_{item.ontology_ns}'
    smw_import_overview.ontology_name = 'Academic Event Ontology (AEON)'
    smw_import_overview.iri = item.iri
    smw_import_overview.ontology_url = 'http://ontology.tib.eu/aeon/'
    smw_import_overview.create_smw_import()
    smw_import_overview.write_wikipage()



    # query = Query(resource_type='property',
    #               sparql_fn='query_properties.rq',
    #               format_='ttl',
    #               source='aeon/aeon.ttl')
    # for printout in query.return_printout():
    #     item = SPARQLitem(resource_type=query.resource_type,
    #                       item_=printout,
    #                       ontology_ns='aeon')

# subject = last_property['subject']
# iri_base = str(subject.defrag())
