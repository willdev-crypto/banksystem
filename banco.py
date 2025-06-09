import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_MOVIMENTACOES = "movimentacoes.json"
AGENCIA = '0001'

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r') as f:
            return json.load(f)
    return []

def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f, indent=4)

def carregar_movimentacoes():
    if os.path.exists(ARQUIVO_MOVIMENTACOES):
        with open(ARQUIVO_MOVIMENTACOES, 'r') as f:
            return json.load(f)
    return []

def salvar_movimentacoes():
    with open(ARQUIVO_MOVIMENTACOES, 'w') as f:
        json.dump(movimentacoes, f, indent=4)

usuarios = carregar_usuarios()
movimentacoes = carregar_movimentacoes()
contas = []

def cadastrar_usuario(nome, data_nascimento, cpf, endereco, senha, is_admin=False):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return False  # Usuário já existe

    senha_hash = generate_password_hash(senha)
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "senha": senha_hash,
        "admin": is_admin
    })
    salvar_usuarios()
    return True

def verificar_login(cpf, senha):
    for usuario in usuarios:
        if usuario["cpf"] == cpf and check_password_hash(usuario["senha"], senha):
            return usuario
    return None

def buscar_usuario_por_cpf(cpf):
    return next((u for u in usuarios if u['cpf'] == cpf), None)

def listar_usuarios():
    return usuarios

def registrar_operacao(cpf, tipo, valor):
    movimentacoes.append({
        "cpf": cpf,
        "tipo": tipo,
        "valor": valor
    })
    salvar_movimentacoes()

def obter_extrato(cpf):
    return [op for op in movimentacoes if op["cpf"] == cpf]
