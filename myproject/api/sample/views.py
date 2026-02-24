from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


class SampleLCView(ListCreateAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


class SampleRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello!"})


@api_view(['GET'])
def say_hello(request):
    return Response("HELLO")


@api_view(['GET'])
def say_test(request):
    return Response("TEST")


@api_view(['GET'])
def say_hi(request):
    return Response("HI!")


@api_view(['GET'])
def increment(request, number):
    result = number + 1
    return Response({"input": number, "result": result})