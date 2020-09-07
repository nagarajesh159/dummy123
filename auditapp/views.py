from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Country, State, Tag, URL
from .serializers import CountrySerializer, StateSerializer, TagSerializer, URLSerializer

import json

# Create your views here.


class DummyMixin(object):

    def get_object(self, obj_model, obj_id):
        # import ipdb;ipdb.set_trace()

        model = obj_model
        try:
            return model.objects.get(id=obj_id)
        except model.DoesNotExist:
            raise Http404


class IndexView(APIView):

    def get(self, request):
        return Response({"hello": "IndexView"}, status=status.HTTP_201_CREATED)
    
    
class CountryList(APIView):
    """
    List all Countrys, or create a new Country.
    """
    def get(self, request, format=None):
        Country_list = Country.objects.all()
        serializer = CountrySerializer(Country_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # import ipdb;ipdb.set_trace()
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetail(APIView):
    """
    Retrieve, update or delete a Country instance.
    """

    def get(self, request, country_id, format=None):
        country = self.get_object(obj_model=Country, obj_id=country_id)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def put(self, request, country_id, format=None):
        country = self.get_object(obj_model=Country, obj_id=country_id)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, country_id, format=None):
        country = self.get_object(obj_model=Country, obj_id=country_id)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StateList(DummyMixin, APIView):
    """
    List all States, or create a new State.
    """
    # def get_country_object(self, country_id):
    #     try:
    #         return Country.objects.get(id=country_id)
    #     except Country.DoesNotExist:
    #         raise Http404

    def get(self, request, country_id, format=None):

        # country = self.get_country_object(country_id)
        dummy_country = self.get_object(obj_model=Country, obj_id=country_id)
        # states = country.state_set.all()
        dummy_state = dummy_country.state_set.all()
        # serializer = StateSerializer(states, many=True)
        dummy_serializer = StateSerializer(dummy_state, many=True)
        # try:
        #     dct={"country": country.name_of_the_country}
        #     new_serializer_data = list(serializer.data)
        #     new_serializer_data.insert(0, dct)
            # new_serializer_data[:][country]=country.name_of_the_country
            # print({new_serializer_data[0]:list(serializer.data)})

        #     return Response(new_serializer_data)
        # except IndexError:
        #     return Response([])
        return Response(dummy_serializer.data)

    def post(self, request, country_id, format=None):
        country = self.get_object(obj_model=Country, obj_id=country_id)
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["country"] = country
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StateDetail(DummyMixin, APIView):
    """
    Retrieve, update or delete a State instance.
    """

    def get(self, request, state_id, format=None):
        state = self.get_object(obj_model=State, obj_id=state_id)
        serializer = StateSerializer(state)
        data = serializer.data
        data['country'] = state.country.name_of_the_country
        # print(data)
        return Response(data)

    def put(self, request, state_id, format=None):
        state = self.get_object(obj_model=State, obj_id=state_id)
        serializer = StateSerializer(state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, state_id, format=None):
        state = self.get_object(obj_model=State, obj_id=state_id)
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(DummyMixin, APIView):
    """
    List all Tags, or create a new Tag.
    """
    def get(self, request, state_id, format=None):
        state = self.get_object(obj_model=State, obj_id=state_id)
        tags = state.tag_set.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request, state_id, format=None):
        # import ipdb;ipdb.set_trace()
        state = self.get_object(obj_model=State, obj_id=state_id)
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["state"] = state
            serializer.validated_data["country"] = state.country
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(DummyMixin, APIView):
    """
    Retrieve, update or delete a Tag instance.
    """
    def get(self, request, tag_id, format=None):
        tag = self.get_object(obj_model=Tag, obj_id=tag_id)
        serializer = TagSerializer(tag)
        data = serializer.data
        data['country'] = tag.country.name_of_the_country
        data['state'] = tag.state.name_of_the_state
        return Response(data)

    def put(self, request, tag_id, format=None):
        tag = self.get_object(obj_model=Tag, obj_id=tag_id)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tag_id, format=None):
        tag = self.get_object(obj_model=Tag, obj_id=tag_id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class URLList(DummyMixin, APIView):
    """
    List all URLs, or create a new URL.
    """
    def get(self, request,tag_id, format=None):
        tag = self.get_object(obj_model=Tag, obj_id=tag_id)
        urls = URL.objects.all()
        serializer = URLSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request,tag_id, format=None):
        tag = self.get_object(obj_model=Tag, obj_id=tag_id)
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["state"] = tag
            serializer.validated_data["state"] = tag.state
            serializer.validated_data["country"] = tag.country
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class URLDetail(DummyMixin, APIView):
    """
    Retrieve, update or delete a URL instance.
    """
    def get(self, request, url_id, format=None):
        # import ipdb; ipdb.set_trace()
        url_data = self.get_object(obj_model=URL, obj_id=url_id)
        serializer = URLSerializer(url_data)
        data = serializer.data
        data['country'] = URL.country
        data['state'] = URL.state
        data['tag'] = URL.tag
        return Response(serializer.data)

    def put(self, request, url_id, format=None):
        url_data = self.get_object(obj_model=URL, obj_id=url_id)
        serializer = URLSerializer(url_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, url_id, format=None):
        url_data = self.get_object(obj_model=URL, obj_id=url_id)
        url_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetAllStates(APIView):

    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)


class GetAllTags(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


class GetAllURLs(APIView):

    def get(self, request):
        url_list = URL.objects.all()
        serializer = URLSerializer(url_list, many=True)
        return Response(serializer.data)


class SaveDataPoints(APIView):

    def post(self, **kwargs):
        pass

