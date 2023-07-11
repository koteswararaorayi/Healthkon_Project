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

class Trend(APIView):
    def get(self, request):
        vitals_data = (request.data['vitals_data'])
        patient_id = request.data.get('patient_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        try:
            with connections['default'].cursor() as cursor:
                l = []
                for vitals in vitals_data:
                    vital_type = vitals['vital_type'] 
                    query = f"""select vital_type, vital_value, DATE_FORMAT(created_at, '{dt_format}') as Date
                        from patient_vitals where patient_id={patient_id} and vital_type='{vital_type}'and 
                        date(created_at) between '{from_date}' and '{to_date}'
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    col_names   = [names[0] for names in cursor.description]
                    vitals  = [dict(zip(col_names, row_data)) for row_data in rows]
                    l.extend(vitals)
                cursor.close()
            if l:
                return Response({"data": l}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Patient vitals data does not exists with this ID within date range"},status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)