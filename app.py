from flask import Flask, render_template, request, redirect, url_for, flash, session
from banco import cadastrar_usuario, verificar_login, registrar_operacao, obter_extrato, listar_usuarios, buscar_usuario_por_cpf

app = Flask(__name__)
app.secret_key = 'secreto123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        senha = request.form['senha']
        is_admin = request.form.get('admin') == 'on'

        if cadastrar_usuario(nome, data_nascimento, cpf, endereco, senha, is_admin):
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('CPF já cadastrado!', 'danger')

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']
        usuario = verificar_login(cpf, senha)

        if usuario:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!', 'success')
            if usuario.get("admin"):
                return redirect(url_for('dashboard'))
            return redirect(url_for('painel'))
        else:
            flash('CPF ou senha incorretos!', 'danger')

    return render_template('login.html')

@app.route('/painel', methods=['GET'])
def painel():
    if 'usuario' not in session:
        flash('Faça login para acessar o painel.', 'warning')
        return redirect(url_for('login'))

    usuario = session['usuario']

    # Verificar se é administrador
    if not usuario.get('admin', False):
        flash('Acesso negado: você não é administrador.', 'danger')
        return redirect(url_for('index'))

    cpf_busca = request.args.get('cpf')  # Obtém o CPF da query string

    if cpf_busca:
        usuarios_filtrados = [u for u in listar_usuarios() if cpf_busca in u['cpf']]
    else:
        usuarios_filtrados = listar_usuarios()

    return render_template('dashboard.html', usuario=usuario, usuarios=usuarios_filtrados, cpf_busca=cpf_busca)


@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session or not session['usuario'].get("admin"):
        flash('Acesso restrito ao administrador.', 'danger')
        return redirect(url_for('login'))

    cpf = request.args.get('cpf')
    if cpf:
        usuario = buscar_usuario_por_cpf(cpf)
        usuarios = [usuario] if usuario else []
    else:
        usuarios = listar_usuarios()

    return render_template('dashboard.html', usuarios=usuarios)

@app.route('/operacoes', methods=['GET', 'POST'])
def operacoes():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario']

    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = float(request.form['valor'])

        registrar_operacao(usuario['cpf'], tipo, valor)
        flash(f'{tipo.capitalize()} de R$ {valor:.2f} realizado com sucesso.', 'success')
        return redirect(url_for('operacoes'))

    extrato = obter_extrato(usuario['cpf'])
    return render_template('operacoes.html', usuario=usuario, extrato=extrato)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Logout efetuado.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
