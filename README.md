# core_exporters_app

core_exporters_app is a Django app.

# Quick start

1. Add "core_exporters_app" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
  ...
  'core_exporters_app',
]
```

2. Include the core_exporters_app URLconf in your project urls.py like this::

```python
  url(r'^exporter/', include("core_exporters_app.urls")),
```
