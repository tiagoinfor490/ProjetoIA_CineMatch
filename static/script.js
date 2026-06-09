// static/script.js

// Carrega o histórico da memória do navegador
let historicoAssistidos = JSON.parse(localStorage.getItem('cineMatchHistorico')) || [];

// NOVA VARIÁVEL: Vai guardar os nomes dos filmes para a busca automática instantânea
let filmesDisponiveis = []; 

function buscarRecomendacoes() {
    const inputElement = document.getElementById('filme-usuario');
    const filmeEscolhido = inputElement.value.trim(); 
    const containerResultados = document.getElementById('lista-recomendacoes');

    if (!filmeEscolhido) {
        return; // Se estiver vazio, não faz nada
    }

    adicionarAoHistorico(filmeEscolhido);
    containerResultados.innerHTML = "<p class='subtitle'>Consultando o cérebro do CineMatch...</p>";

    fetch(`/api/recomendar?filme=${filmeEscolhido}`)
        .then(response => response.json())
        .then(dados => {
            containerResultados.innerHTML = "";

            if (dados.erro) {
                containerResultados.innerHTML = `<p style="color: var(--primary-color);">${dados.erro}</p>`;
                return;
            }

            const sugestoesFiltradas = dados.filter(filme => !historicoAssistidos.includes(filme.titulo));

            if (sugestoesFiltradas.length === 0) {
                containerResultados.innerHTML = "<p class='subtitle'>🎉 Você já assistiu a todas as recomendações disponíveis para este gênero!</p>";
                return;
            }

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
                        <button onclick="adicionarAoHistorico('${filme.titulo}'); buscarRecomendacoes();" style="margin-top: 10px; background-color: #333; font-size: 0.75rem; padding: 4px 8px; align-self: flex-start;">
                            Já Assisti ✔
                        </button>
                    </div>
                `;
                containerResultados.appendChild(card);
            });
            
            // Limpa o campo de texto para a próxima busca
            inputElement.value = "";
        })
        .catch(erro => {
            console.error("Erro:", erro);
            containerResultados.innerHTML = "<p>Ops! Erro ao conectar com o servidor.</p>";
        });
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
            const datalistElement = document.getElementById('lista-sugestoes-busca');
            datalistElement.innerHTML = ''; 
            
            // ATUALIZAÇÃO: Guardamos a lista de filmes em letras minúsculas para checagem rápida
            filmesDisponiveis = filmes.map(f => f.titulo.toLowerCase());

            filmes.forEach(filme => {
                const opcao = document.createElement('option');
                opcao.value = filme.titulo; 
                datalistElement.appendChild(opcao);
            });
            atualizarVisualHistorico();
        });
}

// === NOVIDADE: OUVINTE DE DIGITAÇÃO INSTANTÂNEA ===
document.addEventListener('DOMContentLoaded', () => {
    carregarMenuFilmes();

    // Monitora tudo o que é digitado na caixinha de texto
    document.getElementById('filme-usuario').addEventListener('input', (e) => {
        const textoDigitado = e.target.value.trim().toLowerCase();
        
        // Se o usuário clicou na sugestão ou terminou de digitar o nome exato de um filme da lista:
        if (filmesDisponiveis.includes(textoDigitado)) {
            buscarRecomendacoes(); // Dispara a IA imediatamente!
        }
    });
});