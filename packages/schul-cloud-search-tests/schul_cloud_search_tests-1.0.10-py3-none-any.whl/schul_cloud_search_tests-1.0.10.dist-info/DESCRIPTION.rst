schul_cloud_search_tests
========================

.. image:: https://travis-ci.org/schul-cloud/schul_cloud_search_tests.svg?branch=master
   :target: https://travis-ci.org/schul-cloud/schul_cloud_search_tests
   :alt: Build Status

.. image:: https://badge.fury.io/py/schul-cloud-search-tests.svg
   :target: https://pypi.python.org/pypi/schul-cloud-search-tests
   :alt: Python Package Index

.. image:: https://img.shields.io/docker/build/schulcloud/schul_cloud_search_tests.svg
   :target: https://hub.docker.com/r/schulcloud/schul_cloud_search_tests/builds/
   :alt: Dockerhub Automated Build Status

.. image:: http://firsttimers.quelltext.eu/repository/schul-cloud/schul_cloud_search_tests.svg
   :target: http://firsttimers.quelltext.eu/repository/schul-cloud/schul_cloud_search_tests.html
   :alt: First Timers

These are the tests for the Schul-Cloud search API.
You can read `motivation blog post`_ about

- common tests for all search engines
- testing during live deployment

Installation
------------

You can install the tests by installing Python_ version 3 and ``pip``.
Then, you run the installation from the command line:

.. code:: shell

    pip install --user schul-cloud-search-tests

Installation for Development
----------------------------

If you would like to contribute code to this repository, you can clone it first.

.. code:: shell

    git clone https://github.com/schul-cloud/schul_cloud_search_tests.git
    cd schul_cloud_search_tests

Install the required packages for Python_:

.. code:: shell

    pip3 install --user -r requirements.txt pip-tools==1.6.5

Note that if you would like to change the requirements, please edit the
``requirements.in`` file and run this command to update the dependencies:

.. code:: shell

    pip-compile --output-file requirements.txt requirements.in

Specification
-------------

The idea is that these tests run in between your search client and your
search engine or search adapter.
You use the test interface instead of your search engine interface to 
run checks on every request the client makes:

- Is the client request formulated correctly?
- Is the server response folmulated correctly?

These cases can be defined and are defined:

- When the client issues a successful request and the server responds correctly,
  the request is forwarded, optionally including a note that the tests passed.
- When the client issues a malformed request, HTTP error ``555`` is returned
  including the information which tests did not pass.
  The request is not forwarded to the server.
  To verify this, the client request is included in the reponse.
- When the client issues a correct request, and the server response is malformed,
  then HTTP error ``556`` is returned including a list of error descriptions
  of the mistakes made by the server. To verify this, also the server response
  is included in the errors.

Usage
-----

Suppose you have a server running on http://localhost:1234/v1/search/.
You can tun the search engine tests as a proxy on port 8080 like this:

.. code:: shell

    python3 -m schul_cloud_search_tests.proxy 8080 /endpoint/ http://localhost:1234/v1/search/

Now, all your requests to http://localhost:8080/endpoint/ will be forwarded to 
http://localhost:1234/v1/search/.

When you are done, you can visit http://localhost:8080/stop to stop the server
or run this command:

.. code:: shell

    python3 -m schul_cloud_search_tests.stop 8080

The return code is zero (success) if all tests of all requests passed.
If one test fails, it is a number greater than zero.


Further Reading
---------------

- `Readme Driven Development`_

------------------------------

You can edit this document `on Github
<https://github.com/schul-cloud/schul_cloud_search_tests/blob/master/README.rst#readme>`__
and check it with `this editor <http://rst.ninjs.org/>`__.

.. _Readme Driven Development: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html
.. _motivation blog post: https://schul-cloud.github.io/blog/2017-06-08/search-api-specification
.. _Python: https://python.org

