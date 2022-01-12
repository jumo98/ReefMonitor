import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from ..aquariums.serializers import AquariumSerializer, MeasurementSerializer
from ..aquariums.models import Aquarium
from ..aquariums.handler import Handler

class SwaggerView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        f = open('static/swagger/swagger.json', 'r')
        data = json.load(f)
        return JsonResponse(data, safe=False)

class AquariumView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            aquarium = Aquarium.objects.get(id=id)
            serializer = AquariumSerializer(aquarium)
            return JsonResponse(serializer.data, safe=False)
        aquariums = Aquarium.objects.filter(owner=request.user)
        serializer = AquariumSerializer(aquariums, many=True)
        return JsonResponse(serializer.data, safe=False)

class MeasurementView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        serializer = MeasurementSerializer(data=request.data)
        
        if serializer.is_valid():
            measurement = serializer.save()
            handler = Handler(id)
            handler.AddMeasurement(measurement=measurement, external=True)
            measurement.delete()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)