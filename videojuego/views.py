from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Videojuego, Venta, DetalleVenta
from .forms import CategoriaForm, VideojuegoForm
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count
from django_weasyprint import WeasyTemplateResponseMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin
from datetime import date
from datetime import datetime

from videojuegos import settings

def lista_categoria(PermissionRequiredMixin,request):
    permission_required = 'usuarios.view_usuario'
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def eliminar_categoria(PermissionRequiredMixin,request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('categoria:lista')

def nuevo_categoria(PermissionRequiredMixin,request):
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria:lista')
    context = {'form': form }
    return render(request, 'nuevo_categoria.html', context)

def editar_categoria(PermissionRequiredMixin,request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria:lista')
    context = {'form': form }
    return render(request, 'editar_categoria.html', context)


class VideojuegoList(PermissionRequiredMixin,ListView):
    permission_required = 'usuarios.view_usuario'
    paginate_by = 5
    model = Videojuego

    

class VideojuegoEliminar(PermissionRequiredMixin,DeleteView):
    model = Videojuego
    permission_required = 'usuarios.edit_usuario'
    success_url = reverse_lazy('videojuego:lista')

class VideojuegoCrear(PermissionRequiredMixin,CreateView):
    model = Videojuego
    permission_required = 'usuarios.edit_usuario'
    form_class = VideojuegoForm
    extra_context = {'etiqueta': 'Nuevo','boton': 'Agregar',  'vj_nuevo':True}
    success_url = reverse_lazy('videojuego:lista')

class VideojuegoActualizar(PermissionRequiredMixin,UpdateView):
    permission_required = 'usuarios.edit_usuario'
    model = Videojuego
    
    form_class = VideojuegoForm
    extra_context = {'etiqueta': 'Actualizar', 'boton': 'Guardar'}
    success_url = reverse_lazy('videojuego:lista')

class VideojuegoDetalle(PermissionRequiredMixin,DetailView):
    model = Videojuego
    permission_required = 'usuarios.view_usuario'


class Grafica(PermissionRequiredMixin,TemplateView):
    permission_required = 'usuarios.view_usuario'
    template_name = 'grafica.html'

    def get(self, request, *args, **kwargs):
        juegos_cat = Videojuego.objects.all().values('categoria').annotate(cuantos = Count('categoria'))
        categorias = Categoria.objects.all()

        datos = []
        for categoria in categorias:
            cuantos = 0
            for catjue in juegos_cat:
                if catjue['categoria'] == categoria.id:
                    cuantos = catjue['cuantos']
                    break
            datos.append({'name':categoria.nombre, 'data':[cuantos]})

        self.extra_context = {'datos': datos}
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



class VistaPDF(ListView):
    model = Videojuego
    template_name = 'videojuego_pdf.html'

    def get(self, request,*args, **kwargs):
        suma = 0
        for videojuego in Videojuego.objects.all():
            suma += videojuego.precio
        extra_content = {'suma':suma}


class ListaVideojuegosPDF(WeasyTemplateResponseMixin,VistaPDF):
    pdf_stylesheet = [
        settings.STATICFILES_DIRS[0] + 'css/boostrap.min.css',
    ]
    pdf_attachment = False
    pdf_filename = 'juegos.pdf'

class VistaDetallesPDF(DetailView):
    model = Videojuego
    template_name = 'videojuegoDetalles_pdf.html'


class DetalleJuegoPdf(WeasyTemplateResponseMixin,VistaDetallesPDF):
    pdf_stylesheet = [
        settings.STATICFILES_DIRS[0] + 'css/boostrap.min.css',
    ]
    pdf_attachment = False
    pdf_filename = 'detalles.pdf'

def comprar(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)
    if juego.stock > 0:
        juego.stock = juego.stock - 1
        juego.save() 

        id = str(pk)

        request.session['total'] = request.session['total'] + float(juego.precio)
        request.session['cuantos'] = request.session['cuantos'] + 1

        if id in request.session['juegos']:
            request.session['juegos'][id]['cantidad'] = request.session['juegos'][id]['cantidad'] + 1
        else:
            request.session['juegos'][id] = {'precio':float(juego.precio), 'cantidad':1}

    return redirect('videojuego:lista')

def detalleVenta(request):
    # juego = get_object_or_404(Videojuego, pk=pk)
    # detalle = get_object_or_404(DetalleVenta)
    # # detalle.articulo = Vide

    # print()
    return render(request, 'detalle_venta.html')

    
    




