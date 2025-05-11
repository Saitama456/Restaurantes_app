from rest_framework import serializers
from .models import Cliente, Reserva

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'fecha', 'hora', 'numero_personas', 'estado']

class ClienteSerializer(serializers.ModelSerializer):
    reservas = ReservaSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'correo', 'telefono', 'reservas']

   

