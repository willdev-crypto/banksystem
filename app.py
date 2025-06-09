from flask import Flask, render_template, request, redirect, url_for, flash, session
from banco import cadastrar_usuario, verificar_login
from banco import registrar_operacao, obter_extrato

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

        if cadastrar_usuario(nome, data_nascimento, cpf, endereco):
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('CPF já cadastrado!', 'danger')

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        usuario = verificar_login(cpf)

        if usuario:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('painel'))
        else:
            flash('CPF não encontrado!', 'danger')

    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'usuario' not in session:
        flash('Faça login para acessar o painel.', 'warning')
        return redirect(url_for('login'))

    usuario = session['usuario']
    return render_template('painel.html', usuario=usuario)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Logout efetuado.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

cpf = request.form['cpf']
senha = request.form['senha']
usuario = verificar_login(cpf, senha)

cpf = request.form['cpf']
senha = request.form['senha']
usuario = verificar_login(cpf, senha)

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