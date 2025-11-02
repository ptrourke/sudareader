# SudaReader

An application to extract Suda information from static Suda On Line pages and format them as json files (_suda-extract_),
preliminary to ingesting them into a search engine.

The ultimate plan is to implement a SOLR or OpenSearch search engine (suda-index) with a Flask front end for search and results
display (suda-search).  Future work on allowing further edits to the SOL lemmata is under consideration.

This is a private project of Patrick T. Rourke, and is not work for any institutions that employ him, or for the 
Stoa Consortium. Licensing to be determined.

Work began during the lapse of appropriations of 2025.

Current Tools:

* betacode_converter
* suda_extract

Planned Tools:

* suda-index
* suda-search
