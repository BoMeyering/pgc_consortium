"""
API Views
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# from drf_spectacular.utils import extend_schema

from resources.models import Person
from data_storage.models import Plot
from api.serializers import PersonSerializer, PlotSerializer
from api.responses import ApiResponse

# Create your API views here.

# @api_view(['GET', 'POST'])
# def list_people(request, format=None):
#     """
#     List all records in the Person table
#     """

#     if request.method == 'GET':
#         people = Person.objects.all()
#         serializer = PersonSerializer(people, many=True)

#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = PersonSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def list_person(request, db_id, format=None):
#     """
#     List a single record in the Person table
#     """
#     try:
#         person = Person.objects.get(db_id=db_id)
#     except Person.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = PersonSerializer(person)
        
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = PersonSerializer(person, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         person.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class PersonList(APIView):
    """
    Get all objects in the Person table
    """

    def get(self, request, format=None):
        """ GET the list of all the people """
        people = Person.objects.all()
        serializer = PersonSerializer(people, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """ POST a list of people """
        serializer = PersonSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PersonDetail(APIView):
    """
    Get the details for a single person
    """
    def get_object(self, db_id):
        """ Get an object from the database """
        try:
            return Person.objects.get(db_id=db_id)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_410_GONE)
                
    def get(self, request, db_id, format=None):
        """ GET the details for one person """
        person = self.get_object(db_id)
        serializer = PersonSerializer(person)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, db_id, format=None):
        """ Update the record for one person """
        person = self.get_object(db_id=db_id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, db_id, format=None):
        """ DELETE a person's record from the Person table """
        person = self.get_object(db_id=db_id)
        person.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PlotList(APIView):
    """
    Get a list of all the plots
    """

    def get(self, request, format=None):
        plots = Plot.objects.all()
        serializer = PlotSerializer(plots, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

