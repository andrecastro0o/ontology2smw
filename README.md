# Ontology to SMW
_**Querying an ontology in order to bring it to import to SMW**_

In virtual environment install requirements `pip install -r requirements.txt`

Git add [aeon/confIDent](https://github.com/tibonto/aeon/tree/confIDent) as submodule
`./git_submod_add_aeon.sh`

python script: `python ./main.py ` 


## queries with [ARQ](https://jena.apache.org/documentation/query/)
`arq --data=aeon/aeon.ttl   --query=queries/ontology.rq`

`arq --data=aeon/aeon.ttl   --query=queries/query_classes.rq`

`arq --data=aeon/aeon.ttl   --query=queries/query_properties.rq`