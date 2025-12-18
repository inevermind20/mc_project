from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q

from .models import *
from .forms import SenhaForm
from .utils import gerar_senha_sha256, preview_senha_sha256

import json


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            try:
                usuario = Usuario.objects.get(email=username)
                user = authenticate(request, username=usuario.username, password=password)
            except Usuario.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciais inválidas')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user

    # Viewer vê só seus equipamentos
    if user.perfil == 'viewer':
        total_equipamentos = Equipamento.objects.filter(cliente=user.empresa_cliente).count()
        total_senhas = Senha.objects.filter(equipamento__cliente=user.empresa_cliente, ativa=True).count()
    else:
        total_equipamentos = Equipamento.objects.count()
        total_senhas = Senha.objects.filter(ativa=True).count()

    stats = {
        'total_clientes': Cliente.objects.count(),
        'total_equipamentos': total_equipamentos,
        'total_senhas': total_senhas,
        'total_usuarios': Usuario.objects.count(),
    }

    return render(request, 'dashboard.html', stats)


# === CLIENTES ===

@login_required
def clientes_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/list.html', {'clientes': clientes})


@login_required
def cliente_add(request):
    # Apenas user/admin/superadmin podem adicionar
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão para adicionar clientes')
        return redirect('clientes_list')

    if request.method == 'POST':
        try:
            Cliente.objects.create(
                nif=request.POST['nif'],
                designacao_social=request.POST['designacao_social'],
                designacao_comercial=request.POST.get('designacao_comercial', ''),
                pais_id=request.POST['pais'],
                email=request.POST.get('email', ''),
                telefone=request.POST.get('telefone', ''),
                morada=request.POST.get('morada', '')
            )
            messages.success(request, 'Cliente criado com sucesso!')
            return redirect('clientes_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    paises = Pais.objects.all()
    return render(request, 'clientes/add.html', {'paises': paises})


@login_required
def cliente_delete(request, id):
    # Apenas superadmin pode remover
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return JsonResponse({'success': True})


# === UTILIZADORES ===

@login_required
def utilizadores_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'utilizadores/list.html', {'usuarios': usuarios})


@login_required
def utilizador_add(request):
    # Apenas admin/superadmin podem adicionar
    if request.user.perfil not in ['admin', 'superadmin']:
        messages.error(request, 'Sem permissão para adicionar utilizadores')
        return redirect('utilizadores_list')

    if request.method == 'POST':
        try:
            tipo_empresa = request.POST.get('tipo_empresa')
            empresa_cliente_id = request.POST.get('empresa_cliente') if tipo_empresa == 'cliente' else None

            Usuario.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                perfil=request.POST.get('perfil', 'viewer'),
                tipo_empresa=tipo_empresa,
                empresa_cliente_id=empresa_cliente_id
            )

            messages.success(request, 'Utilizador criado com sucesso!')
            return redirect('utilizadores_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    clientes = Cliente.objects.all()
    return render(request, 'utilizadores/add.html', {'clientes': clientes})


@login_required
def utilizador_delete(request, id):
    # Admin e superadmin podem remover
    if request.user.perfil not in ['admin', 'superadmin']:
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return JsonResponse({'success': True})


# === EQUIPAMENTOS ===

@login_required
def equipamentos_list(request):
    user = request.user

    # Viewer vê só equipamentos da sua empresa
    if user.perfil == 'viewer':
        equipamentos = Equipamento.objects.filter(cliente=user.empresa_cliente)
    else:
        equipamentos = Equipamento.objects.all()

    return render(request, 'equipamentos/list.html', {'equipamentos': equipamentos})


@login_required
def equipamento_add(request):
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão')
        return redirect('equipamentos_list')

    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            modelo_controlador_id = request.POST.get('modelo_controlador')
            numero_serie = request.POST.get('numero_serie')
            notas = request.POST.get('notas', '')

            if not all([cliente_id, modelo_controlador_id, numero_serie]):
                messages.error(request, 'Preencha todos os campos obrigatórios!')
                return redirect('equipamento_add')

            # Se modelo_controlador_id for "criar", criar combinação
            if modelo_controlador_id == 'criar':
                modelo_id = request.POST.get('modelo')
                versao_id = request.POST.get('versao_controlador')
                mc = ModeloControlador.objects.create(
                    modelo_id=modelo_id,
                    versao_controlador_id=versao_id
                )
                modelo_controlador_id = mc.id

            Equipamento.objects.create(
                cliente_id=cliente_id,
                modelo_controlador_id=modelo_controlador_id,
                numero_serie=numero_serie,
                notas=notas
            )

            messages.success(request, f'Equipamento {numero_serie} criado com sucesso!')
            return redirect('equipamentos_list')

        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
            return redirect('equipamento_add')

    # GET - carregar todos dados para dropdowns
    context = {
        'clientes': Cliente.objects.all().order_by('designacao_social'),
        'marcas': Marca.objects.all().order_by('nome'),
        'modelos': Modelo.objects.all().order_by('nome'),
        'tipos_controlador': TipoControlador.objects.all().order_by('nome'),
        'versoes_controlador': VersaoControlador.objects.all().order_by('versao'),
        'modelos_controladores': ModeloControlador.objects.all(),
        'paises': Pais.objects.all().order_by('designacao'),
    }

    return render(request, 'equipamentos/add.html', context)


@login_required
def equipamento_delete(request, id):
    # Apenas superadmin pode remover
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    equipamento = get_object_or_404(Equipamento, id=id)
    equipamento.delete()
    return JsonResponse({'success': True})


# === SENHAS ===

@login_required
def senhas_list(request):
    user = request.user

    # Viewer vê só senhas dos seus equipamentos
    if user.perfil == 'viewer':
        senhas = Senha.objects.filter(equipamento__cliente=user.empresa_cliente)
    else:
        senhas = Senha.objects.all()

    return render(request, 'senhas/list.html', {'senhas': senhas})


@login_required
def senha_add(request):
    """Gerador SHA-256 com tipo de senha automático"""

    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão para gerar senhas')
        return redirect('senhas_list')

    if request.method == 'POST':
        try:
            # Equipamento escolhido no formulário
            equipamento = get_object_or_404(Equipamento, id=request.POST['equipamento'])

            # 1) Verificar se já existe senha permanente ativa
            hoje = timezone.now().date()
            senha_permanente = Senha.objects.filter(
                equipamento=equipamento,
                ativa=True,
                tipo='definitiva',
            ).order_by('-criado_em_data', '-criado_em_hora').first()

            # 2) Verificar se já existe temporária ativa e dentro da validade
            senha_temporaria = Senha.objects.filter(
                equipamento=equipamento,
                ativa=True,
                tipo='temporaria',
                data_fim__gte=hoje,
            ).order_by('-criado_em_data', '-criado_em_hora').first()

            if senha_permanente or senha_temporaria:
                senha_ativa = senha_permanente or senha_temporaria
                tipo_label = 'permanente' if senha_ativa == senha_permanente else 'temporária'
                msg = f'Este equipamento já tem uma senha {tipo_label} ativa ({senha_ativa.senha}).'
                messages.error(request, msg)
                return redirect('senhas_list')

            # Obter tipo de senha do controlador
            tipo_controlador = equipamento.modelo_controlador.versao_controlador.tipo_controlador
            tipo_senha = tipo_controlador.tipo_senha

            # Comprimento
            comprimento = int(request.POST.get('comprimento', 12))
            if comprimento < 6 or comprimento > 16:
                comprimento = 12

            # Gerar senha SHA-256
            senha_valor = gerar_senha_sha256(equipamento, tipo_senha, comprimento)

            # Criar senha
            senha = Senha.objects.create(
                equipamento=equipamento,
                senha=senha_valor,
                tipo=request.POST.get('tipo', 'temporaria'),
                data_inicio=request.POST.get('data_inicio'),
                data_fim=request.POST.get('data_fim') or None,
                criado_por=request.user,
                criado_em_data=timezone.now().date(),
                criado_em_hora=timezone.now().time(),
            )

            # Registrar histórico
            HistoricoSenha.objects.create(
                senha=senha,
                acao='criacao',
                usuario=request.user,
                data=timezone.now().date(),
                hora=timezone.now().time(),
                detalhes=f"Gerada por SHA-256 ({tipo_senha})"
            )

            messages.success(request, f'✅ Senha {senha_valor} gerada com sucesso!')
            return redirect('senhas_list')

        except Exception as e:
            messages.error(request, f'❌ Erro ao gerar senha: {str(e)}')
            return redirect('senha_add')

    # GET
    equipamentos = Equipamento.objects.all().select_related(
        'cliente',
        'modelo_controlador__modelo__marca',
        'modelo_controlador__versao_controlador__tipo_controlador'
    ).order_by('cliente__designacao_social')

    return render(request, 'senhas/add.html', {'equipamentos': equipamentos})


@login_required
def senha_delete(request, id):
    # Apenas superadmin pode remover
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    senha = get_object_or_404(Senha, id=id)
    senha.delete()
    return JsonResponse({'success': True})


# === PERFIL ===

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')

        # Email editável só por admin/superadmin
        if user.perfil in ['admin', 'superadmin']:
            user.email = request.POST.get('email', '')

        # Password
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, 'Perfil atualizado!')
        return redirect('dashboard')

    return render(request, 'editar_perfil.html')


# === AJAX PARA POP-UPS (clientes/marcas/modelos/etc.) ===

@login_required
def ajax_add_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nif=data['nif'],
                designacao_social=data['designacao_social'],
                pais_id=data['pais']
            )
            return JsonResponse({'success': True, 'id': cliente.id, 'nome': str(cliente)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def ajax_add_marca(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            marca = Marca.objects.create(nome=data['nome'])
            return JsonResponse({'success': True, 'id': marca.id, 'nome': str(marca)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def ajax_modelos_por_marca(request, marca_id):
    modelos = Modelo.objects.filter(marca_id=marca_id)
    return JsonResponse({'modelos': [{'id': m.id, 'nome': m.nome} for m in modelos]})


@login_required
def ajax_versoes_por_tipo(request, tipo_id):
    versoes = VersaoControlador.objects.filter(tipo_controlador_id=tipo_id)
    return JsonResponse({'versoes': [{'id': v.id, 'versao': v.versao} for v in versoes]})


@login_required
def ajax_modelo_controlador(request, modelo_id, versao_id):
    try:
        mc = ModeloControlador.objects.get(modelo_id=modelo_id, versao_controlador_id=versao_id)
        return JsonResponse({'exists': True, 'id': mc.id, 'nome': str(mc)})
    except:
        return JsonResponse({'exists': False})


@login_required
def ajax_add_tipo_controlador(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo = TipoControlador.objects.create(nome=data['nome'])
            return JsonResponse({'success': True, 'id': tipo.id, 'nome': str(tipo)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required
def ajax_add_versao_controlador(request):
    data = json.loads(request.body)
    versao = VersaoControlador.objects.create(
        tipo_controlador_id=data['tipo_controlador_id'],
        versao=data['versao']
    )
    return JsonResponse({'success': True, 'id': versao.id})


@login_required
def ajax_add_modelo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            modelo = Modelo.objects.create(
                marca_id=data['marca_id'],
                nome=data['nome']
            )
            return JsonResponse({'success': True, 'id': modelo.id, 'nome': str(modelo)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


# === MARCAS ===

@login_required
def marcas_list(request):
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão')
        return redirect('dashboard')

    marcas = Marca.objects.all()
    return render(request, 'gestao/marcas_list.html', {'items': marcas})


@login_required
def marca_add(request):
    if request.user.perfil not in ['user', 'admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('marcas_list')

    if request.method == 'POST':
        try:
            Marca.objects.create(nome=request.POST['nome'])
            messages.success(request, 'Marca criada com sucesso!')
            return redirect('marcas_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    return render(request, 'gestao/marca_add.html')


@login_required
def marca_delete(request, id):
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    try:
        Marca.objects.filter(id=id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# === TIPO CONTROLADOR ===

@login_required
def tipo_controlador_add(request):
    if request.user.perfil not in ['user', 'admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('tipo_controlador_list')

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            tipo_senha = request.POST.get('tipo_senha', 'alfanumerica')

            if not nome:
                messages.error(request, 'Nome é obrigatório!')
                return render(request, 'gestao/tipo_controlador_add.html')

            TipoControlador.objects.create(
                nome=nome.strip(),
                tipo_senha=tipo_senha
            )

            messages.success(request, f'Tipo de Controlador "{nome}" criado com sucesso!')
            return redirect('tipo_controlador_list')

        except Exception as e:
            messages.error(request, f'Erro ao criar: {str(e)}')

    return render(request, 'gestao/tipo_controlador_add.html')


@login_required
def tipo_controlador_list(request):
    """Listar tipos de controlador"""
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão')
        return redirect('dashboard')

    tipos = TipoControlador.objects.all()
    return render(request, 'gestao/tipo_controlador_list.html', {'items': tipos})


@login_required
def tipo_controlador_delete(request, id):
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    try:
        TipoControlador.objects.filter(id=id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# === VERSÃO CONTROLADOR ===

@login_required
def versao_controlador_list(request):
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão')
        return redirect('dashboard')

    versoes = VersaoControlador.objects.all()
    return render(request, 'gestao/versao_controlador_list.html', {'items': versoes})


@login_required
def versao_controlador_add(request):
    if request.user.perfil not in ['user', 'admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('versao_controlador_list')

    if request.method == 'POST':
        try:
            VersaoControlador.objects.create(
                tipo_controlador_id=request.POST['tipo_controlador'],
                versao=request.POST['versao']
            )
            messages.success(request, 'Versão de Controlador criada!')
            return redirect('versao_controlador_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    tipos = TipoControlador.objects.all()
    return render(request, 'gestao/versao_controlador_add.html', {'tipos': tipos})


@login_required
def versao_controlador_delete(request, id):
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    try:
        VersaoControlador.objects.filter(id=id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# === MODELOS ===

@login_required
def modelos_list(request):
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão')
        return redirect('dashboard')

    modelos = Modelo.objects.all()
    return render(request, 'gestao/modelos_list.html', {'items': modelos})


@login_required
def modelo_add(request):
    if request.user.perfil not in ['user', 'admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('modelos_list')

    if request.method == 'POST':
        try:
            Modelo.objects.create(
                marca_id=request.POST['marca'],
                nome=request.POST['nome']
            )
            messages.success(request, 'Modelo criado!')
            return redirect('modelos_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    marcas = Marca.objects.all()
    return render(request, 'gestao/modelo_add.html', {'marcas': marcas})


@login_required
def modelo_delete(request, id):
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    try:
        Modelo.objects.filter(id=id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# === MODELO + CONTROLADOR ===

@login_required
def modelo_controlador_list(request):
    if request.user.perfil == 'viewer':
        messages.error(request, 'Sem permissão')
        return redirect('dashboard')

    mc = ModeloControlador.objects.all()
    return render(request, 'gestao/modelo_controlador_list.html', {'items': mc})


@login_required
def modelo_controlador_add(request):
    if request.user.perfil not in ['user', 'admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('modelo_controlador_list')

    if request.method == 'POST':
        try:
            ModeloControlador.objects.create(
                modelo_id=request.POST['modelo'],
                versao_controlador_id=request.POST['versao_controlador']
            )
            messages.success(request, 'Modelo+Controlador criado!')
            return redirect('modelo_controlador_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    modelos = Modelo.objects.all()
    versoes = VersaoControlador.objects.all()
    return render(request, 'gestao/modelo_controlador_add.html', {
        'modelos': modelos,
        'versoes': versoes
    })


@login_required
def modelo_controlador_delete(request, id):
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    try:
        ModeloControlador.objects.filter(id=id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# === PAÍSES ===

@login_required
def paises_list(request):
    if request.user.perfil not in ['admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('dashboard')

    paises = Pais.objects.all()
    return render(request, 'gestao/paises_list.html', {'items': paises})


@login_required
def pais_add(request):
    if request.user.perfil not in ['admin', 'superadmin']:
        messages.error(request, 'Sem permissão')
        return redirect('paises_list')

    if request.method == 'POST':
        try:
            Pais.objects.create(
                codigo=request.POST['codigo'],
                designacao=request.POST['designacao']
            )
            messages.success(request, 'País criado!')
            return redirect('paises_list')
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')

    return render(request, 'gestao/pais_add.html')


@login_required
def pais_delete(request, id):
    if request.user.perfil != 'superadmin':
        return JsonResponse({'success': False, 'error': 'Sem permissão'})

    try:
        Pais.objects.filter(id=id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# === HISTÓRICO SENHAS ===

@login_required
def historico_senhas_list(request):
    if request.user.perfil != 'superadmin':
        messages.error(request, 'Sem permissão - Apenas SuperAdmin')
        return redirect('dashboard')

    historico = HistoricoSenha.objects.all()
    return render(request, 'gestao/historico_senhas_list.html', {'items': historico})


# === AJAX PREVIEW SENHA ===

@login_required
def ajax_preview_senha(request):
    """Preview SHA-256 em tempo real"""

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            equipamento_id = data.get('equipamento_id')
            comprimento = int(data.get('comprimento', 12))

            equipamento = Equipamento.objects.select_related(
                'cliente',
                'modelo_controlador__modelo__marca',
                'modelo_controlador__versao_controlador__tipo_controlador'
            ).get(id=equipamento_id)

            tipo_senha = equipamento.modelo_controlador.versao_controlador.tipo_controlador.tipo_senha

            resultado = preview_senha_sha256(
                equipamento.cliente.nif,
                equipamento.modelo_controlador.modelo.marca.nome,
                equipamento.modelo_controlador.modelo.nome,
                equipamento.numero_serie,
                tipo_senha,
                comprimento
            )

            return JsonResponse({
                'success': True,
                'senha': resultado['senha'],
                'hash': resultado['hash'],
                'dados': resultado['dados'],
                'tipo_senha': tipo_senha
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método não permitido'})


# === AJAX VERIFICAR SENHA ATIVA ===

@login_required
def ajax_verificar_senha_ativa(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})

    try:
        data = json.loads(request.body)
        equipamento_id = data.get('equipamento_id')

        equipamento = Equipamento.objects.get(id=equipamento_id)
        hoje = timezone.now().date()

        senha_permanente = Senha.objects.filter(
            equipamento=equipamento,
            ativa=True,
            tipo='definitiva',
        ).order_by('-criado_em_data', '-criado_em_hora').first()

        senha_temporaria = Senha.objects.filter(
            equipamento=equipamento,
            ativa=True,
            tipo='temporaria',
            data_fim__gte=hoje,
        ).order_by('-criado_em_data', '-criado_em_hora').first()

        senha_ativa = senha_permanente or senha_temporaria

        if not senha_ativa:
            return JsonResponse({'success': True, 'tem_ativa': False})

        tipo = 'permanente' if senha_ativa == senha_permanente else 'temporaria'

        return JsonResponse({
            'success': True,
            'tem_ativa': True,
            'tipo': tipo,
            'senha': senha_ativa.senha,
            'data_inicio': senha_ativa.data_inicio.strftime('%d-%m-%Y'),
            'data_fim': senha_ativa.data_fim.strftime('%d-%m-%Y') if senha_ativa.data_fim else None,
            'senha_id': senha_ativa.id,
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
