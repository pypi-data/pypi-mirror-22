===================
Django Glitter News
===================


Adds easy to use News/Blog functionality to
`Glitter <https://github.com/developersociety/django-glitter/>`_.


Installation
============

Getting the code
----------------

You can get **django-glitter-news** by using **pip**:

.. code-block:: console

    $ pip install django-glitter-news

Prerequisites
-------------

Make sure you add ``'glitter_news'``, ``'taggit'`` and ``'adminsortable'`` to your
``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'glitter_news',
        'taggit',
        'adminsortable',
        # ...
    ]

URLconf
-------

Add the Glitter News URLs to your project’s URLconf as follows:


.. code-block:: python

    url(r'^news/', include('glitter_news.urls', namespace='glitter-news'))


Configuration
=============

The following options can be set in your project's `settings.py`:

GLITTER_NEWS_TAGS
-----------------

This setting enables tags for the model ``Post`` in your project.

Default is ``False``.

Example:

.. code-block:: python
    GLITTER_NEWS_TAGS = True

NEWS_PER_PAGE
-------------

Set the number of news articles which will be displayed on a page.

Default is ``10``.

Example:

.. code-block:: python
    NEWS_PER_PAGE = 10

NEWS_STICKY_ON_ALL
------------------

Disable the sticky posts functionality when displaying the list of all news.

Default is ``True``.

Example:

.. code-block:: python
    NEWS_STICKY_ON_ALL = False


Developing
==========

Getting started on improving Django Glitter News is pretty straight forward. Presuming you're
using `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ and
`The Developer Society Dev Tools <https://github.com/developersociety/tools>`_:

.. code-block:: console

    $ dev-clone git@github.com:developersociety/django-glitter-news.git
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
=========

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
