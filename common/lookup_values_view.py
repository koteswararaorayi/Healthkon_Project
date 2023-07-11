from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,views,permissions
from django.db import connections
from django.db import IntegrityError
from rest_framework.decorators import api_view
from uuid import uuid4

class LookupValues(APIView):
    def post(self, request):
        lookup_type = request.data['lookup_type']
        name = request.data['name']
        parent_id = request.data['parent_id']
        try:
            with connections['default'].cursor() as cursor:
                query = f"""
                    INSERT INTO lookup_values (lookup_type, name, parent_id)
                    VALUES('{lookup_type}', '{name}', {parent_id});
                """
                cursor.execute(query)
                cursor.close()
            return Response({"message": "Lookup Values successfully entered."},  status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        lookup_type = request.GET.get('type')
        parent_id = request.GET.get('parent_id',0)
        query = f"""
            select id, lookup_type, name  
            from lookup_values 
            where parent_id={parent_id} and lookup_type='{lookup_type}'
        """
        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            col_names   = [names[0] for names in cursor.description]
            clients  = [dict(zip(col_names, row_data)) for row_data in rows]
            cursor.close()
        return Response({"data": clients}, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def clients_token(request):
    if request.method == 'POST':
        clients_name = request.data['name']
        token = uuid4().hex
        try:
            with connections['default'].cursor() as cursor:
                query = f"""
                    INSERT INTO clients (clients_name, token)
                    VALUES('{clients_name}', '{token}')
                """
                cursor.execute(query)
                cursor.close()
            return Response({"message": "Lookup Values successfully entered."},  status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    if request.method == "GET":
        try:
            with connections['default'].cursor() as cursor:
                query = f"""
                    SELECT id, clients_name from clients
                    """
                cursor.execute(query)
                rows = cursor.fetchall()
                col_names   = [names[0] for names in cursor.description]
                clients  = [dict(zip(col_names, row_data)) for row_data in rows]
                cursor.close()
            return Response({"data": clients}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({"message": "Request could not be completed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)