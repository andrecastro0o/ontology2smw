import re
import rdflib
import string
import pytest
from pathlib import Path
from random import choice
from ontology2smw.classes import QueryOntology, SMWCategoryORProp, \
    xsd2smwdatatype
from ontology2smw.mediawikitools import actions
from ontology2smw.file_utils import yaml_get_source

ontos = [
    ('https://d-nb.info/standards/elementset/gnd.ttl', 'ttl'),
    ('http://www.w3.org/ns/dcat#', 'application/rdf+xml'),
    ('http://rdf.muninn-project.org/ontologies/military.owl',
     'application/rdf+xml'),
    ('http://purl.org/spar/datacite', 'application/rdf+xml'),
]
onto_uri, onto_format = choice(ontos)


@pytest.mark.ontology
def test_queryontology_class():
    print(onto_uri)
    query = QueryOntology(
        sparql_fn='ontology2smw/queries/query_ontology_schema.rq',
        format_=onto_format, source=onto_uri)
    query.get_graph_prefixes()
    printouts = list(query.return_printout())
    assert len(list(printouts)) > 0
    assert len(query.prefixes) > 0


@pytest.mark.termsinsmw
def test_term_creation_from_remote_onto():
    regex_import_str = re.compile(
        r"Imported from \[\[Imported from::(?P<prefix>\w+?):(?P<term>\w+?)]]",
        re.MULTILINE
    )
    regex_label_str = re.compile(
        r"\[\[Has property description::(?P<desc>(.|\n)+?)@(?P<lang>\w+?)]]",
        re.MULTILINE
    )

    query = QueryOntology(sparql_fn='ontology2smw/queries/ontology_terms.rq',
                          format_='application/rdf+xml',
                          source='https://d-nb.info/standards/elementset/gnd')
    query.get_graph_prefixes()
    for printout in query.return_printout():
        assert printout
        term = SMWCategoryORProp(item_=printout, query_=query)
        term.create_wiki_item()
        assert len(term.wikipage_name)
        assert len(term.wikipage_content)
        assert len(re.findall(regex_import_str, term.wikipage_content)) > 0
        search = re.search(regex_import_str, term.wikipage_content)
        assert len(search.group('prefix')) > 0, 'Error: no prefix found'
        assert len(search.group('term')) > 0, 'Error: no term found'
        assert search.group('term') in term.wikipage_name

        if term.term_dict['label']:
            print(f'wiki page: {term.wikipage_content}')
            label_search = re.search(regex_label_str, term.wikipage_content)
            assert len(label_search.group('desc')) > 0, \
                'Error: no term desc found'
        if term.resource_type == 'Property':
            assert term.prop_datatype, 'Error: NO term.prop_datatype'
            if term.prop_datatype != 'Page':
                assert term.prop_datatype in set(xsd2smwdatatype.values()), \
                    'Error: prop_datatype not in xsd2smwdatatype'


@pytest.mark.smw
def test_term_creation_from_local_onto():
    query = QueryOntology(sparql_fn='ontology2smw/queries/ontology_terms.rq',
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
        assert term.term_dict['smw_import_info']
        term.create_wiki_item()


def randstring(lenght=10):
    out = "".join([choice(list(string.ascii_letters)) for n in range(lenght)])
    return out


@pytest.mark.skip(reason="requires VM w/ SMW")
@pytest.mark.smw
def test_category_creation():
    current_file = Path(__file__)
    root_dir = current_file.parent.parent.parent
    print(root_dir)
    wikidetails = root_dir / 'wikidetails.yml'
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


@pytest.mark.skip(reason="requires VM w/ SMW")
@pytest.mark.smw
def test_smw_import_creation():
    current_file = Path(__file__)
    root_dir = current_file.parent.parent.parent
    print(root_dir)
    wikidetails = root_dir / 'wikidetails.yml'
    print(wikidetails)
    wikidetails = yaml_get_source(wikidetails)
    site = actions.login(host=wikidetails['host'],
                         path=wikidetails['path'],
                         scheme=wikidetails['scheme'],
                         username=wikidetails['username'],
                         password=wikidetails['password'])
    actions.edit(
        page='MediaWiki:Smw_import_test', content='Test',
        summary='Testing Smw_import_ \n[[Category:Imported vocabulary]]',
        append=True)
    page_content, page_lastrev = actions.read(page='Category:Test')
    assert page_lastrev
    assert 'Test' in page_content


@pytest.mark.ontology
def test_non_repeating_terms():
    graph = rdflib.Graph()
    graph.parse(location=onto_uri, format=onto_format)
    with open('ontology2smw/queries/ontology_terms.rq', 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    assert printouts
