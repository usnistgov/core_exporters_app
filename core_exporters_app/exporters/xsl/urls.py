""" XSLT exporter url
"""

from django.urls import re_path

from core_exporters_app.exporters.xsl.views.admin import ajax as user_ajax

urlpatterns = [
    re_path(r'^add', user_ajax.add_xslt,
            name='core_exporters_app_exporters_xsl_selection'),
]
