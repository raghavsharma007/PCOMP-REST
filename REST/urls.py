from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'REST'
urlpatterns = [
    path('', views.index, name='index'), # home page
    path('view_data/', views.view_data, name='view_data'), # for viewing data
    path('post/', views.post, name='post'), # for posting data into db
    path('put/', views.put, name='put'), # for updating data into db
    path('dbtable/', views.dbtable, name='dbtable'), # for view data in db table

    # database encryption
    path('security/', views.security, name='security'),
    path('getjsondata/', views.getjsondata, name='getjsondata'),
]
