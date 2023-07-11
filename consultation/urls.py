from django.urls import path
from . import views, consultation_view

app_name = 'consultation'

urlpatterns = [
    path('', consultation_view.Consultation.as_view(), name='consultation'),

]