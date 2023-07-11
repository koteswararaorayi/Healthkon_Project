from django.urls import path
from . import views, patient_view, patient_vitals_view

app_name = 'patient'

urlpatterns = [
    #path('name/', views.printName, name='name'),
    path('patient', patient_view.Patient.as_view(), name='patient'),
    path('vitals', patient_vitals_view.PatientVitals.as_view(), name='vitals'),
]