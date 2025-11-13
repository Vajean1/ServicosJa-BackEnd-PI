from django.contrib import admin
from .models import CategoriaServico, Servico, PrestadorServicos

@admin.register(CategoriaServico)
class CategoriaServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'created_at')
    list_filter = ('categoria',)
    search_fields = ('nome',)

@admin.register(PrestadorServicos)
class PrestadorServicosAdmin(admin.ModelAdmin):
    list_display = ('prestador_profile', 'servico')
    list_filter = ('prestador_profile', 'servico')
