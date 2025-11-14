from django.db import models

class PortfolioItem(models.Model):
    prestador_profile = models.ForeignKey('accounts.PrestadorProfile', on_delete=models.CASCADE, related_name='portfolio')
    imagem = models.ImageField(upload_to='portfolio/')
    data_postagem = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_postagem']

    def __str__(self):
        return f'Foto de {self.prestador_profile.user.get_full_name()} - {self.data_postagem.date()}'

