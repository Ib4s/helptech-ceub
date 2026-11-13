// Aguarda todo o HTML carregar antes de rodar o código
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. CRIAÇÃO DO BOTÃO FLUTUANTE
    const btn = document.createElement('button');
    btn.style.position = 'fixed';
    btn.style.top = '20px';
    btn.style.right = '20px';
    btn.style.zIndex = '1000';
    btn.style.borderRadius = '20px';
    document.body.appendChild(btn);

    // 2. VERIFICAÇÃO DO TEMA SALVO (Para não perder a escolha ao trocar de página)
    const temaAtual = localStorage.getItem('tema');
    if (temaAtual === 'escuro') {
        document.body.classList.add('dark-mode');
        btn.innerText = '☀️ Modo Claro';
    } else {
        btn.innerText = '🌙 Modo Escuro';
    }

    // 3. AÇÃO DE CLIQUE DO BOTÃO
    btn.addEventListener('click', () => {
        // O "toggle" liga e desliga a classe 'dark-mode'
        document.body.classList.toggle('dark-mode');
        
        // Atualiza o texto do botão e salva no navegador (LocalStorage)
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('tema', 'escuro');
            btn.innerText = '☀️ Modo Claro';
        } else {
            localStorage.setItem('tema', 'claro');
            btn.innerText = '🌙 Modo Escuro';
        }
    });
});