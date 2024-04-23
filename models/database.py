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
        hashed_senha = self.gerar_hash_senha(senha)
        comando = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        dados = (usuario, email, hashed_senha)
        self.cursor.execute(comando, dados)
        self.conexao.commit()


    def verificar_senha(self, senha_digitada, hash_senha):
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_senha.encode('utf-8'))
    

    def gerar_hash_senha(self, senha):
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())


    def login(self, usuario, senha_digitada):
        comando = "SELECT senha FROM usuarios WHERE nome = %s"
        self.cursor.execute(comando, (usuario,))
        resultado = self.cursor.fetchone()
        
        if resultado:
            hash_senha = resultado[0]
            return self.verificar_senha(senha_digitada, hash_senha)
        else:
            return False


    def obter_numero_favoritos(self, usuario):
        comando = "SELECT COUNT(*) FROM Favoritos WHERE usuario_id = (SELECT usuario_id FROM Usuarios WHERE nome = %s)"
        self.cursor.execute(comando, (usuario,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0


    def obter_numero_avaliacoes(self, usuario):
        comando = "SELECT COUNT(*) FROM Avaliacoes WHERE usuario_id = (SELECT usuario_id FROM Usuarios WHERE nome = %s)"
        self.cursor.execute(comando, (usuario,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0
    
    
    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
