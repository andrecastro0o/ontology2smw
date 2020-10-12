from ontology2smw.functions import sparql2smwpage
# from pprint import pprint
# from log import logger
# args = parser.parse_args()
# args = parser.parse_args()

from ontology2smw.cli_args import parser
args = parser.parse_args()

def main():
    sparql2smwpage(
        sparql_fn='ontology2smw/queries/query_classes_properties.rq',
        format_='ttl',
        source='aeon/aeon.ttl',
        )


if __name__ == '__main__':
    main()
# TODO: get source from cli args
