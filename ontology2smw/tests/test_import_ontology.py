import os
import sys
import re
import rdflib
import string
import pytest
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from random import choice
from ontology2smw.classes import QueryOntology, SMWCategoryORProp
from ontology2smw.functions import get_term_ns_prefix
from ontology2smw.jinja_utils import url_termination
from ontology2smw.mediawikitools import actions
from ontology2smw.file_utils import yaml_get_source

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.ontology
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

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.ontology
def test_query_class():
    ontology_ns = 'http://www.w3.org/2004/02/skos/core#'
    query = QueryOntology(sparql_fn='ontology2smw/queries/query_ontology_schema.rq',
                          format_="application/rdf+xml", source=ontology_ns)
    printouts = list(query.return_printout())
    print(printouts)
    assert len(list(printouts)) > 0
    # ontology_ns = 'http://purl.obolibrary.org/obo/'
    # query = Query(sparql_fn='queries/query_ontology_schema.rq',
    #               format_="application/rdf+xml", source=ontology_ns)
    # query.return_printout()
    # printouts = list(query.return_printout())
    # assert len(printouts) == 0

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.smw
def test_term_creation():
    query = QueryOntology(sparql_fn='ontology2smw/queries/query_classes_properties.rq',
                          format_='ttl',
                          source='aeon/aeon.ttl')
    query.get_graph_prefixes()
    assert query
    for printout in query.return_printout():
        assert printout
        ns, ns_prefix = get_term_ns_prefix(term_uri=printout.term,
                                           allprefixes=query.prefixes)

        term = SMWCategoryORProp(item_=printout,
                                 namespace=ns,
                                 namespace_prefix=ns_prefix)
        assert term.item_dict['smw_import_info']
        term.create_wiki_item()


def randstring(lenght=10):
    out = "".join([choice(list(string.ascii_letters)) for n in range(lenght)])
    return out

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.smw
def test_category_creation():
    # TODO: block should go to fixtures
    current_file = Path(__file__)
    root_dir = current_file.parent.parent.parent
    print(root_dir)
    wikidetails = root_dir  / 'wikidetails.yml'
    print(wikidetails)
    wikidetails = yaml_get_source(wikidetails)
    site = actions.login(host=wikidetails['host'],
                         path=wikidetails['path'],
                         scheme=wikidetails['scheme'],
                         username=wikidetails['username'],
                         password=wikidetails['password'])
    # end of block
    actions.edit(page='Category:Test', content='Test',
                 summary='Testing Category creation',
                 append=True)
    page_content, page_lastrev = actions.read(page='Category:Test')
    assert page_lastrev
    assert 'Test' in page_content

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.smw
def test_smw_import_creation():
    # TODO: block should go to fixtures
    current_file = Path(__file__)
    root_dir = current_file.parent.parent.parent
    print(root_dir)
    wikidetails = root_dir  / 'wikidetails.yml'
    print(wikidetails)
    wikidetails = yaml_get_source(wikidetails)
    site = actions.login(host=wikidetails['host'],
                         path=wikidetails['path'],
                         scheme=wikidetails['scheme'],
                         username=wikidetails['username'],
                         password=wikidetails['password'])
    # end of block
    actions.edit(page='MediaWiki:Smw_import_test', content='Test',
                 summary='Testing Smw_import_ creation\n[[Category:Imported vocabulary]]',
                 append=True)
    page_content, page_lastrev = actions.read(page='Category:Test')
    assert page_lastrev
    assert 'Test' in page_content

@pytest.mark.ontologyterms
def test_non_repeating_terms():
    all_ontologies = ['http://purl.org/spar/datacite', 'https://d-nb.info/standards/elementset/gnd']
    ontology_ns = all_ontologies[1]
    graph = rdflib.Graph()
    graph.parse(location=ontology_ns, format="application/rdf+xml")
    with open('ontology2smw/queries/ontology_terms.rq', 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    assert printouts

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