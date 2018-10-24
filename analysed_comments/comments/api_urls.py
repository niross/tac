# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from comments.api_views import CommentViewSet

app_name = 'comments_api'
router = routers.DefaultRouter(trailing_slash=True)
router.register(r'', CommentViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
