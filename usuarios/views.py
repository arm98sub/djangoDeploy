from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin
from django.contrib.messages.views import SuccessMessageMixin
from .token import token_activacion
from .models import Usuario, Municipio, Estado
from .forms import UsuarioForm
from django.contrib.auth.models import Group

class NuevoUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    # permission_required = 'usuarios.add_usuario'
    extra_context = {'etiqueta': ('Nuevo'), 
    'boton': ('Agregar'),
    'us_nuevo': True}
    success_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        dominio = get_current_site(self.request) #toma el dominio actual
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string('confirmar_cuenta.html',
            {
                'usuario': user,
                'dominio': dominio,
                'uid': uid,
                'token': token
            }
        )
        asunto = 'Activa cuenta videojuegos'
        to = user.email
        email = EmailMessage(
            asunto,
            mensaje,
            to=[to]
        )
        email.content_subtype = 'html'
        email.send()

        return super().form_valid(form)


def obtiene_municipios(PermissionRequiredMixin,request):
    # estado = get_object_or_404(Estado, id=id_estado)
    if request.method == 'GET':
        return JsonResponse({'error':'Petición incorrecta'}, safe=False,  status=403)
    id_estado = request.POST.get('id')
    municipios = Municipio.objects.filter(estado_id = id_estado)
    json = []
    if not municipios:
        json.append({'error':'No se encontrar municipios para ese estado'})
        
    for municipio in municipios:
        json.append({'id':municipio.id, 'nombre':municipio.nombre})
    return JsonResponse(json, safe=False)

class UsuariosList(PermissionRequiredMixin,ListView):
    paginate_by = 5
    permission_required = 'usuarios.view_usuario'
    model = Usuario
    lista_grupos = Group.objects.all()

    extra_context = {'us_lista' : True,
                    'lista_grupos': lista_grupos}
    template_name = 'usuarios:lista'

class UsuariosEliminar(PermissionRequiredMixin,DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios:lista')


class UsuariosActualizar(PermissionRequiredMixin, SuccessMessageMixin,UpdateView):
    # template_name = 'usuario_detail.html'
    model = Usuario
    permission_required = 'usuarios.edit_usuario'
    form_class = UsuarioForm
    extra_context = {'etiqueta': 'Actualizar', 'boton': 'Guardar'}
    success_url = reverse_lazy('usuarios:editar')
    success_message = "El usuario %(first_name)s se actualizo con exito"

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        obj = Usuario.objects.get(pk=pk)
        return obj

    # def get_success_url(self):
    #     pk = self.kwargs.get(self.pk_url_kwarg)
    #     url = reverse_lazy('usuarios:ver', kwargs={'pk':pk})
    #     return url

class UsuariosDetalle(PermissionRequiredMixin,DetailView):
    model = Usuario
    permission_required = 'usuarios.view_usuario'

class LoginUsuario(LoginView):
    template_name = 'login.html'
    #form_class = AuthenticationForm

    def get_success_url(self):
        self.request.session['cuantos'] = 0
        self.request.session['total'] = 0.0
        self.request.session['juegos'] = {}

        return super().get_success_url()

class ActivarCuenta(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs['uid64'])
            token = kwargs['token']
            user = Usuario.objects.get(id=uid)
        except:
            user = None

        if user and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Cuenta activada con éxito')
        else:
            messages.error(self.request, 'Token inválido, contacta al administrador')

        return redirect('usuarios:login')

def cambia_grupo(request,id_gpo, id_usuario):
    grupo = Group.objects.get(id= id_gpo)
    usuario = Usuario.objects.get(id= id_usuario)
    permission_required = 'usuarios.edit_usuario'
    if grupo in usuario.groups.all():
        if usuario.groups.count() <= 1: #
            messages.error(request, 'El usuario debe pertenecer a un grupo como minimo')
        else:
            usuario.groups.remove(grupo)
            messages.success(request, f'El usuario {usuario} ya no  pertenece al grupo {grupo}')

    else:
        usuario.groups.add(grupo)
        messages.success(request, f'El usuario {usuario} se agrego al grupo {grupo}')
    return redirect('usuarios:lista')


def modificar_usuario_grupo(request, id):
    
    grupos = [grupo.id for grupo in Group.objects.all()]
    usuario = Usuario.objects.get(id=id)
    usuario.groups.clear()
    permission_required = 'usuarios.edit_usuario'

    for item in request.POST:
        if request.POST[item] == 'on':
            usuario.groups.add(Group.objects.get(id=int(item)))

        messages.success(request, f'El usuario {usuario} pertenece al grupo')

    return redirect('usuarios:lista')
