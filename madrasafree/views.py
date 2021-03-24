from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from edxmako.shortcuts import render_to_response, render_to_string
from django.urls import reverse

import requests


@login_required
def registration_completed(request):
    return render_to_response('madrasafree/registration_completed.html')


@login_required
def icredit_payment_success(request):
    return render_to_response('madrasafree/icredit_payment_success.html')


@login_required
@csrf_exempt
@require_POST
def icredit_get_url(request):
    user = request.user
    response = requests.post(
        '{}PaymentPageRequest.svc/GetUrl'.format(settings.ICREDIT_API_URL),
        headers={
            'User-Agent': 'PostmanRuntime/7.26.8',
        },
        json={
            'GroupPrivateToken': settings.ICREDIT_GROUP_PRIVATE_TOKEN,
            'Items': [{
                'CatalogNumber': '1',
                'Quantity': '1',
                'UnitPrice': request.POST.get('Item[UnitPrice]'),
                'Description': '',
            }],
            'RedirectURL': settings.LMS_ROOT_URL + reverse('icredit_payment_success'),
            'EmailAddress': user.email,
            'CustomerFirstName': user.first_name,
            'CustomerLastName': user.last_name,
        }
    )
    url = '"{}"'.format(response.json()['URL'])
    return HttpResponse(url)
