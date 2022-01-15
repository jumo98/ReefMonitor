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
            try:
                aquarium = Aquarium.objects.get(id=id)
            except Aquarium.DoesNotExist:
                return Response(data="Aquarium was not found.", status=status.HTTP_404_NOT_FOUND)
            if aquarium.owner != request.user:
                return Response(data="No access to this aquarium.", status=status.HTTP_403_FORBIDDEN)
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

        try:
            aquarium = Aquarium.objects.get(id=id)
        except Aquarium.DoesNotExist:
            return Response(data="Aquarium was not found.", status=status.HTTP_404_NOT_FOUND)
        if aquarium.owner != request.user:
            return Response(data="No access to this aquarium.", status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            measurement = serializer.save()
            if not measurement.ValidParameters():
                return Response("Duplicate parameters set", status=status.HTTP_400_BAD_REQUEST)
            handler = Handler(id)
            handler.AddMeasurement(measurement=measurement, external=True)
            measurement.delete()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)