Integration rq with pyramid
===========================

This package makes it possible to use the `RQ <http://python-rq.org/>`_
job queueing library in `Pyramid
<http://www.pylonsproject.org/projects/pyramid/about>`_ applications.
Specifically it does three things:

1. allow configuring the redis connection in your ``.ini``-file 
2. make sure the redis connection used by RQ is appropriate for the
   Pyramid application, even if you are running multiple differently
   configure Pyramid applications within the same process.
3. provide a replacement for the standard RQ worker which runs all
   tasks in a fully configured Pyramid environment.


How to use pyramid_rq
=====================

Using pyramid_rq is very easy. The first thing you need to do is add
``pyramid_rq`` to the list of required packages in your ``setup.py``
file::

    setup(name='my_package',
          ...
          install_requires=['pyramid_rq'],
          ...
          )

After doing this you will need to reinstall/develop your application or, if
you are using buildout, rerun buildout.

The next step is to configure RQ in your application. In your startup code
simply add this line::

    config.include('pyramid_rq')

And that is everything! This will setup a default configuration that
assumes you are using a local redis server.


Configuration
=============

The default configuration assumes that you are using a local redis server
listening on its default port. If your environment is different you can
specify a different configuration in your ``.ini``-file. This is done using
three options:

``rq.redis.host`` or ``redis.host``
   The hostname for the redis server. If not specified defaults to
   ``localhost``.

``rq.redis.port`` or ``redis.port``
   The TCP port used to connect to the redis server. Defaults to 6379.

``rq.redis.db`` or ``redis.db``
   The redis database nmber to use. If not specified this defaults to 1.

All configuration options are available under two keys: either prefixed
by ``rq.redis`` or by ``redis``, prefering the ``rq.redis`` key if
present. This is done to allow using the redis configuration in other
places as well, while also making it possible to use a different redis
configuration for RQ.

