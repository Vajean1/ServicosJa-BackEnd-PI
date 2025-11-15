from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator

User = get_user_model()

class Avaliacao(models.Model):
    servico_realizado = models.OneToOneField(
        'contratacoes.ServicoRealizado',
        on_delete=models.CASCADE,
        related_name='avaliacao',
    )
    nota = models.IntegerField(
        validators=[MinLengthValidator(1), MaxLengthValidator(2)]
    )
    comentario = models.TextField(blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('servico_realizado',)
        ordering = ['-data_criacao']
    
    def __str__(self):
        try:
            return f'Avaliação de {self.servico_realizado.client_user.email} para {self.servico_realizado.prestador_user.email} (Nota: {self.nota})'
        except:
            return f'Avaliação (ID: {self.id})'
