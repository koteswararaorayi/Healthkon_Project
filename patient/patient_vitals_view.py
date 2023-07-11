from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,views,permissions
from django.db import connections
from django.db import IntegrityError

class PatientVitals(APIView):
    def post(self, request):
        vitals_data = (request.data['vitals_data'])
        patient_id = request.data.get('id')
        try:
            with connections['default'].cursor() as cursor:
                for vitals in vitals_data:
                    vital_type = vitals['vital_type']
                    vital_value = vitals['vital_value']
                    query = f"""
                        INSERT INTO patient_vitals 
                        (vital_type, vital_value, patient_id)
                        VALUES('{vital_type}', '{vital_value}', {patient_id});
                    """
                    cursor.execute(query)
            cursor.close()
            return Response({"message": "Patient vitals successfully saved."},  status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)