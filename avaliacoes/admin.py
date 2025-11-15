from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente', 'get_prestador', 'nota', 'data_criacao')
    search_fields = (
        'servico_realizado__cliente_user__email', 
        'servico_realizado__prestador_user__email'
    )
    autocomplete_fields = ('servico_realizado',)

    @admin.display(description='Cliente')
    def get_cliente(self, obj):
        return obj.servico_realizado.cliente_user

    @admin.display(description='Prestador')
    def get_prestador(self, obj):
        return obj.servico_realizado.prestador_user
