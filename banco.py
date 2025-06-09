import json
import os

AGENCIA = '0001'

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_MOVIMENTACOES = "movimentacoes.json"

# Funções para carregar e salvar dados
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

# Carregando dados ao iniciar o programa
usuarios = carregar_usuarios()
movimentacoes = carregar_movimentacoes()
contas = []  # Contas podem ser implementadas com persistência depois, se desejar

# Funções do sistema

def cadastrar_usuario(nome, data_nascimento, cpf, endereco, senha):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return False  # Usuário já existe

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "senha": senha
    })
    salvar_usuarios()  # Salva os dados atualizados
    return True

def verificar_login(cpf, senha):
    for usuario in usuarios:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            return usuario
    return None

def listar_usuarios():
    return usuarios

def criar_usuario(nome, data_nascimento, cpf, endereco):
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        return False, 'CPF já cadastrado!'

    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(usuario)
    salvar_usuarios()
    return True, 'Usuário criado com sucesso!'

def verificar_cpf(cpf):
    return any(usuario['cpf'] == cpf for usuario in usuarios)

def buscar_usuario_por_cpf(cpf):
    return next((u for u in usuarios if u['cpf'] == cpf), None)

def criar_conta(cpf):
    usuario = buscar_usuario_por_cpf(cpf)
    if not usuario:
        return False, 'Usuário não encontrado!'

    numero_conta = len(contas) + 1
    conta = {
        'agencia': AGENCIA,
        'numero': numero_conta,
        'usuario': usuario
    }
    contas.append(conta)
    # Se quiser salvar contas, precisará implementar persistência similar
    return True, f'Conta {numero_conta} criada com sucesso!'

def listar_contas():
    return contas

def deposito(valor):
    if valor > 0:
        return valor, 'Depósito realizado com sucesso!'
    return 0, 'Valor inválido para depósito!'

def saque(saldo, valor, extrato, limite_saques):
    if valor > saldo:
        return saldo, extrato, limite_saques, 'Saldo insuficiente!'
    elif valor > 500:
        return saldo, extrato, limite_saques, 'Limite de saque excedido!'
    elif limite_saques >= 3:
        return saldo, extrato, limite_saques, 'Número máximo de saques excedido!'
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        limite_saques += 1
        return saldo, extrato, limite_saques, f'Saque de R$ {valor:.2f} realizado com sucesso!'
    else:
        return saldo, extrato, limite_saques, 'Valor inválido para saque!'

def extrato_bancario(saldo, extrato):
    return extrato if extrato else 'Não foram realizadas movimentações.', saldo

# Registrar operações financeiras (depósito, saque)
def registrar_operacao(cpf, tipo, valor):
    movimentacoes.append({
        "cpf": cpf,
        "tipo": tipo,
        "valor": valor
    })
    salvar_movimentacoes()

def obter_extrato(cpf):
    return [op for op in movimentacoes if op["cpf"] == cpf]
