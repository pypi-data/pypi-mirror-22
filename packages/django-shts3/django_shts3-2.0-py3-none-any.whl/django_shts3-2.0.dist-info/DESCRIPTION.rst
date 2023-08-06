Django shortcuts
================

You spend too much time typing ``python manage.py``.

Usage
-----

Django shortcuts installs ``django``, ``dj``, ``d`` binaries that proxies
Django's ``manage.py``  scripts.

::

    $ django <command or shortcut>

    $ cd any/project/subdirectory
    $ d <command or shortcut>


Shortcuts
---------

::

  # Django
    'c'  : 'collectstatic',
    'r'  : 'runserver',
    'sp' : 'startproject',
    'sa' : 'startapp',
    't'  : 'test',

    # Shell
    's'  : 'shell',
    'sh' : 'shell',

    # Auth
    'csu': 'createsuperuser',
    'cpw': 'changepassword',

    # Migrations
    'm'  : 'migrate',
    'mg' : 'migrate'
    'mkm' : 'makemigrations',

If in directory with manage.py exists file .django_shts3, commands are loaded from it. They overwrite default commands. File format is `alias @@@ command` e.g. `rs @@@ runserver 0.0.0.0:8000`.

Installation
------------

::

    $ pip3 install django-shts3


