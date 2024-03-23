from flask import Flask, render_template, request
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
        usuario = request.form['usuario']
        senha = request.form['senha']
        email = request.form['email']

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


if __name__ == '__main__':
    app.run()

