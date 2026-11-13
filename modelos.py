import sqlite3
from werkzeug.security import generate_password_hash

# ---------------------------------------------------------
# CONEXÃO COM O BANCO
# ---------------------------------------------------------
def conectar():
    conn = sqlite3.connect('helptech.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
# CRIAÇÃO DAS TABELAS
# ---------------------------------------------------------
def criar_tabelas():
    conn = conectar()
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            tipo TEXT NOT NULL,
            inicio_curso TEXT,
            previsao_termino TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT DEFAULT 'Aberto',
            id_solicitante INTEGER,
            id_tecnico INTEGER,
            FOREIGN KEY(id_solicitante) REFERENCES usuarios(id),
            FOREIGN KEY(id_tecnico) REFERENCES usuarios(id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS propostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_chamado INTEGER,
            id_tecnico INTEGER,
            UNIQUE(id_chamado, id_tecnico)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_chamado INTEGER,
            id_remetente INTEGER,
            texto TEXT NOT NULL,
            data_envio DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ---------------------------------------------------------
    # DADOS DE TESTE (Agora com senhas criptografadas!)
    # ---------------------------------------------------------
    usuarios_teste = [
        ('Eduardo - Técnico', '1', 'eduardo@teste.com', generate_password_hash('1'), '2000-01-01', 'tecnico', '2023-01-01', '2027-12-31'),
        ('Lucas - Técnico', '2', 'lucas@teste.com', generate_password_hash('2'), '2000-01-01', 'tecnico', '2023-01-01', '2027-12-31'),
        ('Pedro - Cliente', '3', 'pedro@teste.com', generate_password_hash('3'), '2000-01-01', 'solicitante', None, None),
        ('Mauricio - Cliente', '4', 'mauricio@teste.com', generate_password_hash('4'), '2000-01-01', 'solicitante', None, None)
    ]
    
    conn.executemany('''
        INSERT OR IGNORE INTO usuarios 
        (nome, matricula, email, senha, data_nascimento, tipo, inicio_curso, previsao_termino) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', usuarios_teste)
    
    conn.commit()
    conn.close()