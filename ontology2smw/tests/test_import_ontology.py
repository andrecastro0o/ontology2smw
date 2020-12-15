import re
import rdflib
import string
import pytest
from pathlib import Path
from random import choice
from ontology2smw.classes import MWpage, QueryOntology, SMWCategoryORProp, \
    SMWImportOverview, xsd2smwdatatype, Report
from ontology2smw.mediawikitools import actions
from ontology2smw.file_utils import yaml_get_source, readfile, removefile

ontos = [
    # ('https://d-nb.info/standards/elementset/gnd.ttl', 'gndo', 'ttl'),
    ('http://www.w3.org/ns/dcat#', 'dcat', 'application/rdf+xml'),
    ('http://www.w3.org/ns/dcat#', 'dcat', 'application/rdf+xml'),
    ('http://purl.org/spar/datacite', 'datacite', 'application/rdf+xml'),
    # ('http://purl.obolibrary.org/obo/ncbitaxon.owl#', 'ncbitaxon',
    #  'application/rdf+xml'),  # too large to handle
]
onto_uri, onto_prefix, onto_format = choice(ontos)


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
        # tests def determine_smw_catORprop
        termtype = str(term.term_dict.get('termType'))
        assert term.resource_type.replace('Category', 'Class') in termtype

        if term.resource_type == 'Property':
            assert term.prop_datatype, 'Error: NO term.prop_datatype'
            if term.prop_datatype != 'Page':
                assert term.prop_datatype in set(xsd2smwdatatype.values()), \
                    'Error: prop_datatype not in xsd2smwdatatype'


def randstring(lenght=10):
    out = "".join([choice(list(string.ascii_letters)) for n in range(lenght)])
    return out


@pytest.mark.ontology
def test_non_repeating_terms():
    graph = rdflib.Graph()
    graph.parse(location=onto_uri, format=onto_format)
    with open('ontology2smw/queries/ontology_terms.rq', 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    assert printouts


@pytest.mark.smw
def test_wiki_terms_creation():
    current_file = Path(__file__)
    root_dir = current_file.parent.parent.parent
    print(root_dir)
    wikidetails = root_dir / 'wikidetails.yml'
    print(wikidetails)
    wikidetails = yaml_get_source(wikidetails)
    actions.login(host=wikidetails['host'],
                  path=wikidetails['path'],
                  scheme=wikidetails['scheme'],
                  username=wikidetails['username'],
                  password=wikidetails['password'])
    actions.edit(page='Category:Test', content='Test',
                 summary='Testing Category creation',
                 append=True)
    page_content, page_lastrev = actions.read(page='Category:Test')
    assert page_lastrev
    assert 'Test' in page_content
    # create the MediaWiki:Smw_import_test page and
    actions.edit(
        page='MediaWiki:Smw_import_test', content='Test',
        summary='Testing Smw_import_ \n[[Category:Imported vocabulary]]',
        append=True)
    page_content, page_lastrev = actions.read(page='Category:Test')
    assert page_lastrev
    assert 'Test' in page_content


@pytest.mark.smw
def test_MWpage():
    mwpage = MWpage()
    mwpage.wikipage_name = "Main_Page"
    mwpage.wikipage_content = f"=ontology2smw test: {randstring()}="
    mwpage.write_wikipage()
    page_content, page_lastrev = actions.read(page=mwpage.wikipage_name)
    assert page_content == mwpage.wikipage_content


@pytest.mark.termsinsmw
def test_smwimportoverview():
    for onto in ontos:
        local_onto_uri, local_onto_prefix, local_onto_format = onto
        smwimport_overview = SMWImportOverview(
            ontology_ns=local_onto_uri,
            ontology_ns_prefix=local_onto_prefix,
            ontology_format=local_onto_format)
        assert smwimport_overview.ontology_ns_prefix in \
               smwimport_overview.wikipage_name
        smwimport_overview.create_smw_import()
        assert smwimport_overview.ontology_ns in \
               smwimport_overview.wikipage_content
        prefix_ = smwimport_overview.ontology_ns_prefix.upper()
        category = f'[[Category:{prefix_}]]'
        assert category in smwimport_overview.wikipage_content
        print(smwimport_overview.title, smwimport_overview.version,
              smwimport_overview.desc)
        assert smwimport_overview.title is not None


@pytest.mark.uri
def test_can_resolve_uri():
    for onto in ontos:
        uri = onto[0]
    smwimport = SMWImportOverview
    print(uri)
    uri_resolve = smwimport.can_resolve_uri(self=SMWImportOverview,
                                            uri=uri,
                                            contenttype='application/rdf+xml')
    if uri == 'http://purl.org/spar/datacite/':
        assert uri_resolve is False
    elif uri == 'http://purl.obolibrary.org/obo/ncbitaxon.owl#':
        assert uri_resolve is False
    elif uri == 'http://www.w3.org/ns/dcat#':
        assert uri_resolve is False


@pytest.mark.outputreport
def test_report():
    smw_import_dict = {}
    smw_import_dict[onto_prefix] = SMWImportOverview(
        ontology_ns=onto_uri,
        ontology_ns_prefix=onto_prefix,
        ontology_format=onto_format)
    smw_import_dict[onto_prefix].create_smw_import()
    removefile(filename='report.txt')
    reportobj = Report(importdict=smw_import_dict,
                       cli_arg_write=False,
                       verbose=False,
                       output=True,
                       cache='')
    assert reportobj.report
    assert onto_prefix in reportobj.report
    assert f'Mediawiki:Smw_import_{onto_prefix}' in reportobj.report
    assert reportobj.output_file is True or reportobj.output_file is False
    filepath, content = readfile(filename='report.txt')
    assert 'report.txt' in str(filepath)
    assert f'Mediawiki:Smw_import_{onto_prefix}' in content
    assert len(reportobj.report_cache) > 0
