from django.shortcuts import render
from numpy import size
from rest_framework import generics, status
from api.documents import NewsDocument
from rest_framework.response import Response
from api.models import News

from api.serializers import NewsSerializer

class CreateNewsView(generics.ListAPIView):
    pass
# Create your views here.
import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
import operator
import time


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None


    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            start_time = time.time()
            response = search.execute()
            stop_time = time.time()
            print(f"Execute time is {stop_time - start_time}")

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)

class SearchNews(PaginatedElasticSearchAPIView):
    serializer_class = NewsSerializer
    document_class = NewsDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'title',
                    "content"
                    "created_time",
                    "location",
                    "author"
                ], fuzziness='auto')

class SortedLatest(APIView):
    serializer_class = NewsSerializer
    document_class = NewsDocument
    
    def get(self, request):
        try:
            # search = self.document_class.search().sort("created_time", {"order": "desc"})
            # response = search.execute()

            #print(f'Found {response.hits.total.value} hit(s) for query')
            ordererd = News.objects.all().order_by("-created_time")[0:70]
            
            #results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(ordererd, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(e, status=500) 
