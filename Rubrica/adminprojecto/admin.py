from django.contrib import admin
from adminprojecto.models import Cliente
from adminprojecto.models import Mesa
from adminprojecto.models import Reserva

admin.site.register(Cliente)
admin.site.register(Mesa)
admin.site.register(Reserva)