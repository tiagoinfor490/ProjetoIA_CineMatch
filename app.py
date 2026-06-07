# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# [Etapa 1] Nossa base de dados de filmes
filmes_db = [
    {"id": 1, "titulo": "Matrix", "genero": "Ficção Científica"},
    {"id": 2, "titulo": "Interestelar", "genero": "Ficção Científica"},
    {"id": 3, "titulo": "Blade Runner 2049", "genero": "Ficção Científica"},
    {"id": 4, "titulo": "Vingadores: Ultimato", "genero": "Ação"},
    {"id": 5, "titulo": "Mad Max: Estrada da Fúria", "genero": "Ação"},
    {"id": 6, "titulo": "John Wick", "genero": "Ação"},
    {"id": 7, "titulo": "Se Beber, Não Case!", "genero": "Comédia"},
    {"id": 8, "titulo": "Superbad", "genero": "Comédia"},
    {"id": 9, "titulo": "Gente Grande", "genero": "Comédia"},
    {"id": 10, "titulo": "Invocação do Mal", "genero": "Terror"},
    {"id": 11, "titulo": "Hereditário", "genero": "Terror"}
]

# [Etapa 2] Nossa lógica de recomendação da IA
def recomendar_filmes(titulo_escolhido):
    filme_usuario = None
    for filme in filmes_db:
        if filme["titulo"].lower() == titulo_escolhido.lower():
            filme_usuario = filme
            break
    
    if not filme_usuario:
        return None
    
    genero_alvo = filme_usuario["genero"]
    
    sugestoes = []
    for filme in filmes_db:
        if filme["genero"] == genero_alvo and filme["titulo"].lower() != titulo_escolhido.lower():
            sugestoes.append(filme)
            
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
    
if __name__ == '__main__':
    # Roda o servidor local no modo de testes (debug=True)
    app.run(debug=True)