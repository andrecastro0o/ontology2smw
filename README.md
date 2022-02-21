![ontology2smw build](https://github.com/TIBHannover/ontology2smw/workflows/ontology2smw%20build/badge.svg)
![pytest](https://github.com/TIBHannover/ontology2smw/workflows/pytest/badge.svg)

# Ontology to SMW
_**Automating an RDF ontology import into Semantic Mediawiki**_

[Semantic Mediawiki](https://www.semantic-mediawiki.org)(SMW) allows
[external ontologies to be imported into a Mediawiki (MW) instance](https://www.semantic-mediawiki.org/wiki/Help:Import_vocabulary).
External ontology's properties and classes can be used inside the MW instance, and produce a RDF exports of
the wiki pages, which point to IRIs of the imported ontology(s).

The process of importing is simple, but time consuming. Hence making it a perfect candidate for an automated process,
which can be run at anytime a new version of the ontology is published, hence this python script.

Watch the [ontology2smw presentation](https://youtu.be/AQfJL-i6s88) at SMWCon 2020.

![ontology2smw import workflow](docs/ontology2smw_aeon.svg?raw=true)

Supports:
* python3.6, python3.7, python3.8


## Install:

### Manually
```bash
git clone https://github.com/TIBHannover/ontology2smw.git
cd ontology2smw
# ---- (optional) create and activate a virtual-environment
python -m venv venv
source venv/bin/activate
# ---- virtual environment created
pip install --upgrade setuptools
python setup.py install
```


## Run:

**Run:**



Using a remote ontology:<br/>`ontology2smw --format ttl --ontology https://raw.githubusercontent.com/tibonto/aeon/master/aeon.ttl`

Writing to wiki pages:<br/>`ontology2smw --format ttl --ontology https://raw.githubusercontent.com/tibonto/aeon/master/aeon.ttl --write`

Asking for help:<br/>`ontology2smw --help`
```bash
usage: ontology2smw [-h] [-w] [-o ONTOLOGY] [-f {rdf,ttl}] [-v] [-r]


                   ___
                 { . . }
--------------o00---'----00o--
              ontology2SMW
-----------------------------

optional arguments:
  -h, --help            show this help message and exit
  -w, --write           writes the output to wiki or file. Default: False (dry-run).
  -o ONTOLOGY, --ontology ONTOLOGY
                        Ontology file or URI. Default: https://raw.githubusercontent.com/tibonto/aeon/master/aeon.ttl
  -f {rdf,ttl}, --format {rdf,ttl}
                        Ontology format. Default value: ttl
  -v, --verbose         Verbose output. Default: False.
  -r, --report          Save report in file report.txt Default: False.
  -s SETTINGS, --settings SETTINGS
                        Use a wikidetails.yml file in a different location.


```

<!--

**Requirements:**

In virtual environment install requirements `pip install -r requirements.txt`

`python setup.py install`


**Create a build:**

`python setup.py sdist bdist_wheel`
-->

### To write wiki pages
**wikidetails.yml & wiki write access**
* Ensure user your wiki user account belongs to bot group: see wiki page `Special:UserRights`
* Create a bot password in wiki page: `Special:BotPasswords`
* **copy** `wikidetails.template.yml` as `wikidetails.yml` and fill in bot name and password:<br/>
* **give the bot appropriate rights**: basic, editinterface, editpage, editprotected, createeditmovepage, highvolume

The **local test VM**, mentioned in the following section, **sets a bot account for
the Admin user**, so that once the VM is created **you can just run the script against it.**
Details for that wiki, VM, bot username and password are set in `wikidetails.yml`



### Try on local Virtual Machine
In order to test ontology2smw in action in a isolated virtual
environment, the repository includes a Ansible playbook which creates a VM with Mediawiki installed, and also creates a Bot account for wiki user Admin.

The playbook sets Mediawiki with:
* URL: http://192.168.100.100/w
* SemanticMediawiki extension
* bot account for Admin, with details (in wikidetail.yml):
   * wiki user: Admin
   * wiki user password: adminpassword
   * wiki bot: Admin@ontology2smwbot
   * wiki bot password: botpasswordbotpasswordbotpassword


Requirements:
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* [Ansible](https://www.ansible.com/)

**Create VM:**
```bash
cd vm
vagrant up
ansible-playbook playbook_mw.yml
```
Once tests are done you can either,
* suspend the VM: `vagrant suspend` so it can be reused from the state it was left in with `vagrant up`
* destroy it: `vagrant destroy`


## Develop

```bash
git clone https://github.com/TIBHannover/ontology2smw.git
cd ontology2smw
# (optional) create and activate a virtual-environment
pip install -r requirements.txt
python -m ontology2smw
```

## Test

**Tox:** automated testing on py36, py37, py38
`tox -p all -v`

* pytest
* flake8s
* test coverage report


**pytest**
* without running target VM running Mediawiki + SMW `pytest -m "not smw"`
* with VM running Mediawiki + SMW `pytest` for all the tests
