from functions import sparql2smwpage
# from pprint import pprint
# from log import logger
# args = parser.parse_args()


if __name__ == '__main__':
    sparql2smwpage(sparql_fn='query_class_prop.rq',
                   format_='ttl',
                   source='aeon/aeon.ttl',
                   )
