==================
Core Exporters App
==================

Exporters for the curator core project.

Quick start
===========

1. Add "core_exporters_app" to your INSTALLED_APPS setting
----------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_exporters_app',
    ]

2. Include the core_exporters_app URLconf in your project urls.py
-----------------------------------------------------------------

.. code:: python

      url(r'^exporter/', include("core_exporters_app.urls")),
