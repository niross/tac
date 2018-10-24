from django.conf.urls import url
from django.urls import include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Analysed Comments API')

urlpatterns = [
    url(r'^$', schema_view),
    url(
        r'api/',
        include(
            'comments.api_urls',
            namespace='comments-api'
        )
    ),

]
