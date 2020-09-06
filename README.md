# Ontology to SMW
_**Querying an ontology in order to bring it to import to SMW**_

In virtual environment install requirements `pip install -r requirements.txt`

Git add [aeon/confIDent](https://github.com/tibonto/aeon/tree/confIDent) as submodule
`./git_submod_add_aeon.sh`

run python script: `python ./main.py ` 

run python script and allow it to write wiki pages: `python ./main.py --write` 


## To write wiki pages
**wikidetails.yml & wiki write access**
* Ensure user your wiki user account belongs to bot group: see wiki page `Special:UserRights`
* Create a bot password in wiki page: `Special:BotPasswords`
* copy `wikidetails.template.yml` as `wikidetails.yml` and fill in bot name and password:<br/>
    
    

## queries with [ARQ](https://jena.apache.org/documentation/query/)
`arq --data=aeon/aeon.ttl   --query=queries/ontology.rq`

`arq --data=aeon/aeon.ttl   --query=queries/query_classes.rq`

`arq --data=aeon/aeon.ttl   --query=queries/query_properties.rq`