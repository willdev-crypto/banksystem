import datetime

usuarios = []
contas = []
AGENCIA = '0001'


def listar_usuarios():
    if usuarios:
        print('\n=== Usuários Cadastrados ===')
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']} - CPF: {usuario['cpf']}")
        print('============================')
    else:
        print('Nenhum usuário cadastrado.')


def criar_usuario():
    nome = input('Nome: ')
    data_nascimento = input('Data de Nascimento (dd/mm/aaaa): ')
    cpf = input('CPF (apenas números): ')

    
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print('CPF já cadastrado! Não foi possível criar o usuário.')
        return

    endereco = input('Endereço (logradouro, número, cidade/estado): ')

    usuario = {'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco}
    usuarios.append(usuario)
    print('Usuário criado com sucesso!')


def verificar_cpf():
    cpf = input('Informe o CPF para verificar: ')
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print('CPF já cadastrado no sistema.')
    else:
        print('CPF não encontrado.')


def validar_usuario():
    while True:
        print("Digite 0 para sair e reiniciar o sistema.")
        cpf = input('Informe o CPF para acessar o sistema: ')
        if cpf == '0':
            print('Saindo e reiniciando o sistema...')
            return None
        usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
        if usuario:
            print(f'Bem-vindo, {usuario["nome"]}!')
            return usuario
        else:
            print('Usuário não encontrado! Tente novamente.')


def criar_conta():
    cpf = input('Informe o CPF do usuário: ')
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    if not usuario:
        print('Usuário não encontrado!')
        return

    numero_conta = len(contas) + 1
    conta = {'agencia': AGENCIA, 'numero': numero_conta, 'usuario': usuario}
    contas.append(conta)
    print(f'Conta {numero_conta} criada com sucesso!')


def listar_contas():
    if contas:
        print('\n=== Contas Cadastradas ===')
        for conta in contas:
            print(f"Agência: {conta['agencia']} - Conta: {conta['numero']} - Titular: {conta['usuario']['nome']}")
        print('==========================')
    else:
        print('Nenhuma conta cadastrada.')


def deposito(valor, /):
    if valor > 0:
        return valor
    print('Valor inválido para depósito!')
    return 0


def saque(*, saldo, valor, extrato, limite_saques):
    if valor > saldo:
        print('Saldo insuficiente!')
    elif valor > 500:
        print('Limite de saque excedido!')
    elif limite_saques >= 3:
        print('Número máximo de saques excedido!')
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
        return saldo, extrato
    else:
        print('Valor inválido para saque!')
    return saldo, extrato


def extrato(saldo, /, *, extrato):
    print('\n=== EXTRATO ===')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'Saldo: R$ {saldo:.2f}')
    print('================')


def menu_bancario(usuario):
    saldo = 0
    extrato_str = ''
    limite_saques = 0

    menu = '''
    [a] Criar Conta
    [l] Listar Contas
    [u] Listar Usuários
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair do Sistema Bancário

    => '''

    while True:
        opcao = input(menu).lower()

        if opcao == 'a':
            criar_conta()
        elif opcao == 'l':
            listar_contas()
        elif opcao == 'u':
            listar_usuarios()
        elif opcao == 'd':
            try:
                valor = float(input('Valor do depósito: '))
                saldo += deposito(valor)
            except ValueError:
                print('Por favor, insira um valor numérico válido.')
        elif opcao == 's':
            try:
                valor = float(input('Valor do saque: '))
                saldo, extrato_str = saque(saldo=saldo, valor=valor, extrato=extrato_str, limite_saques=limite_saques)
                limite_saques += 1
            except ValueError:
                print('Por favor, insira um valor numérico válido.')
        elif opcao == 'e':
            extrato(saldo, extrato=extrato_str)
        elif opcao == 'q':
            print('Saindo do sistema bancário...')
            break
        else:
            print('Opção inválida!')

# Função principal
def main():
    while True:
        print('\nBem-vindo(a) ao Bank System!')
        print('[c] Criar Usuário')
        print('[v] CPF Cadastrado')
        print('[e] Ver Conta e detalhes')
        print('[q] Sair')
        opcao = input('Escolha uma opção: ').lower()

        if opcao == 'c':
            criar_usuario()
        elif opcao == 'v':
            verificar_cpf()
        elif opcao == 'e':
            usuario = validar_usuario()
            if usuario:
                menu_bancario(usuario)
        elif opcao == 'q':
            print('Saindo da sua conta...')
            break
        else:
            print('Opção inválida! Tente novamente.')

if __name__ == '__main__':
    main()
