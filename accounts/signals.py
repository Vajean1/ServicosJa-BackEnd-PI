from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from avaliacoes.models import Avaliacao
from contratacoes.models import ServicoRealizado
from .models import PrestadorProfile

#Isso aqui é para atualizar notas e não ficar preso ao cache.
@receiver([post_save, post_delete], sender=Avaliacao)
def atualizar_cache_avaliacao(sender, instance, **kwargs):
    prestador = instance.servico_realizado.prestaador_user
    profile = PrestadorProfile.objects.get(user=prestador)
    avaliacoes = Avaliacao.objects.filter(servico_realizado__prestador_user=prestador)
    total = avaliacoes.count()
    media = avaliacoes.aggregate(avg=models.Avg('nota'))['avg'] or 0
    profile.total_avaliacoes_cache = total
    profile.nota_media_cache = round(media, 2)
    profile.save()
