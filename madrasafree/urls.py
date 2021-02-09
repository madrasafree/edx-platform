from django.conf.urls import include, url
from .views import icredit_get_url

urlpatterns = [
    url(r'^icredit_get_url/$', icredit_get_url, name='icredit_get_url'),
]
