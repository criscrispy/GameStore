Development
===========

Setup
-----
1) Install supported *Python interpreter* versions with ``python-dev``. If using Ubuntu you can use command

  .. code-block:: bash

     sudo apt-get install python3.5 python3.5-dev

2) Install *Virtualenv* for creating isolated Python environments.

  .. code-block:: bash

     pip install virtualenv

  To create an environment and install project requirements use command in project root directory ``wsdproject/``

  .. code-block:: bash

     virtualenv -p /usr/bin/python3.5 ENV
     source ENV/bin/activate
     pip install -r requirements.txt

  To deactivate the environment

  .. code-block:: bash

     deactivate

3) Install Postgre SQL

  .. code-block:: bash

     sudo apt-get install postgresql postgresql-contrib

  .. note::

     TODO: Setup instructions


Django Checklist
----------------
.. note::

   To be written

To implement a feature in django application

- Templates
- Views
- Urls
- Docstring
- Logging
- Models
- Migrations
- Tests


Frontend
--------
Frontend packages are downloaded and managed using package managers ``npm`` and ``bower``.

- NPM (Node Package Manager)

  `Install NodeJs <https://nodejs.org/en/download/>`_

  .. code-block:: bash

     npm install <package>

- Bower, a package manager for front-end packages.

  .. code-block:: bash

     npm install -g bower

  Then you can use

  .. code-block:: bash

     bower install <package>

- Gulp, javascript automation tool. It can be installed through ``npm``

  .. code-block:: bash

     npm install gulp

  Task are written into the ``gulpfile.js`` and ``gulpfile.coffee``.


Testing
-------
- Pytest

   .. code-block:: bash

      pytest

- Hypothesis
- pytest-xdist
- Mock

- Coverage
- pytest-cov

- Tox is virtual environment manager that can be used to run tests against multiple python environments. Environments are specified in ``tox.ini``.

  Test against all environments can be run with command

  .. code-block:: bash

     tox

  Test against specific environment can be run with

  .. code-block:: bash

     tox -e py35

- Setuptools


Documenting
-----------


Resources
---------

http://engineroom.trackmaven.com/blog/using-pytest-with-django/
http://erik.io/blog/2014/09/11/why-and-how-test-coverage-100/
https://wikis.utexas.edu/display/~bm6432/Django+and+Pytest+Testing
