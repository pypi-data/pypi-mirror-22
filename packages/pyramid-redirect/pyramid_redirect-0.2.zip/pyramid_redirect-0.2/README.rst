pyramid_redirect
================

------------
Introduction
------------

pyramid_redirect is a small extension for `Pyramid <http://www.pylonsproject.org/>`_ to redirect urls before further processing takes place.

------------
Installation
------------

Just do

``pip install pyramid_redirect``

or

``easy_install pyramid_redirect``

-------------
Compatibility
-------------

pyramid_redirect runs with pyramid>=1.3 and python>=2.7 and python>=3.5.
Other versions might also work.

-------------
Documentation
-------------

Usage example::

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_redirect')
        # add url redirecting rules...
        #   first parameter is a regular expression
        #   second parameter is the target url
        config.add_redirect_rule(r'http://example\.com/favicon.ico', r'http://example.com/static/favicon.ico')
        config.add_redirect_rule(r'http://example\.com/gallery/(?P<subpath>.*)',
                                r'http://example.com/root/%(subpath)s')
        #
        # ... rest of configuration
        #
        # return WSGI application instance
        return config.make_wsgi_app()

See tests for more examples.

If you use structlog, add the following configuration setting to your INI file to enable structlog-like logging::

    pyramid_redirect.structlog = true

