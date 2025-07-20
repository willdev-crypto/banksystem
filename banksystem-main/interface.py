from banco import (
    listar_usuarios,
    buscar_usuario_por_cpf,
    obter_extrato,
    movimentacoes
)
from getpass import getpass
from werkzeug.security import check_password_hash


def admin_login():
    print("\n🔐 Login de Administrador CLI 🔐")
    cpf = input("CPF do administrador: ")
    senha = getpass("Senha: ")

    usuario = buscar_usuario_por_cpf(cpf)
    if usuario and usuario.get('admin'):
        if check_password_hash(usuario['senha'], senha):
            print(f"\n✅ Bem-vindo, {usuario['nome']}! Acesso concedido ao painel administrativo.\n")
            return usuario
        else:
            print("❌ Senha incorreta.")
    else:
        print("❌ CPF não encontrado ou não é um administrador.")
    return None


def menu_admin(usuario):
    while True:
        print("\n=== Painel Administrativo CLI ===")
        print("[1] Listar usuários")
        print("[2] Consultar dados de um usuário")
        print("[3] Ver extrato de um usuário")
        print("[4] Ver todas as movimentações")
        print("[5] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n📜 Lista de Usuários:")
            usuarios = listar_usuarios()
            for u in usuarios:
                status = "Administrador" if u.get('admin') else "Cliente"
                print(f"➡️ {u['nome']} | CPF: {u['cpf']} | Conta: {u.get('agencia', 'N/A')}-{u.get('conta', 'N/A')} | Saldo: R$ {u.get('saldo', 0.00):.2f} | {status}")

        elif opcao == '2':
            cpf = input("Informe o CPF do usuário: ")
            u = buscar_usuario_por_cpf(cpf)
            if u:
                status = "Administrador" if u.get('admin') else "Cliente"
                print(f"""
🔍 Dados do Usuário:
➡️ Nome: {u['nome']}
➡️ CPF: {u['cpf']}
➡️ Data de Nascimento: {u['data_nascimento']}
➡️ Endereço: {u['endereco']}
➡️ E-mail: {u['email']}
➡️ Agência: {u.get('agencia', 'N/A')}
➡️ Conta: {u.get('conta', 'N/A')}
➡️ Saldo: R$ {u.get('saldo', 0.00):.2f}
➡️ Tipo: {status}
""")
            else:
                print("❌ Usuário não encontrado.")

        elif opcao == '3':
            cpf = input("Informe o CPF do usuário: ")
            extrato = obter_extrato(cpf)
            if extrato:
                print("\n📜 Extrato do usuário:")
                for e in extrato:
                    print(f"{e['data_hora']} | {e['tipo'].capitalize()} | R$ {e['valor']:.2f}")
            else:
                print("⚠️ Nenhuma movimentação encontrada para esse CPF.")

        elif opcao == '4':
            print("\n📜 Todas as movimentações do sistema:")
            if movimentacoes:
                for e in movimentacoes:
                    print(f"{e.get('data_hora', 'Data desconhecida')} | CPF: {e.get('cpf', 'N/A')} | {e.get('tipo', 'N/A').capitalize()} | R$ {e.get('valor', 0.00):.2f}")

            else:
                print("⚠️ Nenhuma movimentação registrada no sistema.")

        elif opcao == '5':
            print("Encerrando painel administrativo CLI...")
            break

        else:
            print("❌ Opção inválida.")


def main():
    print("=== Admin CLI Bank System ===")
    usuario = admin_login()
    if usuario:
        menu_admin(usuario)


if __name__ == "__main__":
    main()
