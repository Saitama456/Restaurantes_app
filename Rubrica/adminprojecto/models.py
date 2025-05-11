from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    capacidad = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=10,
        choices=[("disponible", "Disponible"), ("ocupada", "Ocupada")],
        default="disponible"
    )

    def __str__(self):
        return f"Mesa {self.id} ({self.capacidad} personas)"


class Reserva(models.Model):
    ESTADOS = [("confirmada", "Confirmada"), ("cancelada", "Cancelada")]

    cliente = models.ForeignKey(Cliente, related_name='reservas', on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    numero_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default="confirmada")

    class Meta:
        unique_together = ('mesa', 'fecha', 'hora')  # Para evitar reservas dobles

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha} {self.hora}"

