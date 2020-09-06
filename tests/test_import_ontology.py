import os
import sys
import re
from urllib.parse import urldefrag
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classes import Query, SPARQLitem


def test_test():
    assert 1 == 1


exp_importfrom = re.compile(
    "\[\[Imported from::(?P<ontology>\w.*?):(?P<category>\w.*?)]]")
exp_equivalent_uri = re.compile("\[\[Equivalent URI::(?P<uri>\w.*?)]]")
exp_categories = re.compile("\[\[Category:(?P<categories>\w.*?)]]")
exp_subcategory_line = re.compile("Subcategory\sof.*?")
exp_subcategory = re.compile(
    "Subcategory\sof.*?\[\[Category:(?P<subcat>.*?)]]")


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
            print(item.wikipage_content)
            assert item.wikipage_name.startswith(f'{resource.capitalize()}:')
            found_importfrom = re.search(pattern=exp_importfrom,
                                         string=item.wikipage_content)
            assert found_importfrom.group('ontology') == item.ontology_ns
            assert found_importfrom.group('category') == item.subject_name
            found_equivalent_uri = re.search(pattern=exp_equivalent_uri,
                                             string=item.wikipage_content)
            assert found_equivalent_uri.group('uri') == str(item.subject)
            found_cats = re.findall(pattern=exp_categories,
                                    string=item.wikipage_content)
            print(f'found_cats: {found_cats}')
            assert 'Imported vocabulary' in found_cats and \
                   item.ontology_ns.upper() in found_cats
            if re.search(pattern=exp_subcategory_line,
                         string=item.wikipage_content):
                found_subcats = re.findall(pattern=exp_subcategory,
                                           string=item.wikipage_content)
                subclass_name = urldefrag(item.item_dict['subclassof']).fragment
                print(f'Subcategory: {subclass_name} '
                      f'is found as {found_subcats}')
                assert subclass_name in found_subcats