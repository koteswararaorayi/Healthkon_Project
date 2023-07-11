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
from django.http import JsonResponse
from rest_framework.decorators import api_view

class Consultation(APIView):
    #add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request ):
        doctor_id = request.data['doctor_id']
        caretaker_id = request.user.id
        patient_id = request.data['patient_id']
        try:
            query = f"""
                INSERT INTO consultation_details (doctor_id, caretaker_id, patient_id, created_by)
                VALUES({doctor_id},{caretaker_id},{patient_id}, {request.user.id})
            """
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                cursor.close()
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Consultation started"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        consultation_id = request.data.get('consultation_id',None)
        assigned_doctor_id = request.data.get('assigned_doctor_id',None)
        notes_doc = request.data.get('notes_doc',None)
        notes = request.data.get('notes',None)
        labtests = request.data.get('labtests',None)
        medicines = request.data.get('medicines',None)
        labtests_notes = request.data.get('labtests_notes',None)
        medicines_notes = request.data.get('medicines_notes',None)
        consulatation_status = request.data.get('status',None)
        try:
            query = f"update consultation_details set updated_by={request.user.id}, "

            if assigned_doctor_id:
                query = query+f" assigned_doctor_id={assigned_doctor_id},"
            
            if notes_doc:
                query = query+f" notes_doc='{notes_doc}',"

            if notes:
                query = query+f" notes='{notes}',"

            if labtests:
                query = query+f" labtests='{labtests}',"

            if medicines:
                query = query+f" medicines='{medicines}',"

            if labtests_notes:
                query = query+f" labtests_notes='{labtests_notes}',"

            if medicines_notes:
                query = query+f" medicines_notes='{medicines_notes}',"

            if consulatation_status:
                query = query+f" status='{consulatation_status}',"

            query = query[:-1]+f" where id={consultation_id}"
            with connections['default'].cursor() as cursor:
                rows = cursor.execute(query)
                cursor.close()
                if rows:
                    return Response({"message": "Consultation Details Successfully Updated"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Consultation with this id does not exists"}, status=status.HTTP_400_BAD_REQUEST)             
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)