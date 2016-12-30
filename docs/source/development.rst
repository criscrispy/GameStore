Development
===========

Setup
-----
1) Install supported *Python interpreter* versions. If using Ubuntu you can use command

  .. code-block:: bash

     sudo apt-get install python3.5

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


- Tox
- Setuptools


Documenting
-----------


Resources
---------

http://engineroom.trackmaven.com/blog/using-pytest-with-django/
http://erik.io/blog/2014/09/11/why-and-how-test-coverage-100/
https://wikis.utexas.edu/display/~bm6432/Django+and+Pytest+Testing
