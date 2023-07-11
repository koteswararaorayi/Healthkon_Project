from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,views,permissions
from django.db import connections
from django.db import IntegrityError
from rest_framework.parsers import FileUploadParser,MultiPartParser,JSONParser
import json
from django.core.files.storage import default_storage
import random
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
from common.views import fileView


class Patient(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser,FileUploadParser]
    #@method_decorator(cache_page(60*2))
    def get(self, request):
        healthkon_id = request.GET.get('healthkon_id')       
        if healthkon_id:
            query = f"""
                select p.healthkon_id,p.first_name, p.last_name, p.dob as date_of_birth,p.gender,p.bloodgroup,
                p.mobile,p.address,pr.height,pr.weight,pr.allergies,pr.description,pr.supporting_docs from patients p
                left join patient_report pr on pr.patient_id = p.id
                where p.healthkon_id='{healthkon_id}'
            """
        else:
            query = f"""
                select p.healthkon_id,concat(p.first_name,' ', p.last_name)as name, p.dob as date_of_birth,p.gender,p.bloodgroup,
                p.mobile,p.address,pr.height,pr.weight,pr.allergies,pr.description,pr.supporting_docs from patients p
                left join patient_report pr on pr.patient_id = p.id order by p.id desc
            """
        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            details  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
        if details:
            return Response({"data": details}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Patient with this ID does not exists"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        file_obj = request.FILES.getlist('file_name')
        supporting_docs = fileView(file_obj)
        first_name = data.get('first_name')        
        last_name = data.get('last_name')
        dob = data.get('dateofbirth')
        gender = data.get('gender')
        bloodgroup = data.get('bloodgroup')
        mobile = data.get('mobile')
        address = data.get('address')
        height = data.get('height')
        weight = data.get('weight')
        allergies = data.get('allergies')
        description = data.get('description')
        #supporting_docs = data.get('supporting_docs')
        print(request.user)
        try:
            query = f"""
                INSERT INTO patients 
                (first_name, last_name, dob, gender, bloodgroup, mobile, address, created_by)
                VALUES('{first_name}', '{last_name}', '{dob}', '{gender}', '{bloodgroup}', '{mobile}', '{address}', '{request.user}');
            """
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                last_rec_id = cursor.lastrowid
                query =f""" 
                    INSERT INTO patient_report (patient_id, height, weight, allergies, description, supporting_docs) 
                    VALUES ({last_rec_id}, '{height}', '{weight}', '{allergies}', '{description}', '{supporting_docs}');
                """
                cursor.execute(query)
                if last_rec_id<10:
                    healthkon_id = 'HKPAT0000'+str(last_rec_id)
                elif last_rec_id<100:
                    healthkon_id = 'HKPAT000'+str(last_rec_id)
                elif last_rec_id<1000:
                    healthkon_id = 'HKPAT00'+str(last_rec_id)
                elif last_rec_id<10000:
                    healthkon_id = 'HKPAT0'+str(last_rec_id)
                elif last_rec_id<100000:
                    healthkon_id = 'HKPAT'+str(last_rec_id)
                query = f"""
                        UPDATE patients set healthkon_id='{healthkon_id}' where id={last_rec_id}
                    """
                cursor.execute(query)
                cursor.close()
            return redirect('common:patient_data')
            #return Response({"message": "patient successfully created"},  status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
    def put(self, request):
        patient_id = request.data.get('patient_id')
        mobile = request.data.get('mobile')
        address = request.data.get('address')
        height = request.data.get('height')
        weight = request.data.get('weight')
        allergies = request.data.get('allergies')
        description = request.data.get('description')
        query = f""" 
            update patients p,patient_report pr
            set p.mobile='{mobile}', p.address='{address}', pr.height='{height}', pr.weight='{weight}',
            pr.allergies='{allergies}',pr.description='{description}'
            where p.id='{patient_id}' and pr.patient_id='{patient_id}'
        """
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                cursor.close()
            return Response({"message": "patient details successfully updated."},  status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        patient_id = request.data.get('id')
        query = f"""
            delete p.*,pr.* from patients p
            left join patient_report pr on pr.patient_id = p.id
            where p.id={patient_id}
        """
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                cursor.close()
            return Response({"message": "patient details successfully deleted."},  status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    