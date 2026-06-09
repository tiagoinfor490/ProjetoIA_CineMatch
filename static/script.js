// static/script.js

let historicoAssistidos = JSON.parse(localStorage.getItem('cineMatchHistorico')) || [];
let filmesOriginal = []; // Vai guardar a lista completa vinda do servidor com letras normais

function buscarRecomendacoes() {
    const inputElement = document.getElementById('filme-usuario');
    const filmeEscolhido = inputElement.value.trim(); 
    const containerResultados = document.getElementById('lista-recomendacoes');
    fecharSugestoes(); // Fecha a caixinha ao buscar

    if (!filmeEscolhido) {
        containerResultados.innerHTML = "<p class='subtitle' style='color: #ffcc00;'>⚠️ Por favor, digite ou selecione o nome de um filme antes de buscar!</p>";
        return;
    }

    containerResultados.innerHTML = "<p class='subtitle'>🔍 Consultando o cérebro do CineMatch...</p>";

    fetch(`/api/recomendar?filme=${filmeEscolhido}`)
        .then(response => response.json())
        .then(dados => {
            containerResultados.innerHTML = "";

            if (dados.erro) {
                containerResultados.innerHTML = `
                    <p class='subtitle' style='color: #ff4444;'>❌ Ops! "${filmeEscolhido}" não foi encontrado no nosso catálogo.</p>
                    <p style='color: var(--text-gray); font-size: 0.9rem;'>Dica: Verifique a ortografia ou use a nossa lista de sugestões!</p>
                `;
                return;
            }

            const sugestoesFiltradas = dados.filter(filme => 
                filme.titulo.toLowerCase() !== filmeEscolhido.toLowerCase() && 
                !historicoAssistidos.includes(filme.titulo)
            );

            if (sugestoesFiltradas.length === 0) {
                containerResultados.innerHTML = "<p class='subtitle'>🎉 Você já assistiu a todas as recomendações disponíveis para este gênero!</p>";
                return;
            }

            const mensagemSucesso = document.createElement('p');
            mensagemSucesso.className = 'subtitle';
            mensagemSucesso.style.color = '#00cc66';
            mensagemSucesso.innerHTML = `🍿 Encontramos estes filmes semelhantes a <strong>${filmeEscolhido}</strong>:`;
            containerResultados.appendChild(mensagemSucesso);

            sugestoesFiltradas.forEach(filme => {
                const card = document.createElement('div');
                card.classList.add('filme-card');
                
                card.innerHTML = `
                    <img src="${filme.poster}" alt="Pôster" class="filme-poster">
                    <div class="filme-card-info">
                        <h3>🎬 ${filme.titulo}</h3>
                        <p><strong>Gênero:</strong> ${filme.genero}</p>
                        <p><strong>Diretor:</strong> ${filme.diretor}</p>
                        <p style="color: var(--primary-color); font-weight: bold; margin-top: 5px; font-size: 0.85rem;">
                            🔥 Afinidade: ${filme.pontos} ponto(s)
                        </p>
                        <button onclick="adicionarAoHistorico('${filme.titulo}'); buscarRecomendacoesAoClicarNoCard('${filmeEscolhido}');" style="margin-top: 10px; background-color: #333; font-size: 0.75rem; padding: 4px 8px; align-self: flex-start;">
                            Já Assisti ✔
                        </button>
                    </div>
                `;
                containerResultados.appendChild(card);
            });
            
            inputElement.value = "";
        })
        .catch(erro => {
            console.error("Erro:", erro);
            containerResultados.innerHTML = "<p>Ops! Erro ao conectar com o servidor.</p>";
        });
}

function buscarRecomendacoesAoClicarNoCard(filmeOriginal) {
    document.getElementById('filme-usuario').value = filmeOriginal;
    buscarRecomendacoes();
}

function adicionarAoHistorico(tituloFilme) {
    if (!historicoAssistidos.includes(tituloFilme)) {
        historicoAssistidos.push(tituloFilme);
        localStorage.setItem('cineMatchHistorico', JSON.stringify(historicoAssistidos));
        atualizarVisualHistorico();
    }
}

function atualizarVisualHistorico() {
    const divHistorico = document.getElementById('lista-historico');
    if (historicoAssistidos.length === 0) {
        divHistorico.innerHTML = "<em>Nenhum filme assistido ainda.</em>";
        return;
    }
    divHistorico.innerHTML = historicoAssistidos
        .map(filme => `<span style="background: #333; padding: 5px 10px; border-radius: 15px; border: 1px solid var(--primary-color);">${filme}</span>`)
        .join(' ');
}

function limparHistorico() {
    historicoAssistidos = [];
    localStorage.removeItem('cineMatchHistorico');
    atualizarVisualHistorico();
    document.getElementById('lista-recomendacoes').innerHTML = "";
}

function carregarMenuFilmes() {
    fetch('/api/filmes')
        .then(response => response.json())
        .then(filmes => {
            // Guardamos os dados puros dos filmes vindos do Python
            filmesOriginal = Array.isArray(filmes) ? Grid = filmes : [];
            atualizarVisualHistorico();
        });
}

// NOVA FUNÇÃO: Atualiza a caixa de sugestões personalizada conforme a digitação
function atualizarCaixaSugestoes(texto) {
    const caixa = document.getElementById('caixa-sugestoes');
    const termo = texto.trim().toLowerCase();

    if (!termo) {
        fecharSugestoes();
        return;
    }

    // Filtra os filmes do catálogo que contém as letras digitadas
    const filtrados = filmesOriginal.filter(filme => 
        filme.titulo.toLowerCase().includes(termo)
    );

    if (filtrados.length === 0) {
        fecharSugestoes();
        return;
    }

    // Limpa e constrói as linhas de sugestões
    caixa.innerHTML = '';
    filtrados.forEach(filme => {
        const item = document.createElement('div');
        item.className = 'sugestao-item';
        item.textContent = filme.titulo;
        
        // Quando o usuário clica/toca na sugestão customizada
        item.onclick = function() {
            document.getElementById('filme-usuario').value = filme.titulo;
            fecharSugestoes();
            buscarRecomendacoes(); // Dispara a busca imediatamente após a escolha
        };
        
        caixa.appendChild(item);
    });

    caixa.style.display = 'block'; // Mostra a caixinha na tela
}

function fecharSugestoes() {
    document.getElementById('caixa-sugestoes').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    carregarMenuFilmes();

    const inputInput = document.getElementById('filme-usuario');

    // Escuta a digitação para atualizar a nossa lista customizada
    inputInput.addEventListener('input', (e) => {
        atualizarCaixaSugestoes(e.target.value);
    });

    // Permite buscar ao apertar Enter
    inputInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            buscarRecomendacoes();
        }
    });

    // Fecha a lista se o usuário clicar em qualquer outro lugar fora da caixinha
    document.addEventListener('click', (e) => {
        if (e.target !== inputInput) {
            // Um pequeno delay para dar tempo do clique no item funcionar antes de sumir
            setTimeout(fecharSugestoes, 200);
        }
    });
});