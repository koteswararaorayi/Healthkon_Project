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
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login,logout
from .serializers import MyUserSerializer
from .models import MyUser

class User(APIView):
    #add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]
    def post(self, request ):
        email = request.data['email']
        password = make_password(request.data['password'])
        mobile = request.data['mobile']
        roleid = request.data['roleid']
        speciality_id = request.data.get('speciality_id','NULL')
        project_id = request.data.get('project_id',None)
        location_id = request.data.get('location_id',None)
        account_id = request.data.get('client_id',None)
        try:
            query = f"""
                INSERT INTO users 
                (mobile, roleid, speciality_id, email, password, project_id, location_id)
                VALUES('{mobile}',{roleid},{speciality_id},'{email}','{password}','{project_id}','{location_id}')
            """
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                last_rec_id = cursor.lastrowid
                query = f"""
                    select clients_name, token from clients where id={account_id}
                """
                cursor.execute(query)
                row = cursor.fetchone()
                account_id = row[0]
                token = row[1]
                if roleid == '1':
                    healthkon_id = 'HKACT'+str(last_rec_id)
                elif roleid == '2':
                    healthkon_id = 'HKDR'+str(last_rec_id)
                elif roleid == '3':
                    healthkon_id = 'HKCT'+str(last_rec_id)
                query = f"""
                    UPDATE users set healthkon_id='{healthkon_id}',account_id='{account_id}', 
                    token='{token}'  where id={last_rec_id} 
                """
                row = cursor.execute(query)
                if row:
                    query = f"""
                        select id, healthkon_id, account_id as Client, email, mobile, project_id as Project,
                        location_id as Location, speciality_id, roleid from users where id={last_rec_id}
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    col_names   = [names[0] for names in cursor.description]
                    user  = [dict(zip(col_names, row_data)) for row_data in rows]
                cursor.close()
            return render(request,'login.html',{})
        except IntegrityError as e:
            return Response({"message": "Email/Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": user}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = request.data.get('user_id')
        if user_id:
            query = f"""
                select  r.role_name as Role, s.speciality_name as speciality, email, mobile, healthkon_id from users u
                left join roles r on r.id=u.roleid
                left join specialities s on s.id=u.speciality_id
                where u.id={user_id} and u.active={'1'}
                order by u.id asc 
            """
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                rows  = cursor.fetchall()
                col_names   = [names[0] for names in cursor.description]
                user  = [dict(zip(col_names, row_data)) for row_data in rows]
                cursor.close()
            if not user:
                return Response({"message": "The requried User is Not Available"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"data": user}, status=status.HTTP_200_OK)
                
        else:
            query = """
                select  r.role_name as Role, s.speciality_name as speciality, email, mobile, healthkon_id from users u
                left join roles r on r.id=u.roleid
                left join specialities s on s.id=u.speciality_id
                order by u.id asc
            """
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
                rows  = cursor.fetchall()
                col_names   = [names[0] for names in cursor.description]
                users  = [dict(zip(col_names, row_data)) for row_data in rows]
                cursor.close()
                return Response({"data": users}, status=status.HTTP_200_OK)

    def put(self, request):
        user_id = request.data['user_id']
        mobile = request.data['mobile']
        try:
            query = f"""
                UPDATE users set mobile='{mobile}' where id={user_id}
            """
            with connections['default'].cursor() as cursor:
                rows = cursor.execute(query)
                cursor.close()
            if rows:
                return Response({"message": "User Details Successfully Updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User with this id does not exists"}, status=status.HTTP_400_BAD_REQUEST)             
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.data['user_id']
        query = f"""
           update users set active={'0'} where id={user_id} 
        """
        with connections['default'].cursor() as cursor:
            rows = cursor.execute(query)
            cursor.close()
        if rows:
            return Response({"message": "User Successfully Deactived"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User with this id does not exists"}, status=status.HTTP_400_BAD_REQUEST)

# class ModelUserCreation(APIView):
#     """ 
#     Creates the user. 
#     """

#     def post(self, request):
#         serializer = MyUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             user.set_password(user.password)
#             user.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)