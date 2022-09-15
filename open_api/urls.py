from django.contrib import admin
from django.urls import path, include
from open_api.views import test, imports, delete, get_all, all_files, nodes

urlpatterns = [
    path('test/', test),
    path('imports', imports),
    path('delete/<str:id>', delete),
    path('all', get_all),
    path('all_files', all_files),
    path('nodes/<str:id>', nodes),
]
