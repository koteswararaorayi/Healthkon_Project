from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,views,permissions
from django.db import connections
from django.db import IntegrityError
from django.http import HttpResponse
import json
from healthkon.settings import dt_format

class ConsultationTrend(APIView):
    def get(self, request):
        patient_id = request.data.get('patient_id',None)
        doctor_id = request.data.get('doctor_id',None)
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        if patient_id:
            query = f"""select cd.id, u.healthkon_id as Doctor, us.healthkon_id as Assigned_Doctor, notes_doc, 
                notes, labtests, medicines, labtests_notes, medicines_notes, status,  
                DATE_FORMAT(cd.created_at, '{dt_format}') as Date
                from consultation_details cd
                left join users u on u.id=cd.doctor_id
                left join users us on us.id=cd.assigned_doctor_id
                where patient_id={patient_id} and DATE(cd.created_at) between '{from_date}' and '{to_date}'
            """
        if doctor_id:
            query = f"""select cd.id, p.healthkon_id, u.healthkon_id as caretaker_id, us.healthkon_id as assigned_doctor_id, notes_doc, 
                notes, labtests, medicines, labtests_notes, medicines_notes, status,  
                DATE_FORMAT(cd.created_at, '{dt_format}') as Date
                from consultation_details cd
                left join users u on u.id=cd.caretaker_id
                left join users us on us.id=cd.assigned_doctor_id
                left join patients p on cd.patient_id = p.id
                where doctor_id={doctor_id} and DATE(cd.created_at) between '{from_date}' and '{to_date}'
            """

        try:                        
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                col_names = [col[0] for col in cursor.description]
                trends = [dict(zip(col_names,row)) for row in rows]
                cursor.close()
            if trends:
                return Response({"data": trends}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Patient vitals data does not exists with this ID within date range"},status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
