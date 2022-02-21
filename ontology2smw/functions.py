import sys
from pathlib import Path
from ontology2smw.file_utils import yaml_get_source
from ontology2smw.mediawikitools.actions import login
from ontology2smw.classes import QueryOntology
from ontology2smw.classes import SMWCategoryORProp
from ontology2smw.classes import SMWImportOverview
from ontology2smw.classes import Report
from ontology2smw.cli_args import parser

args = parser.parse_args()


def print_n_add2cache(msg, cache):
    '''
    To be used by class Report to provide a report
    '''
    cache += msg
    print(msg)
    return cache


# def copied from Query Class (should reuse that one)
def query_graph(sparql_fn, graph):
    with open(sparql_fn, 'r') as query_fobj:
        sparq_query = query_fobj.read()
    printouts = graph.query(sparq_query)
    return printouts


def create_smw_import_pages(importdict):
    """
    Creates Mediawiki:smw_import_ONTO page
        For each of the ontologies in importdict (SMWCategoryORProp
        instance)
    """
    for prefix, importoverview in importdict.items():
        # pprint(importoverview.__dict__)
        importoverview.create_smw_import()
        if args.write is True:
            importoverview.write_wikipage()  # ATTENTION: will write to wiki


def sparql2smwpage(sparql_fn: str, format_: str, source: str):
    report_cache = ''
    if format_ == 'rdf':
        format_ = 'application/rdf+xml'
    """
    Performs the calls necessary to turn SPARQL query to SMW pages required
    to import the ontology
    """
    smw_import_dict = {}  # will store SMWImportOverview instances
    query = QueryOntology(sparql_fn=sparql_fn, format_=format_, source=source)
    query.get_graph_prefixes()
    for printout in query.return_printout():
        # loop through each ontology schema term, resulting from SPARQL query
        term = SMWCategoryORProp(item_=printout, query_=query)
        if args.verbose is True:
            msg_str = f'\n{"-"*10}\n{term.wikipage_name}\n{"-"*10}'
            report_cache = print_n_add2cache(msg=msg_str, cache=report_cache)
        else:
            msg_str = f'{term.wikipage_name}\n'
            report_cache = print_n_add2cache(msg=msg_str, cache=report_cache)

        if args.write is True:
            term.write_wikipage()
        if args.verbose is True:
            msg_str = term.wikipage_content.replace("\n\n", "\n")
            report_cache = print_n_add2cache(msg=msg_str, cache=report_cache)

        if term.namespace_prefix not in smw_import_dict.keys():
            smw_import_dict[term.namespace_prefix] = SMWImportOverview(
                ontology_ns=term.namespace,
                ontology_ns_prefix=term.namespace_prefix,
                ontology_format=format_)
        # smw_import_dict[term.namespace_prefix].terms is []
        # of tuples as found in MediaWiki:Smw_import_xyz
        # ie: abstract|Type:Page
        #     Location|Category
        if term.resource_type == 'Category':
            smw_import_dict[term.namespace_prefix].terms.append(
                (term.term_name, term.resource_type))
        elif term.resource_type == 'Property':
            smw_import_dict[term.namespace_prefix].terms.append(
                (term.term_name, f'Type:{term.prop_datatype}'))

        # print(term.item_dict)
    create_smw_import_pages(importdict=smw_import_dict)
    reportobj = Report(importdict=smw_import_dict,
                       cli_arg_write=args.write,
                       verbose=args.verbose,
                       output=args.report,
                       cache=report_cache)
    print(reportobj.report)


def writetowiki_decision():
    """
    Prompts the users to confirm they wants to write to the wiki
    If so wiki bot login will take place and connection will be available
    under var site
    """
    write_confirm = input(
        "You enabled --write. Are you sure you want to write to the wiki? "
        "(If you say yes, make sure to disable cronjob for "
        "mediawiki/maintenance/runJobs.php) [yes/no]")
    if write_confirm == 'yes':
        # use custom wikidetails.yml location
        if args.settings:
            wikidetails = Path(args.settings)
        else:
            wikidetails = Path('.') / 'wikidetails.yml'
        if Path.is_file(wikidetails) is False:
            print(f'No wikidetails.yml file was found in '
                  f'{wikidetails.absolute()}. Is is not possible to write'
                  f' to the wiki')
            sys.exit()
        wikidetails = yaml_get_source(path2f=wikidetails, absolutepath=True)
        site = login(host=wikidetails['host'], path=wikidetails['path'],
                     scheme=wikidetails['scheme'],
                     username=wikidetails['username'],
                     password=wikidetails['password'])
        print(f'Bot logged in to wiki {site.host} {site.path}')
        print('Terms will be written to wiki')
        pass
    else:
        print('If you do not want to write to the wiki, run it wihtout '
              'argument: -w/--write')
        sys.exit()
