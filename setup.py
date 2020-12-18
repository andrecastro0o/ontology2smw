from setuptools import setup
from pathlib import Path

README_path = Path.cwd() / 'README.md'
with open(README_path, 'r') as README_f:
    README = README_f.read()

setup(
    name='ontology2smw',
    version='0.1.0',
    packages=['ontology2smw'],
    include_package_data=True,
    license='GPLv3',
    author='Andre Castro',
    author_email='andre.castro@tib.eu',
    description='Automates RDF ontology import into Semantic Mediawiki',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent", ],
    keywords='Semantic Mediawiki Ontology RDF SPARQL',
    url="https://github.com/TIBHannover/ontology2smw",
    python_requires='>=3.6',
    install_requires=[
        'pyparsing==2.4.7',  # rdflib requiores  pyparsing at version 2.4.7
        'rdflib',
        'PyYAML >= 5.3.1',
        'Jinja2 >= 2.11.2',
        'mwclient >= 0.10.1'],
    test_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ontology2smw = ontology2smw.__main__:main'
        ]
    })
