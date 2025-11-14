from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ServicoRealizado(models.Model):
    #Como não vai ter mais status, o serviço é concluído assim que é realizado.
    cliente_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos_contratados')
    prestador_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos_prestados')
    servico = models.ForeignKey('servicos.Servico', on_delete=models.CASCADE)
    data_realizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_realizacao']
    
    def __str__(self):
        return f'{self.cliente_user} -> {self.prestador_user} ({self.servico})'
