from django.contrib import admin
from django.urls import path
from core import views

admin.site.site_header = "TECNIMPOR CNC"

urlpatterns = [
    # Admin Django
    path('django-admin/', admin.site.urls),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),

    # Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/add/', views.cliente_add, name='cliente_add'),
    path('clientes/delete/<int:id>/', views.cliente_delete, name='cliente_delete'),
    # FUTURO
    # path('clientes/edit/<int:id>/', views.cliente_edit, name='cliente_edit'),  


    # Utilizadores
    path('utilizadores/', views.utilizadores_list, name='utilizadores_list'),
    path('utilizadores/add/', views.utilizador_add, name='utilizador_add'),
    path('utilizadores/delete/<int:id>/', views.utilizador_delete, name='utilizador_delete'),
    # FUTURO
    # path('utilizadores/edit/<int:id>/', views.utilizador_edit, name='utilizador_edit'),

    # Marcas
    path('marcas/', views.marcas_list, name='marcas_list'),
    path('marcas/add/', views.marca_add, name='marca_add'),
    path('marcas/delete/<int:id>/', views.marca_delete, name='marca_delete'),

    # Tipo Controlador
    path('tipo-controlador/', views.tipo_controlador_list, name='tipo_controlador_list'),
    path('tipo-controlador/add/', views.tipo_controlador_add, name='tipo_controlador_add'),
    path('tipo-controlador/delete/<int:id>/', views.tipo_controlador_delete, name='tipo_controlador_delete'),

    # Versão Controlador
    path('versao-controlador/', views.versao_controlador_list, name='versao_controlador_list'),
    path('versao-controlador/add/', views.versao_controlador_add, name='versao_controlador_add'),
    path('versao-controlador/delete/<int:id>/', views.versao_controlador_delete, name='versao_controlador_delete'),

    # Modelos
    path('modelos/', views.modelos_list, name='modelos_list'),
    path('modelos/add/', views.modelo_add, name='modelo_add'),
    path('modelos/delete/<int:id>/', views.modelo_delete, name='modelo_delete'),

    # Modelo + Controlador
    path('modelo-controlador/', views.modelo_controlador_list, name='modelo_controlador_list'),
    path('modelo-controlador/add/', views.modelo_controlador_add, name='modelo_controlador_add'),
    path('modelo-controlador/delete/<int:id>/', views.modelo_controlador_delete, name='modelo_controlador_delete'),

    # Equipamentos
    path('equipamentos/', views.equipamentos_list, name='equipamentos_list'),
    path('equipamentos/add/', views.equipamento_add, name='equipamento_add'),
    path('equipamentos/delete/<int:id>/', views.equipamento_delete, name='equipamento_delete'),
    # FUTURO
    # path('equipamentos/edit/<int:id>/', views.equipamento_edit, name='equipamento_edit'),

    # Senhas
    path('senhas/', views.senhas_list, name='senhas_list'),
    path('senhas/add/', views.senha_add, name='senha_add'),
    path('senhas/delete/<int:id>/', views.senha_delete, name='senha_delete'),
    # FUTURO
    # path('senhas/edit/<int:id>/', views.senha_edit, name='senha_edit'),  
    # path('senhas/disable/<int:id>/', views.senha_disable, name='senha_disable'),
    # path('senhas/history/<int:id>/', views.senha_history, name='senha_history'),

    # Histórico Senhas
    path('historico-senhas/', views.historico_senhas_list, name='historico_senhas_list'),

    # Países
    path('paises/', views.paises_list, name='paises_list'),
    path('paises/add/', views.pais_add, name='pais_add'),
    path('paises/delete/<int:id>/', views.pais_delete, name='pais_delete'),

    # AJAX
    path('ajax/cliente/', views.ajax_add_cliente, name='ajax_add_cliente'),
    path('ajax/marca/', views.ajax_add_marca, name='ajax_add_marca'),
    path('ajax/modelo/', views.ajax_add_modelo, name='ajax_add_modelo'),
    path('ajax/tipo-controlador/', views.ajax_add_tipo_controlador, name='ajax_add_tipo_controlador'),
    path('ajax/modelos-por-marca/<int:marca_id>/', views.ajax_modelos_por_marca, name='ajax_modelos_por_marca'),
    path('ajax/versoes-por-tipo/<int:tipo_id>/', views.ajax_versoes_por_tipo, name='ajax_versoes_por_tipo'),
    path('ajax/modelo-controlador/<int:modelo_id>/<int:versao_id>/', views.ajax_modelo_controlador, name='ajax_modelo_controlador'),
    path('ajax/versao-controlador/', views.ajax_add_versao_controlador, name='ajax_add_versao_controlador'),
    path('ajax/preview-senha/', views.ajax_preview_senha, name='ajax_preview_senha'),
    path('ajax/verificar-senha-ativa/', views.ajax_verificar_senha_ativa, name='ajax_verificar_senha_ativa'),
]
