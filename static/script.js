// static/script.js

function buscarRecomendacoes() {
    // 1. Pegar o filme que o usuário selecionou no menu
    const selectElement = document.getElementById('filme-usuario');
    const filmeEscolhido = selectElement.value;
    
    // 2. Pegar a div onde vamos mostrar os resultados
    const containerResultados = document.getElementById('lista-recomendacoes');

    // Validação simples: se o usuário não escolheu nada, avisa e para a execução
    if (!filmeEscolhido) {
        alert("Por favor, selecione um filme primeiro!");
        return;
    }

    // Mostra uma mensagem de "carregando" enquanto a IA pensa
    containerResultados.innerHTML = "<p class='subtitle'>Consultando o cérebro do CineMatch...</p>";

    // 3. Fazer o pedido (Fetch) para o nosso back-end Flask
    fetch(`/api/recomendar?filme=${filmeEscolhido}`)
        .then(response => response.json()) // Transforma a resposta do Flask em dados que o JS entende
        .then(dados => {
            // Limpa o texto de "carregando"
            containerResultados.innerHTML = "";

            // Se o servidor retornou algum erro (como filme não encontrado)
            if (dados.erro) {
                containerResultados.innerHTML = `<p style="color: var(--primary-color);">${dados.erro}</p>`;
                return;
            }

            // 4. Se deu tudo certo, cria um card para cada filme recomendado
            dados.forEach(filme => {
                // Cria a estrutura do card em HTML
                const card = document.createElement('div');
                card.classList.add('filme-card');
                
                card.innerHTML = `
                    <h3>🎬 ${filme.titulo}</h3>
                    <p>Gênero: ${filme.genero}</p>
                `;
                
                // Coloca o card dentro da nossa lista na tela
                containerResultados.appendChild(card);
            });
        })
        .catch(erro => {
            console.error("Erro na requisição:", erro);
            containerResultados.innerHTML = "<p>Ops! Ocorreu um erro ao conectar com o servidor.</p>";
        });
}