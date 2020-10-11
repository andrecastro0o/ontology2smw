import os
import sys
import re
import rdflib
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classes import Query, SMWCategoryORProp
from functions import get_term_ns_prefix
from jinja_utils import url_termination


def test_ontology_parse():
    graph = rdflib.Graph()
    graph.parse(
        source='aeon/aeon.ttl',
        format='ttl')
    assert graph


exp_importfrom = re.compile(
    "\[\[Imported from::(?P<ontology>\w.*?):(?P<category>\w.*?)]]")
exp_equivalent_uri = re.compile("\[\[Equivalent URI::(?P<uri>\w.*?)]]")
exp_categories = re.compile("\[\[Category:(?P<categories>\w.*?)]]")
exp_subcategory_line = re.compile("Subcategory\sof.*?")
exp_subcategory = re.compile(
    "Subcategory\sof.*?\[\[Category:(?P<subcat>.*?)]]")


def test_term_creation():
    query = Query(sparql_fn='query_class_prop.rq',
                  format_='ttl',
                  source='aeon/aeon.ttl')
    assert query
    for printout in query.return_printout():
        assert printout
        ns, ns_prefix = get_term_ns_prefix(term=printout.subject,
                                           prefixes=query.prefixes)

        term = SMWCategoryORProp(item_=printout,
                                 namespace=ns,
                                 namespace_prefix=ns_prefix)
        assert term.item_dict['smw_import_info']
        term.create_wiki_item()

# def test_category_creation():
#     resource = 'category'
#     query = Query(resource_type='category',
#                   sparql_fn='query_classes.rq',
#                   format_='ttl',
#                   source='aeon/aeon.ttl')
#     assert query
#     for printout in query.return_printout():
#         item = SMWCategoryORProp(resource_type=query.resource_type,
#                                  item_=printout,
#                                  namespace='aeon')
#         assert item.item_dict['smw_import_info']
#         item.create_wiki_item()
#         print(item.wikipage_content)
#         assert item.wikipage_name.startswith(f'{resource.capitalize()}:')
#         assert ':]]' not in item.wikipage_content  # empty prop/category
#         found_importfrom = re.search(pattern=exp_importfrom,
#                                      string=item.wikipage_content)
#         assert found_importfrom.group('ontology') == item.ontology_ns
#         assert found_importfrom.group('category') == item.subject_name
#         found_equivalent_uri = re.search(pattern=exp_equivalent_uri,
#                                          string=item.wikipage_content)
#         assert found_equivalent_uri.group('uri') == str(item.subject)
#         found_cats = re.findall(pattern=exp_categories,
#                                 string=item.wikipage_content)
#         print(f'found_cats: {found_cats}')
#         assert 'Imported vocabulary' in found_cats and \
#                item.ontology_ns.upper() in found_cats
#         if re.search(pattern=exp_subcategory_line,
#                      string=item.wikipage_content):
#             found_subcats = re.findall(pattern=exp_subcategory,
#                                        string=item.wikipage_content)
#             subclass_name = url_termination(item.item_dict['subclassof'])
#             print(f'Subcategory: {subclass_name} '
#                   f'is found as {found_subcats}')
#             assert subclass_name in found_subcats


# def test_property_creation():
#     resource = 'property'
#     query = Query(resource_type='property',
#                   sparql_fn='query_properties.rq',
#                   format_='ttl',
#                   source='aeon/aeon.ttl')
#     assert query
#     for printout in query.return_printout():
#         item = SMWCategoryORProp(resource_type=query.resource_type,
#                                  item_=printout,
#                                  namespace='aeon')
#         assert item.item_dict['smw_import_info']
#         item.create_wiki_item()
#         print(item.wikipage_name)
#         print(item.wikipage_content)
#         assert item.wikipage_name.startswith(resource.capitalize())
#         assert item.wikipage_name.split(':')[-1] == item.subject_name and \
#                item.wikipage_name.split(':')[-1] in item.subject
#
#         assert ':]]' not in item.wikipage_content  # empty prop/category
#         found_importfrom = re.search(pattern=exp_importfrom,
#                                      string=item.wikipage_content)
#         assert found_importfrom.group('ontology') == item.ontology_ns
#         assert found_importfrom.group('category') == item.subject_name
#         found_equivalent_uri = re.search(pattern=exp_equivalent_uri,
#                                          string=item.wikipage_content)
#         assert found_equivalent_uri.group('uri') == str(item.subject)
#         found_cats = re.findall(pattern=exp_categories,
#                                 string=item.wikipage_content)
#         print(f'found_cats: {found_cats}')
#         assert 'Imported vocabulary' in found_cats and \
#                item.ontology_ns.upper() in found_cats
#         # if re.search(pattern=exp_subcategory_line,
#         #              string=item.wikipage_content):
#         #     found_subcats = re.findall(pattern=exp_subcategory,
#         #                                string=item.wikipage_content)
#         #     subclass_name = url_termination(item.item_dict['subclassof'])
#         #     print(f'Subcategory: {subclass_name} '
#         #           f'is found as {found_subcats}')
#         #     assert subclass_name in found_subcats