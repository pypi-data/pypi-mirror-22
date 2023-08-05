chembl_extras
======


.. image:: https://img.shields.io/pypi/v/chembl_extras.svg
    :target: https://pypi.python.org/pypi/chembl_extras/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/chembl_extras.svg
    :target: https://pypi.python.org/pypi/chembl_extras/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/pyversions/chembl_extras.svg
    :target: https://pypi.python.org/pypi/chembl_extras/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/chembl_extras.svg
    :target: https://pypi.python.org/pypi/chembl_extras/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/chembl_extras.svg
    :target: https://pypi.python.org/pypi/chembl_extras/
    :alt: License
    
.. image:: https://badge.waffle.io/chembl/chembl_extras.png?label=ready&title=Ready 
 :target: https://waffle.io/chembl/chembl_extras
 :alt: 'Stories in Ready'    

This is chembl_extras package developed at Chembl group, EMBL-EBI, Cambridge, UK.

This package provides two django custom migration commands:

    * generate_ora2pg_conf - generates configuration file for ora2pg (http://ora2pg.darold.net/) script based on given model.
    * generate_backbone_models - not implemented yet

Additionally, the package defines MoleculeFinder class which uses biopython suffix trie to index Inchies and search them by fragments.
It also provides Ontology (and derivatives) class to model different ontologies for future use.
