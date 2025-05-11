from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Mesa, Reserva
from .serializers import ClienteSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import MesaSerializer, ReservaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class AdminStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        is_admin = request.user.is_staff or request.user.is_superuser
        return Response({'is_admin': is_admin})

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

# Create your views here.
