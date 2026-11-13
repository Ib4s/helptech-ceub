HelpTech CEUB

O HelpTech CEUB é uma plataforma web criada para conectar alunos e professores que precisam de suporte técnico em seus computadores com alunos dos cursos de TI que querem ganhar experiência prática. 

A ideia é funcionar como um mural de classificados exclusivo para a nossa comunidade acadêmica, tornando a manutenção de equipamentos mais acessível, segura e rápida.

## Funcionalidades Principais
* **Dois tipos de perfil:** Cadastro separado para quem precisa de ajuda (Solicitante) e para quem vai consertar (Técnico).
* **Mural de Chamados:** Os solicitantes abrem pedidos de suporte e os técnicos visualizam essas demandas em um painel.
* **Sistema de Candidatura:** O técnico se oferece para resolver o problema e o cliente escolhe quem fará o serviço.
* **Chat Interno:** Após o aceite, os dois conversam de forma privada pelo próprio sistema para combinar preço, horário e local, sem precisar usar o WhatsApp.
* **Segurança:** As senhas dos usuários não ficam salvas em texto, elas são protegidas com criptografia no banco de dados.

## Tecnologias Utilizadas
* **Back-end:** Python com o framework Flask
* **Banco de Dados:** SQLite
* **Front-end:** HTML, CSS e JavaScript (com suporte para Tema Claro/Escuro)
* **Segurança:** Werkzeug Security (Hashing de senhas)

## Como rodar o projeto localmente
1. Baixe os arquivos do repositório.
2. Abra o terminal na pasta do projeto e instale o Flask com o comando: `pip install flask`
3. Inicie o servidor rodando o comando: `python app.py`
4. Abra o seu navegador e acesse: `http://127.0.0.1:5000`
