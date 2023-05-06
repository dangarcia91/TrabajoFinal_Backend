from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,User

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
    
    class CategoriasModel(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=100)
        estado = models.BooleanField(default=True)

        def __str__(self):
            return self.nombre

        class Meta:
            db_table = "categorias"

    class ProductosModel(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=100)
        descripcion = models.CharField(max_length=250)
        imagen_url = models.TextField()
        precio = models.FloatField()
        estado = models.BooleanField(default=True)
        categoria_id = models.ForeignKey(CategoriasModel, on_delete=models.CASCADE)

        def __str__(self):
            return self.nombre

        class Meta:
            db_table = "productos"

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
        usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)

        class Meta:
            db_table = "ventas"

    class DetallesVentaModel(models.Model):
        id = models.AutoField(primary_key=True)
        cantidad = models.IntegerField()
        producto_id = models.ForeignKey(ProductosModel, on_delete=models.CASCADE)
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

