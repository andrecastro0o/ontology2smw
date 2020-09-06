from classes import Query, SPARQLitem
from cli_args import parser
args = parser.parse_args()



if __name__ == '__main__':
    query = Query(resource_type='category',
                  sparql_fn='query_classes.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    for printout in query.return_printout():
        item = SPARQLitem(resource_type=query.resource_type,
                          item_=printout,
                          ontology_ns='aeon')
        if item.item_dict.get('smw_import_info'):
            item.create_wiki_item()
            print(args)
            if args.write is True:
                print('Writing Wiki Page')  # TODO: print -> log
                item.write_wikipage()
            # TODO print -> log
            print(f'*****************{item.wikipage_name}*****************\n'
                  f'{item.wikipage_content}\n*****************\n')
        else:
            print(f'{item.subject} MISSING aeon:SMW_import_info value')
            # TODO print -> log


# subject = last_property['subject']
# iri_base = str(subject.defrag())
