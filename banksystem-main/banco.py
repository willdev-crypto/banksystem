import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Arquivos
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_MOVIMENTACOES = "movimentacoes.json"

# Dados padrão
AGENCIA = '0001'

# ---------- Funções de Arquivo ----------

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r') as f:
            usuarios = json.load(f)
            # Valida e ajusta dados antigos
            for u in usuarios:
                u.setdefault('agencia', AGENCIA)
                u.setdefault('conta', f"{1234 + usuarios.index(u)}-{(5 + usuarios.index(u)) % 10}")
                u.setdefault('saldo', 0.0)
                u.setdefault('admin', False)
            return usuarios
    return []

def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f, indent=4)

def carregar_movimentacoes():
    if os.path.exists(ARQUIVO_MOVIMENTACOES):
        with open(ARQUIVO_MOVIMENTACOES, 'r') as f:
            dados = json.load(f)
            for mov in dados:
                mov.setdefault('data_hora', 'Data desconhecida')
                mov.setdefault('cpf', 'N/A')
                mov.setdefault('tipo', 'N/A')
                mov.setdefault('valor', 0.0)
            return dados
    return []


def salvar_movimentacoes():
    with open(ARQUIVO_MOVIMENTACOES, 'w') as f:
        json.dump(movimentacoes, f, indent=4)

# ---------- Dados na memória ----------
usuarios = carregar_usuarios()
movimentacoes = carregar_movimentacoes()

# ---------- Funções principais ----------

def cadastrar_usuario(nome, data_nascimento, cpf, endereco, email, senha, is_admin=False):
    if any(u["cpf"] == cpf for u in usuarios):
        return False

    senha_hash = generate_password_hash(senha)
    numero_conta = f"{1234 + len(usuarios)}-{(5 + len(usuarios)) % 10}"

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "email": email,
        "senha": senha_hash,
        "admin": is_admin,
        "agencia": AGENCIA,
        "conta": numero_conta,
        "saldo": 0.0
    })
    salvar_usuarios()
    return True

def verificar_login(cpf, senha):
    usuario = buscar_usuario_por_cpf(cpf)
    if usuario and check_password_hash(usuario["senha"], senha):
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
        "valor": valor,
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    salvar_movimentacoes()

def obter_extrato(cpf):
    return [op for op in movimentacoes if op["cpf"] == cpf]
