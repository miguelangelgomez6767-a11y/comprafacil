from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Proveedor, Compra
from .forms import ProveedorForm, CompraForm

@login_required
def home(request):
    total_proveedores = Proveedor.objects.count()
    total_compras = Compra.objects.count()
    compras_recientes = Compra.objects.all()[:5]
    context = {
        'total_proveedores': total_proveedores,
        'total_compras': total_compras,
        'compras_recientes': compras_recientes,
    }
    return render(request, 'compras/home.html', context)

# ==================== PROVEEDORES ====================

@login_required
def proveedor_list(request):
    query = request.GET.get('q', '')
    proveedores = Proveedor.objects.all()
    if query:
        proveedores = proveedores.filter(razon_social__icontains=query) | proveedores.filter(nit__icontains=query)
    return render(request, 'compras/proveedor_list.html', {'proveedores': proveedores, 'query': query})

@login_required
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor registrado exitosamente.')
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'compras/proveedor_form.html', {'form': form, 'titulo': 'Registrar Proveedor'})

@login_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'compras/proveedor_form.html', {'form': form, 'titulo': 'Editar Proveedor'})

@login_required

@require_POST


def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if proveedor.compras.exists():
        messages.error(request, 'No se puede eliminar el proveedor porque tiene compras asociadas.')
    else:
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado correctamente.')
    return redirect('proveedor_list')


# ==================== COMPRAS ====================

@login_required
def compra_list(request):
    compras = Compra.objects.all()
    proveedor_id = request.GET.get('proveedor')
    estado = request.GET.get('estado')

    if proveedor_id:
        compras = compras.filter(proveedor_id=proveedor_id)
    if estado:
        compras = compras.filter(estado=estado)

    proveedores = Proveedor.objects.all()
    context = {
        'compras': compras,
        'proveedores': proveedores,
        'proveedor_seleccionado': proveedor_id,
        'estado_seleccionado': estado,
    }
    return render(request, 'compras/compra_list.html', context)

@login_required
def compra_create(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user
            compra.save()
            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('compra_list')
    else:
        form = CompraForm()
    return render(request, 'compras/compra_form.html', {'form': form, 'titulo': 'Registrar Compra'})

@login_required
def compra_update(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compra actualizada exitosamente.')
            return redirect('compra_list')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'compras/compra_form.html', {'form': form, 'titulo': 'Editar Compra'})

@login_required

@require_POST
def compra_delete(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    compra.delete()
    messages.success(request, 'Compra eliminada correctamente.')
    return redirect('compra_list')
@login_required
def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    compras_proveedor = proveedor.compras.all()
    return render(request, 'compras/proveedor_detail.html', {
        'proveedor': proveedor,
        'compras_proveedor': compras_proveedor
    })

@login_required
def compra_detail(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    return render(request, 'compras/compra_detail.html', {'compra': compra})