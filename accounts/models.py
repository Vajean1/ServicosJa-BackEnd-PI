from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.forms import ValidationError
import requests
from geopy.geocoders import Nominatim

#Api do CEP e Nominatim para pegar as coordenadas diretas do usuário

import requests
from geopy.geocoders import Nominatim
from typing import Optional, Tuple

def pegar_latitude_longitude_do_endereco(
    cep: str,
    rua: str,
    numero: str | int
) -> Tuple[Optional[float], Optional[float], str]:

    try:
        cep = "".join(filter(str.isdigit, str(cep)))

        data = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
        if "erro" in data:
            return None, None, "CEP inválido"

        cidade = data["localidade"]
        uf = data["uf"]
        bairro = data.get("bairro")

        geolocator = Nominatim(user_agent="ServicosJa/1.0", timeout=10)

        endereco1 = f"{rua}, {numero}, {cidade}, {uf}, Brasil"
        loc = geolocator.geocode(endereco1)
        if loc:
            return loc.latitude, loc.longitude, "endereco_exato"

        endereco2 = f"{rua}, {cidade}, {uf}, Brasil"
        loc = geolocator.geocode(endereco2)
        if loc:
            return loc.latitude, loc.longitude, "rua_aproximada"

        if bairro:
            endereco3 = f"{bairro}, {cidade}, {uf}, Brasil"
            loc = geolocator.geocode(endereco3)
            if loc:
                return loc.latitude, loc.longitude, "bairro_aproximado"

        endereco4 = f"{cidade}, {uf}, Brasil"
        loc = geolocator.geocode(endereco4)
        if loc:
            return loc.latitude, loc.longitude, "cidade_aproximada"

        return None, None, "nao_encontrado"

    except Exception:
        return None, None, "erro"

class User(AbstractUser):

    TIPO_USUARIO_ESCOLHA = [
        ('cliente', 'Cliente'),
        ('prestador', 'Prestador de Serviço'),
        ]

    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_ESCOLHA, null=True, blank=True)
    email = models.EmailField(unique=True)
    dt_nascimento = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    #isso é principalmente para o createsuperuser, mas lá no serializer precisa adicionar um campo de requerimento do email e dt nascimento e etc!
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #Atentar para colocar campo necessário no serializer.
    @property
    def idade(self) -> int:

        if not self.dt_nascimento:
            return 'Não informado.'

        hoje = date.today()
        idade = hoje.year - self.dt_nascimento.year
        if (hoje.month, hoje.day) < (self.dt_nascimento.month, self.dt_nascimento.day):
            idade -= 1
        return idade

    def clean(self):
        if self.tipo_usuario == 'cliente' and hasattr(self, 'perfil_prestador'):
            raise ValidationError("Este usuário já é prestador.")
        if self.tipo_usuario == 'prestador' and hasattr(self, 'perfil_cliente'):
            raise ValidationError("Este usuário já é cliente.")
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    telefone_contato = models.BigIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999999999999)],
        help_text='Apenas dígitos; máximo 13 dígitos.'
    )
    cep = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
    rua = models.CharField(max_length=150, blank=True)
    numero_casa = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PrestadorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_prestador')
    biografia = models.TextField(blank=True)
    telefone_publico = models.BigIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999999999999)],
        help_text='Apenas dígitos; máximo 13 dígitos.'
    )
    cep = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
    rua = models.CharField(max_length=150)
    numero_casa = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    disponibilidade = models.BooleanField(default=False, help_text='Disponibilidade de horário 24 horas?')
    possui_material_proprio = models.BooleanField(default=False)
    atende_fim_de_semana = models.BooleanField(default=False)
    raio_atendimento_km = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    foto_perfil = models.ImageField(upload_to='perfil_prestadores/', null=True, blank=True)
    nota_media_cache = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_avaliacoes_cache = models.PositiveIntegerField(default=0)
    acessos_perfil = models.PositiveIntegerField(default=0)
    total_servicos_cache = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    servicos = models.ManyToManyField(
        'servicos.Servico',
        related_name='prestadores'
    )

    class Meta:
        indexes = [
            models.Index(fields=['cep'], name='idx_cep'),
            models.Index(fields=['latitude', 'longitude'], name='idx_geo'),
        ]
    
    def save(self, *args, **kwargs):
        
        if self.cep and self.rua and self.numero_casa :
            if self.pk:
                antigo = PrestadorProfile.objects.get(pk=self.pk)
                if (antigo.cep != self.cep or antigo.rua != self.rua or antigo.numero_casa != self.numero_casa):
                    lat, lon =pegar_latitude_longitude_do_endereco(self.cep, self.rua, self.numero_casa)
                    self.latitude = lat
                    self.longitude = lon
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"
