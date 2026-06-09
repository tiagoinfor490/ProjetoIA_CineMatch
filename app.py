# app.py
from flask import Flask, jsonify, request
# app.py (Adicione antes do final do arquivo)

app = Flask(__name__)

filmes_db = [
    {
        "id": 1, 
        "titulo": "Matrix", 
        "genero": "Ficção Científica", 
        "diretor": "Lana Wachowski",
        "poster": "https://m.media-amazon.com/images/I/613ypTLZHsL._AC_UF894,1000_QL80_.jpg"
    },
    {
        "id": 2, 
        "titulo": "Interestelar", 
        "genero": "Ficção Científica", 
        "diretor": "Christopher Nolan",
        "poster": "https://m.media-amazon.com/images/I/91FhSXlwgjL._AC_UF894,1000_QL80_.jpg"
    },
    {
        "id": 3, 
        "titulo": "A Origem", 
        "genero": "Ficção Científica", 
        "diretor": "Christopher Nolan",
        "poster": "https://upload.wikimedia.org/wikipedia/pt/8/84/AOrigemPoster.jpg"
    },
    {
        "id": 4, 
        "titulo": "Blade Runner 2049", 
        "genero": "Ficção Científica", 
        "diretor": "Denis Villeneuve",
        "poster": "https://br.web.img3.acsta.net/pictures/17/08/25/11/58/463146.jpg"
    },
    {
        "id": 5, 
        "titulo": "Vingadores: Ultimato", 
        "genero": "Ação", 
        "diretor": "Anthony Russo e Joe Russo",
        "poster": "https://m.media-amazon.com/images/I/91J7VHbAwBL._AC_UF894,1000_QL80_.jpg"
    },
    {
        "id": 6, 
        "titulo": "John Wick", 
        "genero": "Ação", 
        "diretor": "Chad Stahelski",
        "poster": "https://upload.wikimedia.org/wikipedia/pt/1/13/John_wick_ver3.jpg"
    },
    {
        "id": 7, 
        "titulo": "Se Beber, Não Case!", 
        "genero": "Comédia", 
        "diretor": "Todd Phillips",
        "poster": "https://m.media-amazon.com/images/I/618FiO7H+sS._AC_UF894,1000_QL80_.jpg"
    },
    {
        "id": 8, 
        "titulo": "Gente Grande", 
        "genero": "Comédia", 
        "diretor": "Dennis Dugan",
        "poster": "https://m.media-amazon.com/images/S/pv-target-images/28ba30adb15abcf10253d4c9e07575a206dfd89e48c37714b5f8603ce1575bf9.jpg"
    },
    {
        "id": 9, 
        "titulo": "Invocação do Mal", 
        "genero": "Terror", 
        "diretor": "James Wan",
        "poster": "https://br.web.img2.acsta.net/pictures/210/166/21016629_2013062820083878.jpg"
    }
]

# [Etapa 2] Nossa lógica de recomendação da IA
# app.py (Substitua a função recomendar_filmes)

def recomendar_filmes(titulo_escolhido):
    # 1. Encontra o filme que o usuário escolheu
    filme_usuario = None
    for filme in filmes_db:
        if filme["titulo"].lower() == titulo_escolhido.lower():
            filme_usuario = filme
            break
    
    if not filme_usuario:
        return None
    
    # 2. Guarda as características do filme escolhido
    genero_alvo = filme_usuario["genero"]
    diretor_alvo = filme_usuario.get("diretor", "")
    
    sugestoes = []
    
    # 3. O SISTEMA DE PESOS (SCORING)
   # app.py (Ajuste apenas essa linha dentro da função recomendar_filmes)

    for filme in filmes_db:
        # Adicionado o .strip() para remover espaços invisíveis que o usuário possa ter digitado
        if filme["titulo"].lower() == titulo_escolhido.strip().lower():
            filme_usuario = filme
            break

        pontos = 0
        
        # Regra 1: Mesmo gênero vale 1 ponto
        if filme["genero"] == genero_alvo:
            pontos += 1
            
        # Regra 2: Mesmo diretor vale 2 pontos
        if "diretor" in filme and filme["diretor"] == diretor_alvo:
            pontos += 2
            
        # Se o filme marcou pelo menos 1 ponto, ele entra nas sugestões
        if pontos > 0:
            # Criamos uma cópia do filme para não alterar o banco de dados original
            filme_sugerido = filme.copy()
            filme_sugerido["pontos"] = pontos # Salvamos a pontuação do filme
            sugestoes.append(filme_sugerido)
            
    # 4. Ordenar os filmes: quem tem mais pontos aparece primeiro!
    # (O código lambda abaixo é um truque do Python para ordenar listas baseadas em um valor específico)
    sugestoes.sort(key=lambda x: x["pontos"], reverse=True)
            
    return sugestoes

# === [Etapa 3 Nova!] Criando a nossa API Web ===

@app.route('/api/recomendar', methods=['GET'])
def api_recomendar():
    # Captura o filme que o usuário vai enviar pela URL (ex: ?filme=Matrix)
    filme_escolhido = request.args.get('filme')
    
    if not filme_escolhido:
        return jsonify({"erro": "Por favor, informe o nome de um filme!"}), 400
        
    # Roda a nossa função de IA
    resultados = recomendar_filmes(filme_escolhido)
    
    if resultados is None:
        return jsonify({"erro": "Filme não encontrado na nossa base de dados."}), 404
        
    # Retorna o resultado em formato JSON (padrão universal da web)
    return jsonify(resultados)
    
from flask import render_template # Adicione essa importação no topo!

@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/api/filmes', methods=['GET'])
def api_listar_filmes():
    # Simplesmente devolvemos a nossa base de dados inteira em formato JSON
    return jsonify(filmes_db)

    
if __name__ == '__main__':
    # Roda o servidor local no modo de testes (debug=True)
    app.run(debug=True)