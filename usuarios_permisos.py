import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videojuegos.settings')
django.setup()


from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from usuarios.models import Usuario, Estado, Municipio

grupo_administradores = Group.objects.create(name = 'administradores35')
grupo_usuarios = Group.objects.create(name = 'usuarios35')

content_type= ContentType.objects.get_for_model(Usuario)

permiso_usuarios = Permission.objects.create(
    codename = 'permiso_usuario35',
    name = 'Permiso requerido para el grupo usuarios',
    content_type = content_type
)

permiso_administradores = Permission.objects.create(
    codename = 'permiso_administradores35',
    name = 'Permiso requerido para el grupo administradores',
    content_type = content_type
)

grupo_usuarios.permissions.add(permiso_usuarios)
grupo_administradores.permissions.add(permiso_administradores)


administrador = Usuario.objects.create_user('alan199@gmail.com',password='alan123')
administrador.groups.add(grupo_administradores)


Usuario.objects.create_superuser('admina@asa.mx',password='admin123')
