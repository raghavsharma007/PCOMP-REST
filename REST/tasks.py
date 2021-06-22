from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import TestData

@shared_task
def multifunc_post(test_data):
    for i in test_data:
        TestData.objects.create(column1=i['column1'], column2=i['column2'], column3=i['column3'],  column4=i['column4'],  column5=i['column5'], column6=i['column6'], column7=i['column7'], column8=i['column8'], column9=i['column9'], column10=i['column10'])
    return None