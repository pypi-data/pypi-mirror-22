==============
Django EnvConf
==============

.. image:: https://travis-ci.org/achedeuzot/django-envconf.svg?branch=master
    :target: https://travis-ci.org/achedeuzot/django-envconf.svg?branch=master

.. image:: https://coveralls.io/repos/github/achedeuzot/django-envconf/badge.svg?branch=master
    :target: https://coveralls.io/github/achedeuzot/django-envconf?branch=master


Django EnvConf allows you to configure your application using environment variables
as recommended by the 12factor methodology.

Shamelessly forked & updated from https://github.com/joke2k/django-environ

-----------
Quick start
-----------

1. Add "envconf" at the top of your ``settings.py`` file like so:

.. code-block:: python

    from envconf import Env
    env = Env(  # Set default values and casting
        DEBUG=(bool, False)
    )
    env.read_env()  # Tries to read the `.env` file which is next to the `manage.py` script.
                    # It's probably better to give the path to be sure it'll read the correct file.


2. Create a ``.env`` file at the root of your project

.. code-block:: shell

    DEBUG=on  # or off / false
    # DJANGO_SETTINGS_MODULE=myapp.settings.dev
    SECRET_KEY=Tom-Marvolo-Riddle
    DATABASE_URL=psql://user:un-gitted-password@127.0.0.1:8458/database
    # DATABASE_URL=sqlite:////my-local-sqlite.db  # sqlite, notice the 4 slashes. See below for more cases.
    CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
    REDIS_URL=rediscache://127.0.0.1:6379:1?client_class=django_redis.client.DefaultClient&password=un-gitted-password

3. Then fetch the variable you want from the environment in your ``settings.py`` file:


.. code-block:: python

    DEBUG = env('DEBUG')  # Defaults to False
    SECRET_KEY = env('SECRET_KEY')  # Raises ImproperlyConfigured exception if SECRET_KEY is not set
    DATABASES = {
        'default': env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
    }

------------
Installation
------------

Through Pypi

.. code-block:: shell

    (venv)$ pip install django-envconf

Directly from git

.. code-block:: shell

    (venv)$ pip install git+https://github.com/achedeuzot/django-envconf.git
    # or
    (venv)$ git clone https://github.com/achedeuzot/django-envconf.git && cd django-envconf
    (venv)$ python setup.py install

-----
Usage
-----
In your settings or configuration module, first either import the standard parser or a Django schema:

.. code-block:: python

    # Default
    from envconf import Env
    env = Env()

    # Schemas
    from envconf.schemas.django110 import Django110Env as env
    env('DEBUG')  # defaults to False
    # Defaults with the following:
    # DEBUG bool
    # SECRET_KEY str
    # DATABASES extracted from DATABASE_URL to dict()

``env`` can be called two ways:

- Type explicit: ``env('VAR_NAME', cast=bool)``
- Type implicit (see below for supported types): ``env.TYPE('ANOTHER_VAR')``. If type is not specified, it defaults
  to ``str``

Casting explicitly:

.. code-block:: python

    # Environment variable: MAIL_ENABLED=1

    mail_enabled = env('MAIL_ENABLED', cast=bool)
    # OR mail_enabled = env.bool('MAIL_ENABLED')
    assert mail_enabled is True

Casting nested types (lists and dicts):

.. code-block:: python

    # Environment variable: FOO=1,2,3
    foo = env('FOO'), cast=list(int))
    assert foo == [1, 2, 3]

You can also set defaults:

.. code-block:: python

    # Environment variable MAX_ROWS has not been defined
    max_rows = env.int('MAX_ROWS', default=100)
    assert max_rows == 100

There are some convenience methods:
- json (a regular JSON string is expected)
- url (which returns a ``urlparse.ParseResult`` object)

.. code-block:: python

    # Environment variable: DATA={"foo":"bar","baz":true}
    data = env.json('DATA')
    # data = {
    #   "foo": "bar",
    #   "baz": True,
    # }

    # Environment variable: SERVICE=ftp://user:password@example.com/some/path?var=foo
    >>> env.url('SERVICE')
    ParseResult(scheme='ftp', netloc='user:password@example.com',
    path='/some/path', params='', query='var=foo', fragment='')


Proxied Values
==============
An environment value or default can reference another environ value by referring to it with a $ sign.  For example:

.. code-block:: python

    PROXIED_VAL = 'hello'
    TEST_VAL ='$PROXIED_VAL'
    environ('TEST_VAL') == 'hello
    environ('UNKNOWN_VAL', default='$PROXIED_VAL') == 'hello'

Proxy values are resolved by default.  To turn off resolving proxy values
pass ``resolve_proxies=False`` to ``environ``, ``environ.str``, or ``environ.unicode``.

Ex:  ``environ('DJANGO_SECRET_KEY', '$1233FJSIFWR44', resolve_proxies=False)``

If you get an infinite recursion when using environ most likely you have an unresolved and perhaps
unintentional proxy value in an environ string.
For example ``environ('DJANGO_SECRET_KEY', '$1233FJSIFWR44')`` will cause an infinite
recursion unless you add ``resolve_proxies=False``.

This is very useful in environment such as Heroku. That way, if you
change your mind later on, you just need to change the configuration (see below) and not your code.

.. code-block:: python

    # Environment variables: MAILGUN_SMTP_LOGIN=foo,
    # SMTP_LOGIN='$MAILGUN_SMTP_LOGIN'

    smtp_login = env('SMTP_LOGIN')
    assert smtp_login == 'foo'

    # Change of mind
    # Environment variales: MANDRILL_SMTP_LOGIN=bar
    # SMTP_LOGIN='$MANDRILL_SMTP_LOGIN'
    smtp_login = env('SMTP_LOGIN)  # Look ma', no hands !
    assert smtp_login == 'bar'


Supported Types
===============
- str
- bool
- int
- float
- json
- list as CSV (FOO=a,b,c)
- tuple (FOO=(a,b,c))
- dict (dict (BAR=key=val,foo=bar)  # envconf.Env(BAR=(dict, {}))
- dict (BAR=key=val;foo=1.1;baz=True)  # envconf.Env(BAR=(dict(value=unicode, cast=dict(foo=float,baz=bool)), {}))
- url
- path (environ.Path)
- db_url

  - PostgreSQL: postgres://, pgsql://, psql:// or postgresql://
  - PostGIS: postgis://
  - MySQL: mysql:// or mysql2://
  - MySQL for GeoDjango: mysqlgis://
  - SQLITE: sqlite:// (sqlite://:memory: for in-memory database, or sqlite:////file/path [4 slashes !])
  - SQLITE with SPATIALITE for GeoDjango: spatialite://
  - Oracle: oracle://
  - LDAP: ldap://
- cache_url

  - Dummy: dummycache://
  - Database: dbcache://
  - File: filecache://
  - Memory: locmemcache://
  - Memcached: memcache://
  - Python memory: pymemcache://
  - Redis: rediscache://
- search_url

  - ElasticSearch: elasticsearch://
  - Solr: solr://
  - Whoosh: whoosh://
  - Xapian: xapian://
  - Simple cache: simple://
- email_url

  - Dummy mail: dummymail://
  - SMTP: smtp://
  - SMTP+SSL: smtp+ssl://
  - SMTP+TLS: smtp+tls://
  - Console mail: consolemail://
  - File mail: filemail://
  - LocMem mail: memorymail://


-----
Tests
-----
Clone the repo and run the tests ;)

.. code-block:: shell

    (venv)$ git clone git@github.com/achedeuzot/django-envconf.git
    (venv)$ cd django-envconf
    (venv)$ python setup.py test

-------
License
-------
Django-envconf is licensed under the BSD License - see the LICENSE file for details


-------------
Compatibility
-------------

Python 2.6, 2.7, 3.3, 3.4, 3.5

Django 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10


-------
Credits
-------

- `django-environ`_ and its contributors & own creditsof course ! Thanks for the awesome package :)

.. _django-environ: https://github.com/joke2k/django-environ

---------
Changelog
---------


0.1.0, 0.2.0, 0.3.* - 12 Sept 2016

- Fork from ``django_environ`` and update of codebase: removal of six dependencly, better oracle support,
  better URL parsing

