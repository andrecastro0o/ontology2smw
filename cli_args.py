from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(
    description="""
                   ___    
                 { . . } 
--------------o00---'----00o--
confIDent ontology2SMW  
-----------------------------""", formatter_class=RawTextHelpFormatter)
parser.add_argument('-w', '--write', action='store_true',
                    help="writes the output to wiki or file. "
                         "Default: False (dry-run).")
