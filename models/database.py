import mysql.connector
import bcrypt

class Database:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='SENHA-MUITO-SECRETA',
            database='livraria'
        )
        self.cursor = self.conexao.cursor()


    def email_existe(self, email):
        comando = "SELECT COUNT(*) FROM usuarios WHERE email = %s"
        self.cursor.execute(comando, (email,))
        resultado = self.cursor.fetchone()
        return resultado[0] > 0


    def usuario_existe(self, usuario):
        comando = "SELECT COUNT(*) FROM usuarios WHERE nome = %s"
        self.cursor.execute(comando, (usuario,))
        resultado = self.cursor.fetchone()
        return resultado[0] > 0


    def cadastrar_usuario(self, usuario, email, senha):
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        comando = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        dados = (usuario, email, hashed_senha)
        self.cursor.execute(comando, dados)
        self.conexao.commit()


    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
