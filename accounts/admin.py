from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClienteProfile, PrestadorProfile, pegar_latitude_longitude_do_endereco

#Aqui mostra nossos models de banco de dados direto na página de admin.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'idade', 'is_active')

    def get_idade(self, obj):
        return obj.idade
    
    get_idade.short_description = 'Idade'

    list_filter = ('is_active', 'date_joined')
    search_fields = ('email', 'first_name')


@admin.register(ClienteProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone_contato', 'cep', 'rua')
    search_fields = ('user__email', 'cep')

@admin.register(PrestadorProfile)
class PrestadorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone_publico', 'cep', 'nota_media_cache', 'total_avaliacoes_cache')
    search_fields = ('user__email', 'cep')
    filter_horizontal = ('servicos',)
    
    readonly_fields = (
        'nota_media_cache',
        'total_avaliacoes_cache',
        'acessos_perfil',
        'total_servicos_cache',
        'latitude',
        'longitude',
        'created_at',
        'updated_at',
    )
    #forçar salvar a latitude e longitude
    def save_model(self, request, obj, form, change):
        if obj.cep and obj.rua and obj.numero_casa:
            lat, lon = pegar_latitude_longitude_do_endereco(obj.cep, obj.rua, obj.numero_casa)
            obj.latitude = lat
            obj.longitude = lon
        
        super().save_model(request, obj, form, change)
