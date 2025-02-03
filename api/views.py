"""
API Views
"""

import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
# from drf_spectacular.utils import extend_schema

from resources.models import Person, Location, Project
from data_storage.models import Plot, Trial, Treatment
from ontology.models import TraitEntity, TraitAttribute, VarTrait, VarMethod, VarScale, Variable, SopDocument, AgroProcess
from imaging.models import AwsModel, Image, ImageOperation
from api.serializers import LocationSerializer, PersonSerializer, PlotSerializer, TrialSerializer, TreatmentSerializer
from api.serializers import ProjectSerializer
from api.serializers import AwsModelSerializer, ImageSerializer, ImageOperationSerializer

###### Resources API Views ######
class LocationList(ListAPIView):
    """
    Get location objects
    """

    # Paginated GET data
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def post(self, request, format=None):
        """
        POST a list of new location objects
        """

        serializer = LocationSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonList(ListAPIView):
    """
    Get all objects in the Person table
    """

    # Paginated GET data
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    # def get(self, request, format=None):
    #     """ GET the list of all the people """
    #     people = Person.objects.all()
    #     serializer = PersonSerializer(people, many=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """ POST a list of people """
        serializer = PersonSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PersonDetail(APIView):
    """
    Manage the details for a single person
    """
    def retrive_person(self, db_id):
        """
        Retrieve a single Person object from the database using the db_id.
        """
        try:
            return Person.objects.get(db_id=db_id)
        except Person.DoesNotExist:
            raise NotFound(f"No Person with db_id={db_id} was found.")
                
    def get(self, request, db_id, format=None):
        """
        GET the details for one person
        """
        person = self.retrive_person(db_id)
        serializer = PersonSerializer(person)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, db_id, format=None):
        """
        Update the record details for one person
        """
        person = self.get_person(db_id=db_id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, db_id, format=None):
        """
        DELETE a Person record corresponding to the db_id
        """
        person = self.get_person(db_id=db_id)
        person.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectList(ListAPIView):
    """
    Get Project objects
    """
    # Paginated GET data
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


###### Data Storage API Views ######
class PlotList(ListAPIView):
    """
    Manage all the plots in the database
    """

    # Paginated GET data
    serializer_class = PlotSerializer

    def get_queryset(self):
        """
        Obtain and filter a queryset for the GET request based on query parameters
        """
        # Grab the queryset and API query parameters
        queryset = Plot.objects.all()
        trial_id = self.request.query_params.get('trial_id', None)
        label = self.request.query_params.get('label', None)
        type = self.request.query_params.get('type', None)
        parent_plot_id = self.request.query_params.get('parent_plot_id', None)

        # Filter queryset based on query parameters
        if trial_id:                                                                                            
            queryset = queryset.filter(trial_id=trial_id)
        if label:
            queryset = queryset.filter(label=label)
        if type:
            queryset = queryset.filter(type=type)
        if parent_plot_id:
            queryset = queryset.filter(parent_plot_id=parent_plot_id)
                                       
        return queryset                                                                                                                 
    
    def post(self, request, format=None):
        """
        POST a list of new plots to add to a field trial(s)
        """
        serializer = PlotSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TrialList(ListAPIView):
    """
    Manage all the trials in the database
    """
    # Paginated GET data
    serializer_class = TrialSerializer

    def get_queryset(self):
        """
        Obtain and filter a queryset for the GET request based on query parameters
        """
        # Grab the queryset and API query parameters
        queryset = Trial.objects.all()
        trial_id = self.request.query_params.get('trial_id', None)
        name = self.request.query_params.get('name', None)
        affiliation_id = self.request.query_params.get('affiliation_id', None)
        establishment_year = self.request.query_params.get('establishment_year', None)

        # Filter queryset based on query parameters
        if trial_id:                                                                                            
            queryset = queryset.filter(trial_id=trial_id)
        if name:
            queryset = queryset.filter(name=name)
        if affiliation_id:
            queryset = queryset.filter(affiliation_id=affiliation_id)
        if establishment_year:
            queryset = queryset.filter(establishment_year=establishment_year)
                                       
        return queryset  
    
class TreatmentList(ListAPIView):
    """
    Manage all the treatments in the database
    """
    # Paginated GET data
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        """
        Obtain and filter a queryset for the GET request based on query parameters
        """
        # Grab the queryset and API query parameters
        queryset = Treatment.objects.all()
        treatment_id = self.request.query_params.get('treatment_id', None)
        name = self.request.query_params.get('name', None)
        type = self.request.query_params.get('type', None)

        # Filter queryset based on query parameters
        if treatment_id:                                                                                            
            queryset = queryset.filter(treatment_id=treatment_id)
        if name:
            queryset = queryset.filter(name=name)
        if type:
            queryset = queryset.filter(type=type)
                                       
        return queryset  


###### Ontology API Views ######

###### Imaging API Views ######
class AwsModelList(ListAPIView):
    """
    Manage all the AWS Model objects in the database
    """
    # Paginated GET data
    serializer_class = AwsModelSerializer

    # Filter paginated results
    def get_queryset(self):
        """
        Obtain and filter a queryset for the GET request based on query parameters
        """
        # Grab the queryset and API query parameters
        queryset = AwsModel.objects.all()
        name = self.request.query_params.get('name', None)
        endpoint_url = self.request.query_params.get('endpoint_url', None)

        # Filter queryset based on query parameters
        if name:                                                                                         
            queryset = queryset.filter(name=name)
        if endpoint_url:
            queryset = queryset.filter(endpoint_url=endpoint_url)
                                       
        return queryset  
    
class ImageList(ListAPIView):
    """
    Manage images in the database
    """

    serializer_class = ImageSerializer

    def get_queryset(self):
        """
        Obtain and filter a a queryset for the GET request based on the query parameters
        """

        # Grab the queryset and API query parameters
        queryset = Image.objects.all()
        filename = self.request.query_params.get('name', None)
        storage_url = self.request.query_params.get('endpoint_url', None)
        observation_id = self.request.query_params.get('observation_id', None)

        # Filter queryset based on query parameters
        if filename:                                                                                         
            queryset = queryset.filter(filename=filename)
        if storage_url:
            queryset = queryset.filter(storage_url=storage_url)
                                       
        return queryset
    
class ImageOperationDetail(APIView):
    def retrive_image_operation(self, db_id):
        """
        Retrieve a single ImageOperation object from the database using the db_id.
        """
        try:
            print(f"finding person {db_id}")
            return ImageOperation.objects.get(db_id=db_id)
        except ImageOperation.DoesNotExist:
            raise NotFound(f"No image operation with db_id={db_id} was found.")
                
    def get(self, request, db_id, format=None):
        """
        GET the details for one image operation
        """
        image_operation = self.retrive_image_operation(db_id)
        serializer = ImageOperationSerializer(image_operation)

        return Response(serializer.data, status=status.HTTP_200_OK)
