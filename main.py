import rdflib
from rdflib.namespace import OWL, RDF, RDFS

query_classes = '''
SELECT ?subject ?subclassof  
WHERE {?subject rdf:type owl:Class;  
                rdfs:subClassOf ?subclassof.
        FILTER(STRSTARTS(STR(?subject), "https://github.com/tibonto/aeon#"))
                }
 '''

query_properties = '''
SELECT ?subject ?subpropertyof ?domain ?type
WHERE {
    {?subject rdf:type owl:AnnotationProperty}
    UNION {?subject rdf:type owl:ObjectProperty}
    UNION {?subject rdf:type owl:DatatypeProperty}.
    OPTIONAL {
        ?subject rdfs:subPropertyOf ?subpropertyof;
                 rdfs:domain ?domain ;
                 rdf:type ?type.
        }
    FILTER(STRSTARTS(STR(?subject), "https://github.com/tibonto/aeon#")).
}
ORDER BY ?type
 '''



if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(
        source='https://raw.githubusercontent.com/tibonto/aeon/confIDent/aeon.ttl',
        format='ttl'
                )
    print(len(graph))

    # for result in graph.query(query_classes, initNs={
    #     'rdf': RDF, 'rdfs': RDFS,'owl': OWL}):
    #     subject, subclass = result
    #     last_class = result
    #     print(result, subject, subclass)

    for result in graph.query(query_properties, initNs={
        'rdf': RDF, 'rdfs': RDFS,'owl': OWL}):
        subject, subpropertyof, domain, type = result
        # subject, subpropertyof = result
        last_property = result
        print(result, subject)

# find NS,
# classes:
#   rdf:type owl:Class
# properties:
#   Annotation properties: rdf:type  owl:AnnotationProperty
#   Object Properties: rdf:type owl:ObjectProperty (subclass of rdf:Property)
#   Data properties: rdf:type owl:DatatypeProperty

# ensure that only the properties and classes from the NS aeon are imported
# ie obo:IAO_0000112 rdf:type owl:AnnotationProperty .
"""
QUESTIONS FOR PHILIP:

The presence of dataType in properties would be useful in bringin them to SMW
"""