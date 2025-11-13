from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from avaliacoes.models import Avaliacao
from contratacoes.models import ServicoRealizado
from .models import PrestadorProfile

#Isso aqui é para atualizar notas e não ficar preso ao cache.
@receiver([post_save, post_delete], sender=Avaliacao)
def atualizar_cache_avaliacao(sender, instance, **kwargs):
    profile = PrestadorProfile.objects.get(user=instance.prestador_user)
    avaliacoes = Avaliacao.objects.filter(prestador_user=instance.prestador_user)
    total = avaliacoes.count()
    media = avaliacoes.aggregate(avg=models.Avg('nota'))['avg'] or 0
    profile.total_avaliacoes_cache = total
    profile.nota_media_cache = round(media, 2)
    profile.save()

@receiver(post_save, sender=ServicoRealizado)
def atualizar_cache_servicos(sender, instance, **kwargs):
    if instance.status == 'concluido':
        profile = PrestadorProfile.objects.get(user=instance.prestador_user)
        profile.total_servicos_cache += 1
        profile.save()
