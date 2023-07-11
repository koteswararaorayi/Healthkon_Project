from django.urls import path
from . import views, user_creation_view, lookup_values_view

app_name = 'common'

urlpatterns = [
    #path('file_upload', views.FileView.as_view(), name='file_upload'),
    path('role', views.RoleView.as_view(), name='role'),
    path('speciality', views.Speciality.as_view(), name='speciality'),
    path('user', user_creation_view.User.as_view(), name='user'),
    #path('user_creation', user_creation_view.ModelUserCreation.as_view(), name='user_creation'),
    path('lookup', lookup_values_view.LookupValues.as_view(), name='lookup'),
    path('clients_token', lookup_values_view.clients_token, name='clients_token'),
    path('login', views.login_request, name='login'),
    path('home', views.index, name='home'),
    path('logout', views.logoutRequest, name='logout'),
    path('patient_data', views.patientData, name='patient_data'),
    path('registration', views.registrationRequest, name='registration'),
    path('email_validate', views.emailValidation, name='email_validate'),
    path('patient_details', views.patientDetails, name='patient_details'),
]
    