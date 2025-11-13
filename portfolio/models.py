from django.db import models

class PortfolioItem(models.Model):
    prestador_profile = models.ForeignKey('accounts.PrestadorProfile', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='portfolio/')
    data_postagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or "Item sem título"
