from django.contrib import admin
from .models import ServicoRealizado

@admin.register(ServicoRealizado)
class ServicoRealizadoAdmin(admin.ModelAdmin):
    list_display = ('cliente_user', 'prestador_user', 'servico', 'data_realizacao')
    list_filter = ('data_realizacao',)
    search_fields = ('cliente_user__email', 'prestador_user__email')