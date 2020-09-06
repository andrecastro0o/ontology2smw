import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classes import Query, SPARQLitem

def test_test():
    assert 1 == 1


def test_category_creation():
    resource = 'category'
    query = Query(resource_type='category',
                  sparql_fn='query_classes.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    assert query
    for printout in query.return_printout():
        item = SPARQLitem(resource_type=query.resource_type,
                          item_=printout,
                          ontology_ns='aeon')
        if item.item_dict.get('smw_import_info'):
            item.create_wiki_item()
            print(item.wikipage_name)
            assert item.wikipage_name.startswith(f'{resource.capitalize()}:')
