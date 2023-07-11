from django.urls import path
from . import views

app_name = 'module1'

urlpatterns = [
    path('', views.index, name='index'),
    path('name/', views.printName, name='name'),
    path('first/', views.firstHtml, name='first'),
    path('add/', views.add, name='add'),
    path('add/addrecord/', views.addrecord, name='addrecord'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('update/<int:id>', views.update, name='delete'),
    path('update/updaterecord/<int:id>', views.updaterecord, name='delete'),
]