from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'usuarios'

urlpatterns = [
    path('nuevo/', views.NuevoUsuario.as_view(), name='nuevo'),
    path('municipios/', views.obtiene_municipios, name='municipios'),
    path('lista/', views.UsuariosList.as_view(), name='lista'),
    path('eliminar/<int:pk>', views.UsuariosEliminar.as_view(), name='eliminar'),
    path('editar/', views.UsuariosActualizar.as_view(), name='editar'),
    path('ver/<int:pk>', views.UsuariosDetalle.as_view(), name='ver'),
    path('login/', views.LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.NuevoUsuario.as_view(), name='signup'),
    path('activar/<slug:uid64>/<slug:token>', views.ActivarCuenta.as_view(), name='activar'),
    path('cambia-grupo/<int:id_gpo>/<int:id_usuario>', views.cambia_grupo, name='cambia-grupo'),
    path('modificar-grupos/<int:id>', views.modificar_usuario_grupo, name='modificar_usuario_grupo'),


]
