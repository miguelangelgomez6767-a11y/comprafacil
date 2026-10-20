from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=150, verbose_name="Razón Social / Nombre")
    nit = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="NIT",
        help_text="Número de Identificación Tributaria único."
    )
    nombre_contacto = models.CharField(max_length=100, verbose_name="Nombre de Contacto")
    telefono = models.CharField(
        max_length=20, 
        verbose_name="Teléfono",
        validators=[RegexValidator(r'^[0-9+\s()-]+$', 'Ingrese un número de teléfono válido.')]
    )
    correo = models.EmailField(verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.razon_social} ({self.nit})"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['razon_social']


class Compra(models.Model):
    ESTADO_CHOICES = [
        ('registrada', 'Registrada'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]

    numero_compra = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Número de Compra"
    )
    proveedor = models.ForeignKey(
        Proveedor, 
        on_delete=models.PROTECT, 
        related_name='compras',
        verbose_name="Proveedor"
    )
    fecha_compra = models.DateField(verbose_name="Fecha de Compra")
    descripcion = models.TextField(verbose_name="Descripción de bienes o servicios")

    
    # NUEVO ATRIBUTO DE SUSTENTACIÓN (Texto opcional o detalles de soporte)
    sustentacion = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Sustentación"
    )


    valor_total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Valor Total",
        validators=[MinValueValidator(0.01, message="El valor total debe ser mayor que cero.")]
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='registrada', 
        verbose_name="Estado"
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='compras_registradas',
        verbose_name="Usuario que registró"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra #{self.numero_compra} - {self.proveedor.razon_social}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha_compra', '-id']