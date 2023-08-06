tornado-http-auth
=================

.. class:: no-web no-pdf

|pypi| |license|


Digest and basic authentication for the Tornado_ web framework. Based on code
and ideas from Twisted's cred_.


Installation
------------

The latest stable version of tornado-ansi-markup can be installed from pypi:

.. code-block:: bash

  $ pip install tornado-http-auth


Usage
-----

.. code-block:: python

  import tornado.ioloop
  from tornado.web import RequestHandler, Application
  from tornado_http_auth import DigestAuthMixin, BasicAuthMixin, auth_required

  credentials = {'user1': 'pass1'}

  class MainHandler(DigestAuthMixin, RequestHandler):
      @auth_required(realm='Protected', auth_func=credentials.get)
      def get(self):
          self.write('Hello %s' % self._current_user)

  app = Application([
      (r'/', MainHandler),
  ])

  app.listen(8888)
  tornado.ioloop.IOLoop.current().start()

  # curl --digest user1:pass1 -v http://localhost:8888  -> 200 OK
  # curl --digest user2:pass2 -v http://localhost:8888  -> 401 Unauthorized


License
-------

This project is released under the terms of the `Apache License, Version 2.0`_.


.. |pypi| image:: https://img.shields.io/pypi/v/tornado-http-auth.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/tornado-http-auth
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/pypi/l/tornado-http-auth.svg?style=flat-square&label=license
    :target: https://pypi.python.org/pypi/tornado-http-auth
    :alt: Apache License, Version 2.0.

.. _cred: https://twistedmatrix.com/documents/15.4.0/core/howto/cred.html
.. _Tornado: http://www.tornadoweb.org/en/stable/
.. _`Apache License, Version 2.0`: https://raw.github.com/gvalkov/tornado-http-auth/master/LICENSE
