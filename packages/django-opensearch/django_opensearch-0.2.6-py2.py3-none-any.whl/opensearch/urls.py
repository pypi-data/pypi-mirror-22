# -*- coding: utf-8 -*-

# django-opensearch
# opensearch/urls.py

from __future__ import unicode_literals

from django.conf.urls import (
    patterns,
    url,
)

__all__ = [
    "urlpatterns",
]

# opensearch urls
urlpatterns = patterns("opensearch.views",
    url(r"^opensearch\.xml$", "opensearch", name="opensearch"),  # opensearch
)
