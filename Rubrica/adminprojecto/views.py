from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Mesa
from .serializers import MesaSerializer

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



# Create your views here.
