from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MovieSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *

# Create your views here.
class MovieApi(APIView):
    def get(self, request,**kwargs):
        if kwargs.get('pk'):
            pk = kwargs.get('pk')
            obj = get_object_or_404(Movie.objects.all(), pk=pk)
            movie = MovieSerializer(obj)
            return Response({'movie' : movie.data})

        movie = Movie.objects.all()
        movies = MovieSerializer(movie, many = True)
        return Response({'movies':movies.data})

    def post(self, request):
        serializer = MovieSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status= status.HTTP_401_BAD_CREATED)

    def put(self, request,pk):
        movie = get_object_or_404(Movie.objects.all(), pk = pk)
        mv = MovieSerializer(instance = movie, data= request.data, partial = True)
        if mv.is_valid(raise_exception = True):
            mv.save()
            print(mv)
        return Response(mv.data)

    def delete(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        movie.delete()
        return Response({"message":"deleed successfully"}, status = 204)