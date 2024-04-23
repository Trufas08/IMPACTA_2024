from flask import Flask, render_template, request, redirect, session
from models.database import Database

app = Flask(__name__)
app.secret_key = 'SENHA-MUITO-SECRETA'

db = Database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    msg = ''
    if request.method == 'POST':
        usuario = request.form['usuario'].lower().replace(' ', '')
        senha = request.form['senha'].replace(' ', '')
        email = request.form['email'].lower().replace(' ', '')

        if usuario and senha and email:
            if not db.email_existe(email) and not db.usuario_existe(usuario):
                db.cadastrar_usuario(usuario, email, senha)
                msg = "Cadastro realizado com sucesso!"
            elif db.email_existe(email) and db.usuario_existe(usuario):
                msg = "E-mail e usuário já cadastrados!"
            elif db.email_existe(email):
                msg = "E-mail já cadastrado"
            elif db.usuario_existe(usuario):
                msg = "Usuário já cadastrado"

    return render_template('cadastro.html', mensagem=msg)


@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST':
        usuario = request.form['usuario'].lower().replace(' ', '')
        senha = request.form['senha']

        if usuario and senha:
            if db.login(usuario, senha):
                session['usuario'] = usuario
                return redirect('/usuario')
            else:
                msg = "Usuário ou senha incorretos."

    return render_template('login.html', mensagem=msg)


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('usuario', None)
    return redirect('/login')


@app.route('/usuario')
def usuario():
    if 'usuario' in session:
        usuario = session['usuario']
        favoritos = db.obter_numero_favoritos(usuario)
        avaliacoes = db.obter_numero_avaliacoes(usuario)
        return render_template('usuario.html', usuario=usuario.capitalize(), favoritos=favoritos , avaliacoes=avaliacoes)
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run()
