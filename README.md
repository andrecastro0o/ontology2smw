# Ontology to SMW
_**Querying an ontology in order to bring it to import to SMW**_

[Semantic Mediawiki](https://www.semantic-mediawiki.org)(SMW) allows 
[external ontologies to be imported into a Mediawiki (MW) instance](https://www.semantic-mediawiki.org/wiki/Help:Import_vocabulary). 
external ontology's properties and classes can be used inside the MW instance, and produce a RDF exports of 
the wiki pages, which point to IRIs of the imported ontology(s).

The process of importing is simple, but time consuming. Hence making it a perfect candidate for an automated process, 
which can be run at anytime a new version of the ontology is published, hence this python script.

Currently the script works only with [The Academic Event Ontology (AEON)](https://github.com/tibonto/aeon) in the context of the confIDent project,
but seems possible to make it work with any ontology and an instances of SMW. 

<!-- HOW IS THE IMPORT DONE -->

## Run Script:
**Prerequisites:** 

In virtual environment install requirements `pip install -r requirements.txt`

Git add [aeon/confIDent](https://github.com/tibonto/aeon/tree/confIDent) as submodule
`./git_submod_add_aeon.sh`

**Run:**

without writing to pages: `python ./main.py ` 

writing to wiki pages: `python ./main.py --write` 


## To write wiki pages
**wikidetails.yml & wiki write access**
* Ensure user your wiki user account belongs to bot group: see wiki page `Special:UserRights`
* Create a bot password in wiki page: `Special:BotPasswords`
* copy `wikidetails.template.yml` as `wikidetails.yml` and fill in bot name and password:<br/>
    
## Properties from other ontologies
AEON makes use of the properties from OWL and BFO namespaces, namely:
* [owl:topDataProperty](http://www.w3.org/2002/07/owl#topDataProperty) ` rdfs:comment "The data property that relates every individual to every data value."`
* [obo:BFO_0000015](http://purl.obolibrary.org/obo/BFO_0000015) `rdfs:label "process"@en`
* [obo:BFO_0000023](http://purl.obolibrary.org/obo/BFO_0000023) `rdfs:label "role"@en`
    
Which requires us to also **include them to SMW (currently manually) in Mediawiki instaces pages**:

*MediaWiki:Smw_import_owl* appending the rest of the resource list:<br/> 
``` 
 topDataProperty|Type:Page
 topObjectProperty|Type:Page
```

*Property:topDataProperty*:
```
Imported from [[Imported from::owl:topDataProperty]]

Equivalent URI [[Equivalent URI::http://www.w3.org/2002/07/owl#topDataProperty]]

Has type [[Has type::Page]]

[[Category:OWL]] [[Category:Imported vocabulary]]
```

*Property:topObjectProperty*:
```
Imported from [[Imported from::owl:topObjectProperty]]

Equivalent URI [[Equivalent URI::http://www.w3.org/2002/07/owl#topObjectProperty]]

Has type [[Has type::Page]]

[[Category:OWL]] [[Category:Imported vocabulary]]
```

*MediaWiki:Smw_import_bfo*:
```
http://purl.obolibrary.org/obo/|[https://basic-formal-ontology.org/ Basic Formal Ontology (BFO)]

 BFO_0000015|Category
 BFO_0000023|Category

[[Category:Imported vocabulary]] [[Category:BFO]]
``` 

*Category:BFO_0000015*:
```
Imported from [[Imported from::bfo:BFO_0000015]]

Equivalent URI [[Equivalent URI::http://purl.obolibrary.org/obo/BFO_0000015]]


[[Category:BFO]] [[Category:Imported vocabulary]]
```

*Category BFO_0000023*:
```
Imported from [[Imported from::bfo:BFO_0000023]]

Equivalent URI [[Equivalent URI::http://purl.obolibrary.org/obo/BFO_0000015]]

[[Category:BFO]] [[Category:Imported vocabulary]]
```




## queries with [ARQ](https://jena.apache.org/documentation/query/)
`arq --data=aeon/aeon.ttl   --query=queries/ontology.rq`

`arq --data=aeon/aeon.ttl   --query=queries/query_classes.rq`

`arq --data=aeon/aeon.ttl   --query=queries/query_properties.rq`