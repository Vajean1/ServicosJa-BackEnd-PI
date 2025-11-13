from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('cliente_user', 'prestador_user', 'nota', 'data_criacao')
    list_filter = ('nota', 'data_criacao')
    search_fields = ('cliente_user__email', 'prestador_user__email')

