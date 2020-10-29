import sys
from pathlib import Path
from ontology2smw.cli_args import parser
from ontology2smw.file_utils import yaml_get_source
from ontology2smw.mediawikitools.actions import login

args = parser.parse_args()


def main():
    if not args.ontology:
        print("Error: mandatory argument --ontology was not provided",
              file=sys.stderr)
        sys.exit()
    if args.write:
        write_confirm = input(
            "You enabled --write. Are you sure you want to write to the wiki? "
            "(If you say yes, make sure to disable cronjob for "
            "mediawiki/maintenance/runJobs.php) [yes/no]")
        if write_confirm == 'yes':
            wikidetails = Path(__file__).parent.parent / 'wikidetails.yml'
            if Path.is_file(wikidetails) is False:
                print('No wikidetails.yml file was found in the root '
                      'directory. Hence is not possible to write to the wiki')
                sys.exit()
            wikidetails = yaml_get_source(wikidetails)
            site = login(host=wikidetails['host'],
                         path=wikidetails['path'],
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
    from ontology2smw.functions import sparql2smwpage
    sparql2smwpage(
        sparql_fn='ontology2smw/queries/query_classes_properties.rq',
        format_=args.format,
        source=args.ontology,
    )


if __name__ == '__main__':
    main()
# TODO: get source from cli args
