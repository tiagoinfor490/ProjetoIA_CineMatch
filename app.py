# app.py
from flask import Flask, jsonify, request
# app.py (Adicione antes do final do arquivo)

app = Flask(__name__)
main = app

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

    },
    
    {
        "id": 10,
        "titulo": "Duna",
        "genero": "Ficção Científica", 
        "diretor": "Denis Villeneuve", 
        "poster": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=400"

    },

    {
        "id": 11,
        "titulo": "Tenet",
        "genero": "Ficção Científica",
        "diretor": "Christopher Nolan",
        "poster": "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=400"
        
    },
    {
    "id": 12, 
    "titulo": "Gladiador", 
    "genero": "Ação",
    "diretor": "Ridley Scott", 
    "poster": "https://images.unsplash.com/photo-1559181567-c3190ca9959b?q=80&w=400"
    
    },

    {"id": 13, "titulo": "Mad Max: Estrada da Fúria", "genero": "Ação", "diretor": "George Miller", "poster": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?q=80&w=400"},

    {"id": 14, "titulo": "Batman: O Cavaleiro das Trevas", "genero": "Ação", "diretor": "Christopher Nolan", "poster": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=400"},
]

# [Etapa 2] Nossa lógica de recomendação da IA
# app.py (Substitua a função recomendar_filmes)

# app.py (Substitua a função recomendar_filmes para garantir compatibilidade total)

def recomendar_filmes(titulo_escolhido):
    filme_usuario = None
    # Remove espaços e joga para minúsculo
    titulo_busca = titulo_escolhido.strip().lower()
    
    for filme in filmes_db:
        if filme["titulo"].lower() == titulo_busca:
            filme_usuario = filme
            break
    
    if not filme_usuario:
        return None
    
    genero_alvo = filme_usuario["genero"]
    diretor_alvo = filme_usuario.get("diretor", "")
    
    sugestoes = []
    
    for filme in filmes_db:
        # Garante que não vai recomendar o próprio filme pesquisado
        if filme["titulo"].lower() == titulo_busca:
            continue
            
        pontos = 0
        
        # Comparação direta de gênero
        if filme["genero"] == genero_alvo:
            pontos += 1
            
        # Comparação direta de diretor
        if "diretor" in filme and filme["diretor"] == diretor_alvo:
            pontos += 2
            
        if pontos > 0:
            filme_sugerido = filme.copy()
            filme_sugerido["pontos"] = pontos
            sugestoes.append(filme_sugerido)
            
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