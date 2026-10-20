from django import forms
from .models import Proveedor, Compra

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social', 'nit', 'nombre_contacto', 'telefono', 'correo', 'direccion']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_razon_social'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nit'}),
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nombre_contacto'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_telefono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_correo'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_direccion'}),
        }

    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        query = Proveedor.objects.filter(nit=nit)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("Ya existe un proveedor registrado con este NIT.")
        return nit


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        # Se añade 'sustentacion' en los campos del formulario
        fields = ['numero_compra', 'proveedor', 'fecha_compra', 'descripcion', 'sustentacion', 'valor_total', 'estado']
        widgets = {
            'numero_compra': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_numero_compra'}),
            'proveedor': forms.Select(attrs={'class': 'form-select', 'id': 'id_proveedor'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_compra'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_descripcion'}),
            # Widget agregado para la sustentación
            'sustentacion': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_sustentacion'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_valor_total'}),
            'estado': forms.Select(attrs={'class': 'form-select', 'id': 'id_estado'}),
        }

    def clean_numero_compra(self):
        numero_compra = self.cleaned_data.get('numero_compra')
        query = Compra.objects.filter(numero_compra=numero_compra)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise forms.ValidationError("Ya existe una compra registrada con este número.")
        return numero_compra

    def clean_valor_total(self):
        valor_total = self.cleaned_data.get('valor_total')
        if valor_total is not None and valor_total <= 0:
            raise forms.ValidationError("El valor total debe ser un número mayor que cero.")
        return valor_total