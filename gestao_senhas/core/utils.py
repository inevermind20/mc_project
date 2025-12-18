import hashlib
from datetime import datetime
from .models import Senha

def gerar_senha_sha256(equipamento, tipo_senha='alfanumerica', comprimento=12):
    """
    Gera senha SHA-256 baseada em dados do equipamento

    Args:
        equipamento: Objeto Equipamento
        tipo_senha: 'alfanumerica' (default) ou 'numerica'
        comprimento: Tamanho da senha (default: 12)

    Returns:
        str: Senha única
    """

    # Dados base para hash
    cliente = equipamento.cliente
    modelo = equipamento.modelo_controlador.modelo
    marca = modelo.marca
    dados = f"{cliente.nif}{marca.nome}{modelo.nome}{equipamento.numero_serie}"

    # Gerar hash SHA-256
    hash_obj = hashlib.sha256(dados.encode('utf-8'))
    hash_hex = hash_obj.hexdigest().upper()

    # Extrair senha conforme tipo
    if tipo_senha == 'numerica':
        # Só dígitos
        senha_base = ''.join([c for c in hash_hex if c.isdigit()])
        # Se não houver dígitos suficientes, converter A-F para 0-5
        if len(senha_base) < comprimento:
            for char in hash_hex:
                if len(senha_base) >= comprimento:
                    break
                if char in 'ABCDEF':
                    senha_base += str(ord(char) - 65)
                elif char.isdigit():
                    senha_base += char
        senha = senha_base[:comprimento]
    else:
        # Alfanumérico (padrão)
        senha = hash_hex[:comprimento]

    # Validar unicidade
    tentativa = 0
    senha_final = senha

    while Senha.objects.filter(senha=senha_final).exists():
        tentativa += 1
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        dados_timestamp = f"{dados}{timestamp}{tentativa}"

        hash_obj = hashlib.sha256(dados_timestamp.encode('utf-8'))
        hash_hex = hash_obj.hexdigest().upper()

        if tipo_senha == 'numerica':
            senha_base = ''.join([c for c in hash_hex if c.isdigit()])
            if len(senha_base) < comprimento:
                for char in hash_hex:
                    if len(senha_base) >= comprimento:
                        break
                    if char in 'ABCDEF':
                        senha_base += str(ord(char) - 65)
                    elif char.isdigit():
                        senha_base += char
            senha_final = senha_base[:comprimento]
        else:
            senha_final = hash_hex[:comprimento]

        if tentativa > 100:
            raise ValueError('Não foi possível gerar senha única após 100 tentativas')

    return senha_final


def preview_senha_sha256(nif, marca, modelo, numero_serie, tipo_senha='alfanumerica', comprimento=12):
    """
    Preview de senha sem salvar (para AJAX)
    """
    dados = f"{nif}{marca}{modelo}{numero_serie}"
    hash_obj = hashlib.sha256(dados.encode('utf-8'))
    hash_hex = hash_obj.hexdigest().upper()

    if tipo_senha == 'numerica':
        senha_base = ''.join([c for c in hash_hex if c.isdigit()])
        if len(senha_base) < comprimento:
            for char in hash_hex:
                if len(senha_base) >= comprimento:
                    break
                if char in 'ABCDEF':
                    senha_base += str(ord(char) - 65)
                elif char.isdigit():
                    senha_base += char
        senha = senha_base[:comprimento]
    else:
        senha = hash_hex[:comprimento]

    return {
        'senha': senha,
        'hash': hash_hex,
        'dados': dados
    }
