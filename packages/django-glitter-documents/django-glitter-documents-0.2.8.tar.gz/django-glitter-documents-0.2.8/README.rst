Django Glitter Documents
========================

The Document handler for `Glitter <https://github.com/developersociety/django-glitter/>`_ you've
been waiting for.


Getting Started
---------------

Installation is simple using ``pip``:

.. code-block:: console

    $ pip install django-glitter-documents

Add ``glitter_documents`` to your site's ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'glitter_documents',
        ...
    ]

And finally, remember to run the migrations:

.. code-block:: console

    $ ./manage.py migrate


Developing
----------

Getting started on improving Django Glitter Documents is pretty straight forward. Presuming you're
using `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ and
`The Developer Society Dev Tools <https://github.com/developersociety/tools>`_:

.. code-block:: console

    $ dev-clone git@github.com:developersociety/django-glitter-documents.git
    $ make reset

Please remember to run ``make format`` before you commit, and ``tox`` before pushing the changes you
make:

.. code-block:: console

    $ make format
    $ git add .
    $ git commit -m 'Made it do something awesome!'
    $ tox
    $ git push



Releasing
---------

Releasing a new version of the project to PyPi is fairly straight forward.

First, make sure you have the correct credentials for PyPi correctly configued on your machine.

Update and commit the Version History in the README.

Then, use ``bumpversion`` to increment the version numbers in the project. This will also create a
commit and a tag automatically for the new version. For example, to increment the version numbers
for a 'patch' release:

.. code-block:: console

    $ bumpversion patch
    $ git push --tags origin master

``bumpversion`` can increment 'patch', 'minor' or 'major' version numbers:

.. code-block:: console

    $ bumpversion [patch | minor | major]

Then release the new version to PyPi:

.. code-block:: console

    $ make release


Version History
---------------

0.2.5
~~~~~

Added Makefile for linting, beautficiation and easier PyPi releasing.
https://github.com/developersociety/django-glitter-documents/pull/18

0.2.4
~~~~~

Added "View on site" link to list of documents.
https://github.com/developersociety/django-glitter-documents/pull/16


0.2.3
~~~~~

Add file extension method to model.
https://github.com/developersociety/django-glitter-documents/pull/13
