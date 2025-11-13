from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ServicoRealizado(models.Model):
    cliente_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos_contratados')
    prestador_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos_prestados')
    servico = models.ForeignKey('servicos.Servico', on_delete=models.CASCADE)
    data_realizacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')],
        default='pendente'
    )

