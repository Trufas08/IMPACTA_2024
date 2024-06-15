from flask import Flask, render_template, request, redirect, session, jsonify
from models.database import Database

app = Flask(__name__)
app.secret_key = 'SENHA-MUITO-SECRETA'

db = Database()


@app.route('/')
def index():
    usuario = get_usuario()
    return render_template('index.html', usuario=usuario)


@app.route('/pesquisa', methods=['GET'])
def pesquisa():
    query = request.args.get('query')
    if query:
        livros = db.pesquisar_livros(query)
        livros_formatados = [{'id': livro[0], 'titulo': livro[1]} for livro in livros]
        return jsonify({'livros': livros_formatados})
    else:
        return jsonify({'livros': []})


@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    msg = ''
    usuario = get_usuario()
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

    return render_template('cadastro.html', mensagem=msg, usuario=usuario)


@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ''
    usuario = get_usuario()
    if request.method == 'POST':
        usuario = request.form['usuario'].lower().replace(' ', '')
        senha = request.form['senha']

        if usuario and senha:
            if db.login(usuario, senha):
                session['usuario'] = usuario
                return redirect('/usuario')
            else:
                msg = "Usuário ou senha incorretos."

    return render_template('login.html', mensagem=msg, usuario=usuario)


def get_usuario():
    return session.get('usuario', None)


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('usuario', None)
    return redirect('/login')


@app.route('/usuario')
def usuario():
    if 'usuario' in session:
        usuario = session['usuario']
        favoritos = db.obter_favoritos(usuario)
        avaliacoes = db.obter_numero_avaliacoes(usuario)
        return render_template('usuario.html', usuario=usuario.capitalize(), favoritos=favoritos, avaliacoes=avaliacoes)
    else:
        return redirect('/login')


@app.route('/adicionar_favorito/<int:livro_id>', methods=['POST'])
def adicionar_favorito(livro_id):
    if 'usuario' in session:
        usuario = session['usuario']
        db.adicionar_favorito(usuario, livro_id)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Usuário não está logado.'})


@app.route('/remover_favorito/<int:livro_id>', methods=['POST'])
def remover_favorito(livro_id):
    if 'usuario' in session:
        usuario = session['usuario']
        db.remover_favorito(usuario, livro_id)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Usuário não está logado.'})


@app.route('/detalhes_livro/<int:livro_id>')
def detalhes_livro(livro_id):
    usuario = get_usuario()
    detalhes = db.obter_detalhes_livro(livro_id, usuario)
    return render_template('detalhes_livro.html', livro=detalhes, usuario=usuario)


if __name__ == '__main__':
    app.run(debug=True)
