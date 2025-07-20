from flask import Flask, render_template, request, redirect, url_for, flash, session
from banco import buscar_usuario_por_cpf
from banco import (
    cadastrar_usuario, verificar_login, registrar_operacao,
    obter_extrato, listar_usuarios, buscar_usuario_por_cpf, salvar_usuarios
)
import re

app = Flask(__name__)
app.secret_key = 'secreto123'  # Troque por uma chave segura no deploy

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        email = request.form['email']
        senha = request.form['senha']
        is_admin = request.form.get('admin') == 'on'

        # Validação simples
        if not re.fullmatch(r'\d{11}', cpf):
            flash('CPF deve conter exatamente 11 dígitos numéricos.', 'danger')
            return render_template('cadastro.html')

        if '@' not in email:
            flash('E-mail inválido.', 'danger')
            return render_template('cadastro.html')

        # Verificar se já existe admin
        if is_admin and any(u.get('admin') for u in listar_usuarios()):
            flash('Já existe um administrador cadastrado.', 'danger')
            return render_template('cadastro.html')

        if cadastrar_usuario(nome, data_nascimento, cpf, endereco, email, senha, is_admin):
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('CPF já cadastrado.', 'danger')

    return render_template('cadastro.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']
        usuario = verificar_login(cpf, senha)

        if usuario:
            session['cpf'] = usuario['cpf']
            flash('Login realizado com sucesso!', 'success')
            if usuario.get('admin'):
                return redirect(url_for('dashboard'))
            return redirect(url_for('painel'))
        else:
            flash('CPF ou senha incorretos.', 'danger')

    return render_template('login.html')

@app.context_processor
def inject_functions():
    return dict(buscar_usuario_por_cpf=buscar_usuario_por_cpf)

# Painel do usuário comum
@app.route('/painel')
def painel():
    if 'cpf' not in session:
        flash('Faça login para acessar.', 'warning')
        return redirect(url_for('login'))

    usuario = buscar_usuario_por_cpf(session['cpf'])
    if usuario.get('admin'):
        flash('Acesso restrito para usuários.', 'danger')
        return redirect(url_for('dashboard'))

    extrato = obter_extrato(usuario['cpf'])
    return render_template('painel.html', usuario=usuario, extrato=extrato)

# Dashboard do administrador
@app.route('/dashboard')
def dashboard():
    if 'cpf' not in session:
        flash('Faça login como administrador.', 'warning')
        return redirect(url_for('login'))

    usuario = buscar_usuario_por_cpf(session['cpf'])
    if not usuario.get('admin'):
        flash('Acesso restrito ao administrador.', 'danger')
        return redirect(url_for('painel'))

    cpf_busca = request.args.get('cpf')
    if cpf_busca:
        usuarios_filtrados = [u for u in listar_usuarios() if cpf_busca in u['cpf']]
    else:
        usuarios_filtrados = listar_usuarios()

    return render_template('dashboard.html', usuario=usuario, usuarios=usuarios_filtrados, cpf_busca=cpf_busca)

# Operações bancárias (depósito e saque)
@app.route('/operacoes', methods=['GET', 'POST'])
def operacoes():
    if 'cpf' not in session:
        flash('Faça login.', 'warning')
        return redirect(url_for('login'))

    usuario = buscar_usuario_por_cpf(session['cpf'])

    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = float(request.form['valor'])

        if valor <= 0:
            flash('Valor precisa ser maior que zero.', 'danger')
            return redirect(url_for('operacoes'))

        if tipo == 'saque':
            senha_saque = request.form.get('senha_saque')
            if not senha_saque or not verificar_login(usuario['cpf'], senha_saque):
                flash('Senha incorreta para saque.', 'danger')
                return redirect(url_for('operacoes'))
            if usuario['saldo'] < valor:
                flash('Saldo insuficiente.', 'danger')
                return redirect(url_for('operacoes'))
            usuario['saldo'] -= valor
            registrar_operacao(usuario['cpf'], 'Saque', valor)
            flash(f'Saque de R$ {valor:.2f} realizado com sucesso.', 'success')

        elif tipo == 'deposito':
            usuario['saldo'] += valor
            registrar_operacao(usuario['cpf'], 'Depósito', valor)
            flash(f'Depósito de R$ {valor:.2f} realizado com sucesso.', 'success')

        else:
            flash('Operação inválida.', 'danger')
            return redirect(url_for('operacoes'))

        # Atualiza o saldo no JSON
        usuario_db = buscar_usuario_por_cpf(usuario['cpf'])
        if usuario_db:
            usuario_db['saldo'] = usuario['saldo']
            salvar_usuarios()

        return redirect(url_for('operacoes'))

    extrato = obter_extrato(usuario['cpf'])
    return render_template('operacoes.html', usuario=usuario, extrato=extrato)

# Logout
@app.route('/logout')
def logout():
    session.pop('cpf', None)
    flash('Logout efetuado.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
