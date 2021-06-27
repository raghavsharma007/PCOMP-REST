from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import TestData
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import random


@shared_task
def multifunc_post(test_data):
    for i in test_data:
        TestData.objects.create(column1=i['column1'], column2=i['column2'], column3=i['column3'],  column4=i['column4'],  column5=i['column5'], column6=i['column6'], column7=i['column7'], column8=i['column8'], column9=i['column9'], column10=i['column10'])
    return None

@shared_task
def multifunc_put(test_data):
    ids = TestData.objects.values_list('id', flat=True)[:25]
    for index, i in enumerate(test_data):
        TestData.objects.filter(pk=ids[index]).update(column1=i['column1'], column2=i['column2'], column3=i['column3'],  column4=i['column4'],  column5=i['column5'], column6=i['column6'], column7=i['column7'], column8=i['column8'], column9=i['column9'], column10=i['column10'])
    return None

# encryption and decryption
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



# @periodic_task(run_every=(crontab(minute='*/1')), name="dynamic db encryption", ignore_result=True)
@shared_task
def encrypt_db():
    encryption_key = 'encryptionkey1234'
    all_data = TestData.objects.all()
    random_num = random.randint(1,10)
    for i in all_data:
        if i.random_encryptionNum != None and int(i.random_encryptionNum) != 0:
            print('data is encrypted')
            column1 = decrypt(encryption_key, i.column1, i.random_encryptionNum)
            column2 = decrypt(encryption_key, i.column2, i.random_encryptionNum)
            column3 = decrypt(encryption_key, i.column3, i.random_encryptionNum)
            column4 = decrypt(encryption_key, i.column4, i.random_encryptionNum)
            column5 = decrypt(encryption_key, i.column5, i.random_encryptionNum)
            column6 = decrypt(encryption_key, i.column6, i.random_encryptionNum)
            column7 = decrypt(encryption_key, i.column7, i.random_encryptionNum)
            column8 = decrypt(encryption_key, i.column8, i.random_encryptionNum)
            column9 = decrypt(encryption_key, i.column9, i.random_encryptionNum)
            column10 = decrypt(encryption_key, i.column10, i.random_encryptionNum)
        else:
            print('data is not encrypted earlier')
            column1, column2, column3, column4, column5, column6, column7, column8, column9, column10 = i.column1, i.column2, i.column3, i.column4, i.column5, i.column6, i.column7, i.column8, i.column9, i.column10

        print('encrypting the data')
        i.column1 = encrypt(encryption_key, column1, random_num)
        i.column2 = encrypt(encryption_key, column2, random_num)
        i.column3 = encrypt(encryption_key, column3, random_num)
        i.column4 = encrypt(encryption_key, column4, random_num)
        i.column5 = encrypt(encryption_key, column5, random_num)
        i.column6 = encrypt(encryption_key, column6, random_num)
        i.column7 = encrypt(encryption_key, column7, random_num)
        i.column8 = encrypt(encryption_key, column8, random_num)
        i.column9 = encrypt(encryption_key, column9, random_num)
        i.column10 = encrypt(encryption_key, column10, random_num)
        i.random_encryptionNum = random_num
        print(column1, i.column1, random_num)
        try:
            i.save()
        except:
            print('error in datatype of postgreSQL')