from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db import transaction

# Create your views here.
class CategoriasView(generics.ListCreateAPIView):
    queryset = CategoriasModel.objects.all()
    serializer_class = CategoriasSerializer

class CategoriaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoriasModel.objects.all()
    serializer_class = CategoriasSerializer

    def delete(self, request, pk):
        self.serializer_class(self.get_queryset().get(id=pk)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductosView(generics.ListCreateAPIView):
    queryset = ProductosModel.objects.all()
    serializer_class = ProductosSerializer

class ProductoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductosModel.objects.all()
    serializer_class = ProductosSerializer

class PagosView(generics.ListCreateAPIView):
    queryset = PagosModel.objects.all()
    serializer_class = PagosSerializer

class PagoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PagosModel.objects.all()
    serializer_class = PagosSerializer

    def delete(self, request, pk):
        self.serializer_class(self.get_queryset().get(id=pk)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VentasView(generics.ListCreateAPIView):
    queryset = VentasModel.objects.all()
    serializer_class = VentasSerializer

    @transaction.atomic
    def post(self, request):
        try:
            cliente = ClientesModel(
                nombre=request.data['cliente']['nombre'],
                correo=request.data['cliente']['correo'],
                dni=request.data['cliente']['dni'],
            )
            cliente.save()

            usuario = User.objects.get(id=request.data['usuario_id'])
            venta = VentasModel(
                observacion=request.data['observacion'],
                usuario_id=usuario,
                cliente_id=cliente,
            )
            venta.save()

            for detalle in request.data['detalles_venta']:
                producto = ProductosModel.objects.get(id=detalle['producto_id'])
                detalle = DetallesVentaModel(
                    cantidad=detalle['cantidad'],
                    producto_id=producto,
                    venta_id=venta,
                )
                detalle.save()
            return Response({
                'message': 'Venta registrada correctamente'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)