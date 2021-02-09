from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import requests

@csrf_exempt
@require_POST
def icredit_get_url(request):
    response = requests.post(
        '{}PaymentPageRequest.svc/GetUrl'.format(settings.ICREDIT_API_URL),
        headers={
            'User-Agent': 'PostmanRuntime/7.26.8',
        },
        json={
            'GroupPrivateToken': settings.ICREDIT_GROUP_PRIVATE_TOKEN,
            'Items': [{
                'CatalogNumber': 'XXX',
                'Quantity': '1',
                'UnitPrice': '1',
                'Description': '1',
            }],
            'RedirectURL': settings.LMS_ROOT_URL,
            'EmailAddress': request.POST.get('email'),
            'CustomerFirstName': '',
            'CustomerLastName': '',
        }
    )
    url = response.json()['URL']
    return HttpResponse(url)
