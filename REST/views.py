from django.shortcuts import render
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from .models import TestData
import ast
import time
from asgiref.sync import sync_to_async
import numpy as np
import multiprocessing
from django.utils import timezone
import random
import hashlib
from .tasks import multifunc_post, encrypt_db, multifunc_put



# funcion for createinf test data for APIs
def create_data(mtype):
    # initializing emply dictionary
    test_data = {}
    if mtype == 'post':
        # creating random ten series
        for i in range(0, 10):
            data_series = pd.util.testing.rands_array(10, 50)
            test_data[f'column{i+1}'] = data_series
        
        test_data = pd.DataFrame(test_data)
        d = test_data.to_json(orient='records')
        json_test_data = json.loads(d)
        json_test_data = json.dumps(json_test_data, indent=4) # prettyfy json

    if mtype == 'put':
        # creating random ten series
        for i in range(0, 10):
            data_series = pd.util.testing.rands_array(10, 25)
            test_data[f'column{i+1}'] = f'updated_data{i+1}' + '-' + data_series
        
        test_data = pd.DataFrame(test_data)
        d = test_data.to_json(orient='records')
        json_test_data = json.loads(d)
        json_test_data = json.dumps(json_test_data, indent=4) # prettyfy json

    return json_test_data


def view_data(request):
    return None

        
# index page
def index(request):
    context = {}
    return render(request, 'REST/index.html', context)


@csrf_exempt
def post(request):
    # start timer
    startTimer = time.time()

    # calling data
    json_data = create_data('post')

    # POST request
    if request.method == 'POST':
        test_data = request.POST.get('testData') # getting POST data from form
        browzer_check = request.POST.get('checkbrowzer') # check if request coming from brozwer

        # convert string into dict
        test_data = ast.literal_eval(test_data)

        #saving data in database(parallel or simple)
        if 'parallel_post' in request.POST:
            multifunc_post.delay(test_data)
            # multiprocessing_func(test_data, schedule=timezone.now())
        elif 'simple_post' in request.POST:
            for i in test_data:
                TestData.objects.create(column1=i['column1'], column2=i['column2'], column3=i['column3'],  column4=i['column4'],  column5=i['column5'], column6=i['column6'], column7=i['column7'], column8=i['column8'], column9=i['column9'], column10=i['column10'])


        if browzer_check == 'on':
            # return HTML with json
            browzer = True

            endTime = time.time() - startTimer # end timer
            print(endTime)
            context = {'browzer': browzer}
            return render(request, 'REST/result.html', context)
        else:
            # only return json
            browzer = False

            # end timer
            endTime = time.time() - startTimer 
            print(endTime)
            context = {'browzer': browzer}
            return render(request, 'REST/result.html', context)
    

    # context of view
    context = {'json_data': json_data}
    return render(request, 'REST/post.html', context)


@csrf_exempt
def put(request):

    # start timer
    startTimer = time.time()

    # calling data
    json_data = create_data('put')

    # POST request
    if request.method == 'POST':
        test_data = request.POST.get('testData') # getting POST data from form
        browzer_check = request.POST.get('checkbrowzer') # check if request coming from brozwer

        # convert string into dict
        test_data = ast.literal_eval(test_data)

        # updating data in database(parallel or simple)
        if 'parallel_put' in request.POST:
            multifunc_put.delay(test_data)
        elif 'simple_put' in request.POST:
            ids = TestData.objects.values_list('id', flat=True)[:25]
            for index, i in enumerate(test_data):
                TestData.objects.filter(pk=ids[index]).update(column1=i['column1'], column2=i['column2'], column3=i['column3'],  column4=i['column4'],  column5=i['column5'], column6=i['column6'], column7=i['column7'], column8=i['column8'], column9=i['column9'], column10=i['column10'])

        if browzer_check == 'on':
            # return HTML with json
            browzer = True

            endTime = time.time() - startTimer # end timer
            print(endTime)
            context = {'browzer': browzer}
            return render(request, 'REST/result.html', context)
        else:
            # only return json
            browzer = False

            # end timer
            endTime = time.time() - startTimer 
            print(endTime)
            context = {'browzer': browzer}
            return render(request, 'REST/result.html', context)

    
    # context of view
    context = {'json_data': json_data}
    return render(request, 'REST/put.html', context)



# for viewing current data in database table
@csrf_exempt
def dbtable(request):
    # getting all the data from the table
    dbdata = TestData.objects.all()

    if request.method == 'POST':
        # for deleting all the entries in database
        TestData.objects.all().delete()

    if TestData.objects.all().count() > 0:
        encrypt_db.delay()
    context = {'dbdata': dbdata}
    return render(request, 'REST/dbtable.html', context)


# securing REST APIs.(PART-2)

def encrypt(key, msg, num=1):
    encryped = []
    # for j in range(1, num+1):
    for i, c in enumerate(msg):
        key_c = ord(key[i % len(key)])
        msg_c = ord(c)
        encryped.append(chr((msg_c + key_c + num) % 127))
    return ''.join(encryped)

def decrypt(key, encryped, num=1):
    msg = []
    # for j in range(1, num+1):
    for i, c in enumerate(encryped):
        key_c = ord(key[i % len(key)])
        enc_c = ord(c)
        msg.append(chr((enc_c - key_c - int(num)) % 127))
    return ''.join(msg)



def func_decrypter(json_encrypted_data):
    encryption_key = 'encryptionkey1234'
    json_data = []
    json_encrypted_data = ast.literal_eval(json_encrypted_data)
    for i in json_encrypted_data:
        random_encryptionNum = int(i['random_encryptionNum'])
        column1 = decrypt(encryption_key, i['column1'], random_encryptionNum)
        column2 = decrypt(encryption_key, i['column2'], random_encryptionNum)
        column3 = decrypt(encryption_key, i['column3'], random_encryptionNum)
        column4 = decrypt(encryption_key, i['column4'], random_encryptionNum)
        column5 = decrypt(encryption_key, i['column5'], random_encryptionNum)
        column6 = decrypt(encryption_key, i['column6'], random_encryptionNum)
        column7 = decrypt(encryption_key, i['column7'], random_encryptionNum)
        column8 = decrypt(encryption_key, i['column8'], random_encryptionNum)
        column9 = decrypt(encryption_key, i['column9'], random_encryptionNum)
        column10 = decrypt(encryption_key, i['column10'], random_encryptionNum)
        json_data.append({'column1': column1, 'column2': column2, 'column3': column3, 'column4': column4, 'column5': column5, 'column6': column6, 'column7': column7, 'column8': column8, 'column9': column9, 'column10': column10})
        print(json_data)
    return json.dumps(json_data, indent=4)


def testdataSerializer(multi_instance):
    json_data = []
    for i in multi_instance:
        json_data.append({'column1': i.column1, 'column2': i.column2, 'column3': i.column3, 'column4': i.column4, 'column5': i.column5, 'column6': i.column6, 'column7': i.column7, 'column8': i.column8, 'column9': i.column9, 'column10': i.column10, 'random_encryptionNum': i.random_encryptionNum})
    return json.dumps(json_data, indent=4)



def security(request):
    context = {}
    return render(request, 'REST/security.html', context)

def getjsondata(request):
    # multiprocessing_func_encrypter.now('encrypt')
    if TestData.objects.all().count() > 0:
        encrypt_db.delay()

    # POST request
    if request.method == 'POST':
        json_data = testdataSerializer(TestData.objects.all())
        browzer_check = request.POST.get('checkbrowzer') # check if request coming from brozwer


        if browzer_check == 'on':
            # return HTML with json
            browzer = True

            if 'decrypt' in request.POST:
                json_encrypted_data = request.POST.get('testData')
                json_data = func_decrypter(json_encrypted_data)
                data_received = False
                context = {'browzer': browzer, 'json_data': json_data, 'data_received': data_received}
                return render(request, 'REST/get.html', context)
            # return HTML with json
            browzer = True
            data_received = True
            context = {'browzer': browzer, 'json_data': json_data, 'data_received': data_received}
            return render(request, 'REST/get.html', context)
        
        else:
            # only return json
            browzer = False
            context = {'browzer': browzer, 'json_data': json_data}
            return render(request, 'REST/get.html', context)

    # context of view
    browzer = True
    data_received = False
    json_data = {'request': 'Get all data'}
    context = {'json_data': json_data, 'browzer': browzer, 'data_received': data_received}
    return render(request, 'REST/get.html', context)