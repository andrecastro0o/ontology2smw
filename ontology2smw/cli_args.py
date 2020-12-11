from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(
    description="""
                   ___    
                 { . . } 
--------------o00---'----00o--
              ontology2SMW  
-----------------------------""", formatter_class=RawTextHelpFormatter)
parser.add_argument('-w', '--write', action='store_true',
                    help="writes the output to wiki or file. "
                         "Default: False (dry-run).")
parser.add_argument('-o', '--ontology',
                    default='https://raw.githubusercontent.com/tibonto/aeon/master/aeon.ttl',
                    help="Ontology file or URI. "
                    "Default: https://raw.githubusercontent.com/tibonto/aeon/master/aeon.ttl ")
parser.add_argument('-f', '--format',
                    choices=['rdf', 'ttl'],
                    default='ttl',
                    help="Ontology format. Default value: ttl")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Verbose output. Default: False.")
parser.add_argument('-r', '--report', action='store_true',
                    help="Save report in file report.txt Default: False.")

