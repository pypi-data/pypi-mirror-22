=====
Usage
=====

Include the project into pyramid::

    pyramid.includes=
        ...
        pyramid_jinja2_webpack


Or::

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2_webpack')


==========================
Configuring jinja2_webpack
==========================

You can put settings into the ini::

    webpack.manifest=/path/to/manifest.json
    webpack.publicRoot=/static/pack/
    webpack.errorOnInvalidReference=false

================================
Referencing assets from template
================================

In your jinja2 assets you can refer to webpack
entries by URL using the filter syntax::

    {{ 'my-entry': webpack }}

==============================
Referencing assets from python
==============================

You can access the webpack environment from either the
config object::

    webpack_env = config.get_webpack_environment()


Or from the request object::

    webpack_env = request.webpack_environment


You can then query an asset like::

    asset = webpack_env.identify_assetspec('my-entry')
    url = asset.url

=========
More Info
=========

See: `jinja2_webpack <http://jinja2-webpack.readthedocs.io/en/latest/>`_.
