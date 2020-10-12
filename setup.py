from setuptools import setup
from pathlib import Path

README_path = Path.cwd() / 'README.md'
with open(README_path, 'r') as README_f:
    README = README_f.read()

setup(
    name='ontology2smw',
    version='0.0.1',
    packages=['ontology2smw'],
    license='GPLv3',
    author='Andre Castro',
    author_email='andre.castro@tib.eu',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3.7'],
    keywords='Semantic Mediawiki Ontology RDF SPARQL',
    install_requires=['rdflib', 'pyyaml', 'Jinja2', 'mediawikitools'],
    test_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ontology2smw = ontology2smw.__main__:main'
        ]
    })