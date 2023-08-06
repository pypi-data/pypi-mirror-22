Resyndicator
============

This documentation is best viewed on https://resyndicator.readthedocs.io/.

Purpose
-------

The Resyndicator is a Python 3 framework for aggregating data from various
sources into Atom feeds. If you have a list of a couple hundred data
sources – such as feeds, sitemaps, and Twitter users – and want to share the aggregate of those
entries between your various devices (computers, phones, etc.), your
colleagues, or even the visitors of your website, then that’s just what
the Resyndicator is for.

- It can obtain data from feeds, sitemaps, social media, and any other sources you implement.
- It allows for queries as sophisticated as SQLAlchemy allows to filter
  your aggregate feed.
- It allows you to subclass the fetchers easily, so you can write fetchers for
  endpoints as obscure as Adobe’s AMF.
- It keeps all entries in Postgres, so you have a backup.

I’ve been using the Resyndicator for the `EA Foundation <https://ea-stiftung.org/>`_, `.impact <http://dotimpact.im/>`_, `Saram <http://www.saram-ev.de/>`_, `Derpy News <http://derpynews.com/>`_, and `Ferret Go <http://www.ferret-go.com/>`_, and a marketing department of Logitech also indicated interest at one point.

Setup
-----

I’ve created a `sample implementation <https://bitbucket.org/Telofy/samplefeeder/src>`_ of the Resyndicator framework to facilitate the setup process. You can fork it and adapt it for your purposes. (I’ve been following the convention of calling my implementations “soandsofeeder” – a word ending in “feeder” with no hyphen or space in between.) The `Resyndicator is hosted on PyPI <https://pypi.python.org/pypi/resyndicator>`_, so you can just install it through pip.

- One important file is `samplefeeder/settings.py <https://bitbucket.org/Telofy/samplefeeder/src/master/samplefeeder/settings.py>`_ with some general settings. For the defaults see `resyndicator/settings.py <https://bitbucket.org/Telofy/resyndicator/src/master/resyndicator/settings.py>`_.
- The other is `samplefeeder/resources.py <https://bitbucket.org/Telofy/samplefeeder/src/master/samplefeeder/resources.py>`_.

Settings
~~~~~~~~

In ``settings.py``, you’ll in particular need to change your database credentials with something like
``DATABASE = 'postgresql://foo:bar@localhost/samplefeeder'`` (you may
need to create the database and grant access rights to the user). I haven’t tested it with anything other than Postgres.

For
more options, see `resyndicator/settings.py <https://bitbucket.org/Telofy/resyndicator/src/master/resyndicator/settings.py>`_.

Note: You can create the database like so::

    create role samplefeeder with password 'samplefeeder' login;
    create database samplefeeder with owner samplefeeder;

My system automatically creates it with UTF-8 encoding, but some Debian systems package a version of
Postgres that uses some weird encoding by default. In that case make sure to inherit from the right template.

::

    postgres=# \l
                                                     List of databases
               Name           |     Owner      | Encoding  |   Collate   |    Ctype    |       Access privileges
    --------------------------+----------------+-----------+-------------+-------------+-------------------------------
     postgres                 | postgres       | UTF8      | en_DK.UTF-8 | en_DK.UTF-8 |
     samplefeeder             | samplefeeder   | UTF8      | en_DK.UTF-8 | en_DK.UTF-8 |


Resources
~~~~~~~~~

In ``resources.py``, you list the feeds and (eponymous) resyndicators
like so for example::

    from datetime import timedelta
    from sqlalchemy.sql import or_
    from resyndicator import settings
    from resyndicator.models import Entry
    from resyndicator.fetchers import (
        FeedFetcher, SitemapIndexFetcher, SitemapFetcher,
        TwitterFetcher, ContentFetcher)
    from resyndicator.resyndicators import Resyndicator
    from . import settings

    CONTENT_FETCHERS = [
        ContentFetcher(past=settings.PAST, timeout=10)
    ]

    RESYNDICATORS = [
        Resyndicator(
            title='Effective Altruism',
            past=PAST,
            query=or_(
                Entry.source_link.in_([
                    'http://feeds.feedburner.com/TheGivewellBlog',
                    'http://www.openphilanthropy.org/sitemap.xml',
                ])
            )
        )
    ]

    FETCHERS = [
        FeedFetcher('http://feeds.feedburner.com/TheGivewellBlog',
                    interval=10*60),
        SitemapFetcher('http://www.openphilanthropy.org/sitemap.xml',
                       defaults={'title': 'Open Phil Sitemap',
                                 'author': 'Open Philanthropy Project'},
                       interval=30*60),
    ]

    STREAMS = [
        TwitterFetcher(
            oauth_token=settings.OAUTH_TOKEN,
            oauth_secret=settings.OAUTH_SECRET,
            interval=5*60),
    ]

Samplefeeder contains a working sample ``resources.py`` that you can adapt. It is missing the
sample TwitterFetcher so it does not expose the OAuth secret.

For each resyndicator, you define a query and a title which will
determine its ID and thus its identity. If you change the title you
create a new, different feed. The query determines the entries of the feed and
is specified as `SQLAlchemy where statements <http://docs.sqlalchemy.org/en/latest/orm/query.html>`_.

To build your Samplefeeder fork, run `make`.

Running It
----------

You can check the `supervisord.conf <https://bitbucket.org/Telofy/samplefeeder/src/master/samplefeeder/supervisord.conf>`_ that is includede with the Samplefeeder for sample invocations.

Note: The Resyndicator requires Python 3 (and I haven’t tested it with versions older than Python 3.4) while Supervisor will only support Python 3 upon version 4.0, so you’ll need two different Pythons to run it this way. (But it’s no problem to run a Python 3 application through Supervisor.)

::

    [program:fetcher]
    command = bin/resyndicator -s samplefeeder.settings fetchers
    ...

    [program:content]
    command = bin/resyndicator -s samplefeeder.settings content
    ...

You can use ``bin/resyndicator -s samplefeeder.settings fetchers --test-mode`` to instruct the Resyndicator to ignore the intervals and fetche all feeds immediately so you don’t have to wait to see if any of them malfunction.

Serving the Feeds
-----------------

The feeds are written to files in the `webroot/` subdirectory. Point your Nginx or Varnish at this
directory to serve the feeds. An Nginx example::

    server {
        listen 80;
        listen [::]:80;
        server_name feeds.example.com;

        charset utf-8;
        keepalive_timeout 5;
        root /opt/samplefeeder/webroot/;
        access_log /var/log/nginx/feeds.access.log main;
    }

Testing
-------

You can run use pytest to run the tests:

1. ``make`` to install the virtualenv with the Resyndicator and dependencies
2. ``bin/pip install pytest``
3. ``bin/py.test resyndicator``
