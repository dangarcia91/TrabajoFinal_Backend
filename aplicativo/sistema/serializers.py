from rest_framework.serializers import ModelSerializer
from .models import *

class RegistroUsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class Personserializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'tipoUsuario']

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
    
    def to_representation(self, instance):
        representacion = super().to_representation(instance)
        representacion['foto'] = instance.foto.url
        return representacion