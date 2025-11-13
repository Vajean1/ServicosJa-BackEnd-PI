from django.contrib import admin
from .models import ServicoRealizado

@admin.register(ServicoRealizado)
class ServicoRealizadoAdmin(admin.ModelAdmin):
    list_display = ('cliente_user', 'prestador_user', 'servico', 'status', 'data_realizacao')
    list_filter = ('status', 'data_realizacao')
    search_fields = ('cliente_user__email', 'prestador_user__email')

    # Se atentar para quando fazer a view da api criar uma função para que seja possível somente o cliente alterar os status do serviço.
    def mudanca_de_status_cliente(self, request, obj=None):
        if obj and request.user == obj.client_user:
            return True
        return super().mudanca_de_status_cliente(request, obj)
    
    def prestador_nao_muda_status(self, request, obj=None):
        return False
