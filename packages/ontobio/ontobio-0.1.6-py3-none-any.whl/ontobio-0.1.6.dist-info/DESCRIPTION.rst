|Build Status| |DOI|

ontobio - a python API for working with ontologies and associations
===================================================================

This module provides objects and utility methods for working with
ontologies and associations of entities (genes, variants, etc) to
ontology classes.

The ontologies and associations can either be local files or provided by
remote services (currently the OntoBee SPARQL service for ontologies and
a Monarch or GO Golr service for associations).

API Docs
========

`ontobio <https://www.pydoc.io/pypi/ontobio-0.1.6/index.html>`__ on
pydoc.io

Command Line
============

See the README in the
`bin <https://github.com/biolink/ontobio/tree/master/bin>`__ directory

Notebooks
=========

See the `Jupyter
Notebooks <http://nbviewer.jupyter.org/github/biolink/ontobio/tree/master/notebooks/>`__
for code examples

Basics
======

There are two ways of initiating an ontology object:

-  via a local obo-json file
-  via remote connections to OBO PURLs
-  via remote query to a SPARQL service (currently ontobee, but soon
   others)

Persistent caching is used (currently cachier) to avoid repeated
expensive I/O connections

This is handled via the `ontol\_manager.py <ontobio/ontol_manager.py>`__
module. This creates an ontology object (see
`ontol.py <ontobio/ontol.py>`__ ).

Note that object modeling is lightweight - we use the python networkx
package for representing the basic graph portion of an ontology. See
also the `obographs <https://github.com/geneontology/obographs>`__ spec.

Associations
============

See the ontobio.golr package

.. |Build Status| image:: https://travis-ci.org/biolink/ontobio.svg?branch=master
   :target: https://travis-ci.org/biolink/ontobio
.. |DOI| image:: https://zenodo.org/badge/13996/biolink/ontobio.svg
   :target: https://zenodo.org/badge/latestdoi/13996/biolink/ontobio


