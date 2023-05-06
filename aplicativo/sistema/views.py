from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import SoloClientes
from cloudinary import uploader

class RegistroUsuario(APIView):
    def post(self, request: Request):
        serializador= RegistroUsuarioSerializer(data = request.data)
        if serializador.is_valid():
            password = serializador.validated_data.get('password')
            nuevo_usuario = Usuario(**serializador.validated_data)
            nuevo_usuario.set_password(password)

            nuevo_usuario.save()

            return Response(data={
                'message': 'Usuario creado exitosamente'
                
            }, status=status.HTTP_201_CREATED)
        
        else:
            return Response(data={
                'message': 'Error al crear el usuario',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class Perfilusuario(generics.GenericAPIView):
    serializer_class = Personserializer

    def get(self, request: Request):
        print(request.user)
        print(request.auth)
        usuarios = Usuario.objects.all()
        serializador = Personserializer(usuarios, many=True)
        return Response(data = {
            'content': serializador.data
        }, status=status.HTTP_200_OK)
    
class ProductoView(generics.GenericAPIView):
    serializer_class = ProductoSerializer
    Permission_classes = [IsAuthenticated]
    
    def post(self, request: Request):
        try:
            data = {
                'nombre': request.data.get('nombre'),
                'foto': request.FILES.get('foto'),
                'precio': request.data.get('precio'),
                'estado': request.data.get('estado'),    
            }
            data_serializada = ProductoSerializer(data=data)
            if data_serializada.is_valid():
                data_serializada.save()

                return Response(data= {
                    'message': 'Producto creado exitosamente',
                    'content': data_serializada.data
                }, status=status.HTTP_201_CREATED)
            else:
                print(data_serializada.errors)
                return Response(data={
                    'message': 'Error al crear producto',
                    'content': data_serializada.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
                print(serializador.error)
            
        except Exception as e:
            return Response(data={
                'message': 'Error al crear producto',
                'content': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request:Request):
        productos = Producto.objects.all()
        serializador = ProductoSerializer(productos, many=True)

        return Response(data = {
            'content': serializador.data
        }, status=status.HTTP_200_OK)
    
# VIDEO: minuto 1:18

#login: 1:53 minutos - JSON Web Token
# pip install djangorestframework-simplejwt
# pip install cloudinary
# 1:58:44
# Views Mascota: 3:08:00