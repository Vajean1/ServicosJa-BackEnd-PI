from django.contrib import admin
from .models import PortfolioItem

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('prestador_profile', 'data_postagem')
    list_filter = ('prestador_profile',)
    search_fields = ('prestador__user__email',)
    readonly_fields = ('data_postagem',)
