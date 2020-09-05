import rdflib, os, sys
from rdflib.namespace import OWL, RDF, RDFS
from pathlib import Path
from pprint import pprint

if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(
        source='aeon/aeon.ttl',
        format='ttl'
                )

    for query_fn in os.listdir(Path.cwd() / 'queries'):
        query_path = Path.cwd() / 'queries' / query_fn
        print(f'\n\n*** {query_path} ***\n')
        with open(query_path, 'r') as query_fobj:
            query = query_fobj.read()

        query = graph.query(query,
                            initNs={'rdf': RDF, 'rdfs': RDFS, 'owl': OWL})

        for result in query:
            result_dict = result.asdict()
            last_property = result_dict
            pprint(result_dict)

# subject = last_property['subject']
# iri_base = str(subject.defrag())
