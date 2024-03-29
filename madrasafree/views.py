#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from edxmako.shortcuts import render_to_response
from django.urls import reverse

import requests

from madrasafree.models import ExtraInfo


@login_required
def registration_completed(request):
    context = {
        'user': request.user,
    }
    return render_to_response('madrasafree/registration_completed.html', context, request=request)


@login_required
def icredit_payment_success(request):
    context = {
        'user': request.user,
    }
    extra_info = request.user.extrainfo
    extra_info.support_is_donor = True
    extra_info.support_payment_response = request.GET.get('Token')
    extra_info.save()
    return render_to_response('madrasafree/icredit_payment_success.html', context, request=request)


@login_required
def donate(request):
    context = {
        'user': request.user,
    }
    return render_to_response('madrasafree/donate.html', context, request=request)


@login_required
def donate_success(request):
    context = {
        'user': request.user,
    }
    return render_to_response('madrasafree/donate_success.html', context, request=request)


@login_required
@csrf_exempt
@require_POST
def icredit_get_url(request):
    user = request.user
    amount = request.POST.get('Item[UnitPrice]')
    try:
        extra_info = request.user.extrainfo
    except ExtraInfo.DoesNotExist:
        extra_info = ExtraInfo(
            user=request.user,
        )
    extra_info.support_amount = amount
    data = {
        'GroupPrivateToken': settings.ICREDIT_GROUP_PRIVATE_TOKEN,
        'Items': [{
            'Quantity': '1',
            'UnitPrice': amount,
            'Description': '',
        }],
        'RedirectURL': settings.LMS_ROOT_URL + reverse('donate_success'),
        'EmailAddress': user.email,
        'CustomerFirstName': user.first_name,
        'CustomerLastName': user.last_name,
    }

    if request.POST.get('CreateRecurringSale'):
        data['SaleType'] = 2
        data['CreateRecurringSale'] = True
        data['RecurringSaleAutoCharge'] = True
        data['RecurringSaleDay'] = 15
        data['RecurringSaleCycle'] = 3
        data['RecurringSaleStep'] = 1
        data['RecurringSaleCount'] = 0
        extra_info.support_is_periodical = True
        data['Items'][0]['Description'] = 'תמיכה חודשית במדרסה'
    else:
        data['SaleType'] = 1
        extra_info.support_is_periodical = False
        data['Items'][0]['Description'] = 'תמיכה חד פעמית במדרסה'

    extra_info.save()
    response = requests.post(
        '{}PaymentPageRequest.svc/GetUrl'.format(settings.ICREDIT_API_URL),
        headers={
            'User-Agent': 'PostmanRuntime/7.26.8',
        },
        json=data,
    )
    url = '"{}"'.format(response.json()['URL'])
    return HttpResponse(url)
