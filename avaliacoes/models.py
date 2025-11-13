
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Avaliacao(models.Model):
    cliente_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_dadas')
    prestador_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente_user', 'prestador_user')
        indexes = [
            models.Index(fields=['prestador_user'], name='idx_prestador_avaliacoes'),
        ]
