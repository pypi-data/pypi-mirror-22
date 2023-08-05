schul-cloud-url-crawler
=======================

.. image:: https://travis-ci.org/schul-cloud/url-crawler.svg?branch=master
   :target: https://travis-ci.org/schul-cloud/url-crawler
   :alt: Build Status

.. image:: https://badge.fury.io/py/schul-cloud-url-crawler.svg
   :target: https://pypi.python.org/pypi/schul-cloud-url-crawler
   :alt: Python Package Index

This crawler fetches ressources from urls and posts them to a server.

Purpose
-------

The purpose of this crawler is:

- We can provide test data to the API.
- It can crawl ressources which are not active and cannot post.
- Other crawl services can use this crawler to upload their conversions.
- It has the full crawler logic but does not transform into other formats.

  - Maybe we can create recommendations or a library for crawlers from this case.

Requirements
------------

The crawler should work as follows:

- Provide urls

  - as command line arguments
  - as a link to a file with one url per line
  
- Provide ressources_

  - as one ressource in a file
  - as a list of ressources

The crawler must be invoked to crawl.

Example
~~~~~~~

This example gets a ressource from the url and post it to the api.

.. code:: shell

    python3 -m ressource_url_crawler http://localhost:8080 \
            https://raw.githubusercontent.com/schul-cloud/ressources-api-v1/master/schemas/ressource/examples/valid/example-website.json
            
Authentication
~~~~~~~~~~~~~~

You can specify the authentication_ like this:

- ``--basic=username:password`` for basic authentication
- ``--apikey=apikey`` for api key authentication

Further Requirements
--------------------

- **The crawler does not post ressources twice.**
  This can be implemented by
  
  - caching the ressources locally, to see if they changed
  
    - compare ressource
    - compare timestamp
    
  - removing the ressources from the database if they are updated after posting new ressources.
  
This may require some form of state for the crawler.
The state could be added to the ressources in a ``X-Ressources-Url-Crawler-Source`` field.
This allows local caching and requires getting the objects from the database.

.. _ressources: https://github.com/schul-cloud/ressources-api-v1#ressources-api
.. _authentication: https://github.com/schul-cloud/ressources-api-v1#authorization
