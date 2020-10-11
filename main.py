from cli_args import parser
from functions import query2page
# from pprint import pprint
# from log import logger
args = parser.parse_args()




if __name__ == '__main__':
    query2page(sparql_fn='query_class_prop.rq',
               format_='ttl',
               source='aeon/aeon.ttl',
               )
