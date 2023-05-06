from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cloudinary.models import CloudinaryField

# Create your models here.
class EdiciónUsuario(BaseUserManager):
    def create_superuser(self, correo, nombre, apellido, password, tipoUsuario):
        if not correo:
            raise ValueError('El usuario debe tener un correo')

        correo_normalizado = self.normalize_email(correo)
        
        nuevo_usuario = self.model(correo = correo_normalizado, nombre = nombre, apellido = apellido, tipoUsuario = tipoUsuario)

        nuevo_usuario.set_password(password)
        nuevo_usuario.is_superuser = True
        nuevo_usuario.is_staff = True

        nuevo_usuario.save()

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)

    nombre = models. TextField(null=False)
    apellido = models.TextField(null=False)
    correo = models.EmailField(max_length=100, unique=True, null=False)
    password = models.TextField(null=False)
    tipoUsuario = models.TextField(choices=[('ADMIN', 'ADMIN'), ('CLIENTE', 'CLIENTE')], db_column='tipo_usuario')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'

    REQUIRED_FIELDS = ['nombre', 'apellido', 'tipoUsuario']

    objects = EdiciónUsuario()

    class Meta:
        db_table = 'usuarios' 

class Categoria(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.TextField(null=False)
    habilitado = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categorias'

class Producto(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.TextField(null=False)
    foto = CloudinaryField('foto')
    precio = models.FloatField()
    estado = models.BooleanField()
    # categoria_id = models.ForeignKey(to=Usuario, on_delete=models.CASCADE)

    # cliente = models.ForeignKey(to=Usuario, on_delete=models.RESTRICT, db_column='cliente_id')
#     def __str__(self) -> str:
#         return self.nombre
    class Meta:
        db_table = 'productos'

class ClientesModel(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    dni = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "clientes"

class VentasModel(models.Model):
    id = models.AutoField(primary_key=True)
    observacion = models.CharField(max_length=100)
    cliente_id = models.ForeignKey(ClientesModel, on_delete=models.CASCADE)
    # usuario_id = models.ForeignKey(ClientesModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "ventas"

class DetallesVentaModel(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta_id = models.ForeignKey(VentasModel, on_delete=models.CASCADE, related_name='detallesVenta')

    class Meta:
        db_table = "detalles_venta"

class PagosModel(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.FloatField()
    estado = models.BooleanField(default=True)
    venta_id = models.ForeignKey(VentasModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "pagos"