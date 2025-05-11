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

from rest_framework import status

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        mesa_id = data.get('mesa')
        fecha = data.get('fecha')
        hora = data.get('hora')

        # Verificar si ya existe una reserva confirmada para esa mesa en esa fecha y hora
        ya_reservada = Reserva.objects.filter(
            mesa_id=mesa_id,
            fecha=fecha,
            hora=hora,
            estado='confirmada'
        ).exists()

        if ya_reservada:
            return Response(
                {"error": "La mesa ya está reservada en ese horario."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


# Create your views here.
