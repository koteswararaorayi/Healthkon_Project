from django.urls import path
from . import views, patient_trends_view, consultation_trends_view

app_name = 'report'

urlpatterns=[
    path('patient_trends',patient_trends_view.Trend.as_view(),name='patient_trends'),
    path('consultation_trends',consultation_trends_view.ConsultationTrend.as_view(),name='consultation_trends'),
]