from modelos import conectar
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------------------------------------
# FUNÇÕES DE USUÁRIO (Cadastro e Login)
# ---------------------------------------------------------
def registrar_usuario(nome, matricula, email, senha, data_nascimento, tipo, inicio_curso=None, previsao_termino=None):
    conn = conectar()
    # SEGURANÇA: Transforma a senha em um código embaralhado irreversível (hash)
    senha_criptografada = generate_password_hash(senha)
    
    try:
        conn.execute('INSERT INTO usuarios (nome, matricula, email, senha, data_nascimento, tipo, inicio_curso, previsao_termino) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                     (nome, matricula, email, senha_criptografada, data_nascimento, tipo, inicio_curso, previsao_termino))
        conn.commit()
        return True # Retorna True se o cadastro der certo
    except: 
        return False # Retorna False se a matrícula já existir
    finally: 
        conn.close()

def autenticar_usuario(matricula, senha):
    conn = conectar()
    # Busca apenas pela matrícula primeiro
    usuario = conn.execute('SELECT * FROM usuarios WHERE matricula = ?', (matricula,)).fetchone()
    conn.close()
    
    # SEGURANÇA: Verifica se o usuário existe e se a senha digitada bate com o hash do banco
    if usuario and check_password_hash(usuario['senha'], senha):
        return usuario
    return None

def buscar_usuario(id_usuario):
    conn = conectar()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id_usuario,)).fetchone()
    conn.close()
    return usuario

# ---------------------------------------------------------
# FUNÇÕES DE CHAMADOS
# ---------------------------------------------------------
def abrir_chamado(titulo, descricao, id_solicitante):
    conn = conectar()
    conn.execute('INSERT INTO chamados (titulo, descricao, id_solicitante) VALUES (?, ?, ?)', (titulo, descricao, id_solicitante))
    conn.commit()
    conn.close()

def listar_chamados_abertos():
    conn = conectar()
    chamados = conn.execute("SELECT * FROM chamados WHERE status = 'Aberto'").fetchall()
    conn.close()
    return chamados

def listar_meus_chamados(id_solicitante):
    conn = conectar()
    chamados = conn.execute("SELECT * FROM chamados WHERE id_solicitante = ?", (id_solicitante,)).fetchall()
    conn.close()
    return chamados

def listar_trabalhos_tecnico(id_tecnico):
    conn = conectar()
    chamados = conn.execute("SELECT * FROM chamados WHERE id_tecnico = ? AND status != 'Aberto'", (id_tecnico,)).fetchall()
    conn.close()
    return chamados

def finalizar_chamado(id_chamado):
    conn = conectar()
    conn.execute("UPDATE chamados SET status = 'Concluído' WHERE id = ?", (id_chamado,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# FUNÇÕES DE PROPOSTAS
# ---------------------------------------------------------
def candidatar_tecnico(id_chamado, id_tecnico):
    conn = conectar()
    try:
        conn.execute('INSERT INTO propostas (id_chamado, id_tecnico) VALUES (?, ?)', (id_chamado, id_tecnico))
        conn.commit()
    except: pass # Se ele já se candidatou, o sistema ignora para não dar erro
    finally: conn.close()

def listar_propostas(id_chamado):
    conn = conectar()
    propostas = conn.execute('SELECT p.id_tecnico, u.nome FROM propostas p JOIN usuarios u ON p.id_tecnico = u.id WHERE p.id_chamado = ?', (id_chamado,)).fetchall()
    conn.close()
    return propostas

def escolher_tecnico(id_chamado, id_tecnico):
    conn = conectar()
    # Muda o status do chamado e vincula o técnico escolhido
    conn.execute("UPDATE chamados SET status = 'Em Andamento', id_tecnico = ? WHERE id = ?", (id_tecnico, id_chamado))
    # Limpa as propostas pois o chamado já tem dono
    conn.execute("DELETE FROM propostas WHERE id_chamado = ?", (id_chamado,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# FUNÇÕES DE CHAT E MÉTRICAS
# ---------------------------------------------------------
def enviar_mensagem(id_chamado, id_remetente, texto):
    conn = conectar()
    conn.execute('INSERT INTO mensagens (id_chamado, id_remetente, texto) VALUES (?, ?, ?)', (id_chamado, id_remetente, texto))
    conn.commit()
    conn.close()

def listar_mensagens(id_chamado):
    conn = conectar()
    mensagens = conn.execute('''
        SELECT m.texto, m.data_envio, u.nome, u.id as id_remetente 
        FROM mensagens m JOIN usuarios u ON m.id_remetente = u.id 
        WHERE m.id_chamado = ? ORDER BY m.data_envio ASC
    ''', (id_chamado,)).fetchall()
    conn.close()
    return mensagens

def obter_estatisticas(id_tecnico):
    conn = conectar()
    concluidos = conn.execute("SELECT COUNT(*) FROM chamados WHERE id_tecnico = ? AND status = 'Concluído'", (id_tecnico,)).fetchone()[0]
    em_andamento = conn.execute("SELECT COUNT(*) FROM chamados WHERE id_tecnico = ? AND status = 'Em Andamento'", (id_tecnico,)).fetchone()[0]
    conn.close()
    return concluidos, em_andamento