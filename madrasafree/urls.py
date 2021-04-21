from django.conf.urls import url
from .views import icredit_get_url, registration_completed, icredit_payment_success, donate, donate_success

urlpatterns = [
    url(r'^registration_completed/$', registration_completed, name='registration_completed'),
    url(r'^payment_success/$', icredit_payment_success, name='icredit_payment_success'),
    url(r'^donate/$', donate, name='donate'),
    url(r'^donate_success/$', donate_success, name='donate_success'),
    url(r'^icredit_get_url/$', icredit_get_url, name='icredit_get_url'),
]
