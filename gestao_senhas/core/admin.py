from django.contrib import admin
from .models import *

admin.site.register(Pais)
admin.site.register(Cliente)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(TipoControlador)
admin.site.register(VersaoControlador)
admin.site.register(ModeloControlador)
admin.site.register(Equipamento)
admin.site.register(Senha)
admin.site.register(HistoricoSenha)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'perfil', 'tipo_empresa', 'empresa_cliente')
    list_filter = ('perfil', 'tipo_empresa')
