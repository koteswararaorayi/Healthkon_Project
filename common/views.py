from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,views,permissions
from django.db import connections
from django.db import IntegrityError
from rest_framework.parsers import FileUploadParser,MultiPartParser
from django.core.files.storage import default_storage
import random
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.contrib import messages
from rest_framework.decorators import api_view

def fileView(file_obj):
    file_list = []
    for file_name in file_obj:
        n = str(id(file_name))
        file = (n + str(file_name))
        def process(file_name,y):
            with default_storage.open( n + str(file_name), 'wb+') as destination:
                for chunk in file_name.chunks():
                    destination.write(chunk)
        process(file_name,n)
        file_list.append(file)
    supporting_docs = ','.join(file_list)
    return supporting_docs

class RoleView(APIView):
    def post(self, request):
        role_name = request.data['role_name']
        active = 1
        try:
            with connections['default'].cursor() as cursor:
                query = f"""
                    INSERT INTO roles 
                    (role_name, active)
                    VALUES('{role_name}', {active});
                """
                cursor.execute(query)
                cursor.close()
            return Response({"message": "User roles successfully created."},  status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        template = loader.get_template('registration.html')
        query = """
            select id, role_name from roles
        """
        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            roles  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
            return Response({"data": roles}, status=status.HTTP_200_OK)
            # context={ 'roles': roles, }
            # print(context)
            # return HttpResponse(template.render(context, request))
            #return render(request, 'registration.html', context)

class Speciality(APIView):
    def post(self, request):
        speciality_name = request.data['speciality_name']
        description = request.data['description']
        try:
            with connections['default'].cursor() as cursor:
                query = f"""
                    INSERT INTO specialities 
                    (speciality_name, description)
                    VALUES('{speciality_name}', '{description}');
                """
                cursor.execute(query)
                cursor.close()
            return Response({"message": "Doctor specialities successfully entered."},  status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        query = """
            select id,speciality_name as speciality from specialities
        """
        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            rows  = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            specialities  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
            return Response({"data": specialities}, status=status.HTTP_200_OK)

def login_request(request):
    template = loader.get_template('login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f' welcome {email} !!')
            return redirect('common:home')
        else:
            messages.error(request,"Invalid username or password.")        
    return render(request,'login.html',{})

def index(request):

    return render(request,'home.html',{})

def logoutRequest(request):
    logout(request)
    messages.info(request,"Successfully logout.")
    return render(request,'login.html',{})

def patientData(request):
    return render(request,'patients.html',{})

def registrationRequest(request):
    return render(request,'registration.html',{})

def patientDetails(request):
    healthkon_id = request.GET.get('healthkon_id')

    return render(request,'patient_details.html',{'healthkon_id':healthkon_id})


@api_view(('GET','POST'))
def emailValidation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            query = f'''
                select * from users where email="{email}"
            '''
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                row  = cursor.fetchone()
            if row:                
                return Response({"message": "Email/Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Email Valid'}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)