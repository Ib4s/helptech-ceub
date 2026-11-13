from flask import Flask, render_template, request, redirect, url_for, session
import modelos
import servicos

app = Flask(__name__)
# Chave secreta necessária para usar sessões (manter o usuário logado)
app.secret_key = 'chave_secreta_projeto_ceub'

# Garante que o banco de dados seja criado ao iniciar
modelos.criar_tabelas()

# ---------------------------------------------------------
# PÁGINAS INICIAIS E AUTENTICAÇÃO
# ---------------------------------------------------------
@app.route('/')
def landing(): 
    return render_template('landing.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Se enviou o formulário, tenta cadastrar
    if request.method == 'POST':
        tipo = request.form['tipo']
        inc = request.form.get('inicio_curso') if tipo == 'tecnico' else None
        prev = request.form.get('previsao_termino') if tipo == 'tecnico' else None
        
        if servicos.registrar_usuario(request.form['nome'], request.form['matricula'], request.form['email'], request.form['senha'], request.form['data_nascimento'], tipo, inc, prev):
            return redirect(url_for('login'))
        return "Erro: Matrícula ou E-mail já registados."
    # Se apenas acessou o link, mostra a página
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = servicos.autenticar_usuario(request.form['matricula'], request.form['senha'])
        # Se achou o usuário no banco, cria a sessão de login
        if usuario:
            session['id_usuario'] = usuario['id']
            session['nome_usuario'] = usuario['nome']
            session['tipo_usuario'] = usuario['tipo']
            return redirect(url_for('dashboard'))
        return "Matrícula ou senha inválidos."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Limpa o login atual
    return redirect(url_for('landing'))

# ---------------------------------------------------------
# DASHBOARD (O Coração do Sistema)
# ---------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    # Proteção: Se não estiver logado, manda pro login
    if 'id_usuario' not in session: return redirect(url_for('login'))
    
    # Se for CLIENTE, mostra a página 'index.html' com os chamados dele
    if session['tipo_usuario'] == 'solicitante':
        chamados = servicos.listar_meus_chamados(session['id_usuario'])
        # Prepara a lista anexando as propostas de cada chamado
        dados = [{'chamado': c, 'propostas': servicos.listar_propostas(c['id'])} for c in chamados]
        return render_template('index.html', nome=session['nome_usuario'], chamados_dados=dados)
    
    # Se for TÉCNICO, mostra a página 'mural.html' com as oportunidades
    else:
        chamados_abertos = servicos.listar_chamados_abertos()
        meus_trabalhos = servicos.listar_trabalhos_tecnico(session['id_usuario'])
        return render_template('mural.html', nome=session['nome_usuario'], chamados=chamados_abertos, meus_trabalhos=meus_trabalhos)

# ---------------------------------------------------------
# ROTAS DE AÇÃO (Botões que não têm tela própria)
# ---------------------------------------------------------
@app.route('/abrir', methods=['POST'])
def abrir():
    servicos.abrir_chamado(request.form['titulo'], request.form['descricao'], session['id_usuario'])
    return redirect(url_for('dashboard'))

@app.route('/candidatar/<int:id_chamado>', methods=['POST'])
def candidatar(id_chamado):
    servicos.candidatar_tecnico(id_chamado, session['id_usuario'])
    return redirect(url_for('dashboard'))

@app.route('/escolher/<int:id_chamado>/<int:id_tecnico>', methods=['POST'])
def escolher(id_chamado, id_tecnico):
    servicos.escolher_tecnico(id_chamado, id_tecnico)
    return redirect(url_for('dashboard'))

@app.route('/finalizar/<int:id_chamado>', methods=['POST'])
def finalizar(id_chamado):
    servicos.finalizar_chamado(id_chamado)
    return redirect(url_for('dashboard'))

# ---------------------------------------------------------
# ROTAS DE VISUALIZAÇÃO (Perfil e Chat)
# ---------------------------------------------------------
@app.route('/perfil/<int:id_usuario>')
def perfil(id_usuario):
    u = servicos.buscar_usuario(id_usuario)
    estatisticas = servicos.obter_estatisticas(id_usuario) if u['tipo'] == 'tecnico' else None
    return render_template('perfil.html', u=u, estatisticas=estatisticas)

@app.route('/chat/<int:id_chamado>', methods=['GET', 'POST'])
def chat(id_chamado):
    if 'id_usuario' not in session: return redirect(url_for('login'))
    
    # Se digitou algo, envia para o banco
    if request.method == 'POST':
        servicos.enviar_mensagem(id_chamado, session['id_usuario'], request.form['mensagem'])
        return redirect(url_for('chat', id_chamado=id_chamado))
    
    # Busca o histórico do chat
    mensagens = servicos.listar_mensagens(id_chamado)
    return render_template('chat.html', id_chamado=id_chamado, mensagens=mensagens, id_logado=session['id_usuario'])

if __name__ == '__main__':
    app.run(debug=True)