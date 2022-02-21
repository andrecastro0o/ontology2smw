import sys
from pathlib import Path
from ontology2smw.cli_args import parser
from ontology2smw.functions import writetowiki_decision
from ontology2smw.functions import sparql2smwpage

args = parser.parse_args()


def main():
    if not args.ontology:
        print("Error: mandatory argument --ontology was not provided",
              file=sys.stderr)
        sys.exit()
    if args.write:
        writetowiki_decision()

    # get base path of the code
    base_path = Path(__file__).parent

    sparql2smwpage(
        sparql_fn=base_path / 'queries' / 'ontology_terms.rq',
        format_=args.format,
        source=args.ontology,
    )


if __name__ == '__main__':
    main()
