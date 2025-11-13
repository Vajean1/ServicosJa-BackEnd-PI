from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from datetime import date
import requests

#Api do CEP e Nominatim para pegar as coordenadas diretas do usuário

def pegar_latitude_longitude_do_endereco(cep, rua, numero):
    try:
        cep = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        cep_data = cep.json()
        
        if "erro" in cep:
            return None, None
        
        endereco = f"{rua}, {numero}, {cep_data['localidade']}, {cep_data['uf']}"

        url = 'https://nominatim.openstreetmap.org/search'

        parametros = {
            "q" : endereco,
            "format" : "json",
            "limit" : 1,
        } 

        headers = {
            'User-Agent' : 'ServicosJa/1.0'
        }

        response = requests.get(url, params=parametros, headers=headers)
        data = response.json()

        if data:
            return float(data[0]['lat'], float(data[0]['lon']))
        
        return None, None
    
    except Exception as error:
        print(error)
        return None, None

class User(AbstractUser):
    email = models.EmailField(unique=True)
    dt_nascimento = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    #isso é principalmente para o createsuperuser, mas lá no serializer precisa adicionar um campo de requerimento do email e dt nascimento e etc!
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #Atentar para colocar campo necessário no serializer.
    @property
    def idade(self):

        if not self.dt_nascimento:
            return 'Não informado.'

        hoje = date.today()
        idade = hoje.year - self.dt_nascimento.year
        if (hoje.month, hoje.day) < (self.dt_nascimento.month, self.dt_nascimento.day):
            idade -= 1
        return idade

class ClienteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone_contato = models.CharField(max_length=20, blank=True)
    cep = models.CharField(max_length=9, blank=True)
    rua = models.CharField(max_length=150, blank=True)
    numero_casa = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PrestadorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)
    telefone_publico = models.CharField(max_length=20)
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=150)
    numero_casa = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
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
        
        if self.cep and self.rua and self.numero_casa and not self.latitude:
            lat, lon = pegar_latitude_longitude_do_endereco(self.cep, self.rua, self.numero_casa)
            
            if lat and lon:
                self.latitude = lat
                self.longitude = lon
        super().save(*args, **kwargs)
