from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Mesa, Reserva
from .serializers import ClienteSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import MesaSerializer, ReservaSerializer
from django.core.mail import send_mail

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

    def perform_create(self, serializer):
        reserva = serializer.save()
        self.enviar_correo(reserva, nuevo=True)

    def perform_update(self, serializer):
        reserva = serializer.save()
        self.enviar_correo(reserva, nuevo=False)

    def enviar_correo(self, reserva, nuevo=True):
        try:
            cliente = Cliente.objects.get(id=reserva.cliente_id)
            mesa = Mesa.objects.get(id=reserva.mesa_id)

            asunto = "✅ Nueva Reserva Confirmada" if nuevo else "✏️ Reserva Modificada"
            mensaje = (
                f"Hola {cliente.nombre},\n\n"
                f"{'Se ha creado una nueva reserva' if nuevo else 'Tu reserva ha sido actualizada'}.\n\n"
                f"📅 Fecha: {reserva.fecha}\n"
                f"⏰ Hora: {reserva.hora}\n"
                f"🍽️ Mesa asignada: {mesa.id} (Capacidad: {mesa.capacidad})\n"
                f"👥 Número de personas: {reserva.numero_personas}\n"
                f"📌 Estado: {reserva.estado}\n\n"
                f"Gracias por elegir nuestro restaurante.\n"
            )

            send_mail(
                subject=asunto,
                message=mensaje,
                from_email='admin@restaurante.com',
                recipient_list=[cliente.correo],
                fail_silently=False,
            )
        except Exception as e:
            print("❌ Error al enviar correo:", e)


# Create your views here.
