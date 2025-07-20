from banco import (
    criar_usuario, verificar_cpf, buscar_usuario_por_cpf, criar_conta,
    listar_contas, listar_usuarios, deposito, saque, extrato_bancario
)


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
    [q] Sair

    => '''

    while True:
        opcao = input(menu).lower()

        if opcao == 'a':
            cpf = input('Informe o CPF do usuário: ')
            sucesso, msg = criar_conta(cpf)
            print(msg)
        elif opcao == 'l':
            contas = listar_contas()
            for conta in contas:
                print(f"{conta['agencia']} {conta['numero']} - {conta['usuario']['nome']}")
        elif opcao == 'u':
            usuarios = listar_usuarios()
            for usuario in usuarios:
                print(f"{usuario['nome']} - {usuario['cpf']}")
        elif opcao == 'd':
            try:
                valor = float(input('Valor do depósito: '))
                val, msg = deposito(valor)
                saldo += val
                print(msg)
            except ValueError:
                print('Valor inválido.')
        elif opcao == 's':
            try:
                valor = float(input('Valor do saque: '))
                saldo, extrato_str, limite_saques, msg = saque(saldo, valor, extrato_str, limite_saques)
                print(msg)
            except ValueError:
                print('Valor inválido.')
        elif opcao == 'e':
            extrato_texto, saldo_atual = extrato_bancario(saldo, extrato_str)
            print('\n=== EXTRATO ===')
            print(extrato_texto)
            print(f'Saldo: R$ {saldo_atual:.2f}')
        elif opcao == 'q':
            break
        else:
            print('Opção inválida.')


def main():
    while True:
        print('\nBem-vindo ao Bank System CLI')
        print('[c] Criar Usuário')
        print('[v] Verificar CPF')
        print('[e] Entrar com CPF')
        print('[q] Sair')

        opcao = input('Escolha uma opção: ').lower()

        if opcao == 'c':
            nome = input('Nome: ')
            data = input('Data de Nascimento (dd/mm/aaaa): ')
            cpf = input('CPF: ')
            endereco = input('Endereço: ')
            sucesso, msg = criar_usuario(nome, data, cpf, endereco)
            print(msg)
        elif opcao == 'v':
            cpf = input('CPF: ')
            print('CPF encontrado!' if verificar_cpf(cpf) else 'CPF não cadastrado.')
        elif opcao == 'e':
            cpf = input('CPF para login: ')
            usuario = buscar_usuario_por_cpf(cpf)
            if usuario:
                print(f'Bem-vindo, {usuario["nome"]}')
                menu_bancario(usuario)
            else:
                print('Usuário não encontrado.')
        elif opcao == 'q':
            break
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    main()
