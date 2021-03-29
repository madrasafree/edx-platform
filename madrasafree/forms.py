# coding=utf-8
from .models import ExtraInfo
from django.forms import ModelForm, BooleanField


class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    support_is_donor = BooleanField(
        required=False,
        label='אני רוצה לתמוך במיזם ובתנועה',
    )

    class Meta:
        model = ExtraInfo
        fields = ('support_is_donor',)
