from django.db import models

class CategoriaServico(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(CategoriaServico, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['categoria'], name='idx_categoria'),
        ]

    def __str__(self):
        return self.nome

class PrestadorServicos(models.Model):
    prestador_profile = models.ForeignKey('accounts.PrestadorProfile', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prestador_profile', 'servico')
        verbose_name = 'Serviço do prestador'
        verbose_name_plural = "Prestador - Serviços"
