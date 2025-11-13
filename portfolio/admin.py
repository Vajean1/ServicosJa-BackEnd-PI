from django.contrib import admin
from .models import PortfolioItem

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('prestador_profile', 'titulo', 'data_postagem')
    list_filter = ('prestador_profile',)
    search_fields = ('titulo', 'descricao')