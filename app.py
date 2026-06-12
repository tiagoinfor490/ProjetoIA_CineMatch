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
        "poster": "https://br.web.img3.acsta.net/pictures/21/09/29/20/10/5897145.jpg"

    },

    {
        "id": 11,
        "titulo": "Tenet",
        "genero": "Ficção Científica",
        "diretor": "Christopher Nolan",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjI0NDQzYmEtNzMwZC00ODA3LTgzZDYtZTk5ODZjY2Y2OTkzXkEyXkFqcGc@._V1_.jpg"
        
    },
    {
    "id": 12, 
    "titulo": "Gladiador", 
    "genero": "Ação",
    "diretor": "Ridley Scott", 
    "poster": "https://cinema-em-cena.nyc3.cdn.digitaloceanspaces.com/reviews/1233/4DUClyGA6OqjXv6yC0Imf6THGfp.jpg"
    
    },

    {
    "id": 13,
    "titulo":"Mad Max: Estrada da Fúria", 
    "genero": "Ação",
    "diretor": "George Miller", 
    "poster": "https://play-lh.googleusercontent.com/4jEtcyD2lETV4XbD7Tz-epv7z4f9MK07hPNG1ZvwShJP1eIHg5rdDrDDNM8YMDQdR_hW6YbAPNDb0kydkg"
    
    },

    {"id": 14, "titulo": "Batman: O Cavaleiro das Trevas", "genero": "Ação", "diretor": "Christopher Nolan", "poster": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=400"},

    # Drama
    {"id": 15, "titulo": "O Poderoso Chefão", "genero": "Drama", "diretor": "Francis Ford Coppola", "poster": "https://play-lh.googleusercontent.com/ooMpCgZK3ftSd8b5z8pob30iilVw2sUf6V9DQoWPRd4UlvWhT-PJIJMgJEojH3WjTXt4srbfzUuEYu72J-Q"},
    {"id": 16, "titulo": "Clube da Luta", "genero": "Drama", "diretor": "David Fincher", "poster": "https://br.web.img3.acsta.net/medias/nmedia/18/90/95/96/20122166.jpg"},
    {"id": 17, "titulo": "Forrest Gump", "genero": "Drama", "diretor": "Robert Zemeckis", "poster": "https://upload.wikimedia.org/wikipedia/pt/c/c0/ForrestGumpPoster.jpg"},
    {"id": 18, "titulo": "Whiplash", "genero": "Drama", "diretor": "Damien Chazelle", "poster": "https://m.media-amazon.com/images/I/914trm0WbIL._AC_UF894,1000_QL80_.jpg"},
    {"id": 19, "titulo": "O Show de Truman", "genero": "Drama", "diretor": "Peter Weir", "poster": "https://br.web.img3.acsta.net/medias/nmedia/18/93/64/37/20269376.jpg"},

    # Comédia & Animação
    {"id": 20, "titulo": "Superbad", "genero": "Comédia", "diretor": "Greg Mottola", "poster": "https://upload.wikimedia.org/wikipedia/pt/thumb/8/8b/Superbad_Poster.png/250px-Superbad_Poster.png"},
    {"id": 21, "titulo": "Deadpool", "genero": "Comédia", "diretor": "Tim Miller", "poster": "https://m.media-amazon.com/images/M/MV5BNzY3ZWU5NGQtOTViNC00ZWVmLTliNjAtNzViNzlkZWQ4YzQ4XkEyXkFqcGc@._V1_.jpg"},
    {"id": 22, "titulo": "Toy Story", "genero": "Animação", "diretor": "John Lasseter", "poster": "https://upload.wikimedia.org/wikipedia/pt/a/a7/Toy_Story_1995.jpg"},
    {"id": 23, "titulo": "A Viagem de Chihiro", "genero": "Animação", "diretor": "Hayao Miyazaki", "poster": "https://br.web.img3.acsta.net/pictures/210/527/21052756_20131024195513383.jpg"},
    {"id": 24, "titulo": "Shrek", "genero": "Animação", "diretor": "Andrew Adamson", "poster": "https://m.media-amazon.com/images/I/919ZUTtPbXL._AC_UF894,1000_QL80_.jpg"},

    # Suspense & Terror
    {"id": 25, "titulo": "Ilha do Medo", "genero": "Suspense", "diretor": "Martin Scorsese", "poster": "https://www.papodecinema.com.br/wp-content/uploads/2012/04/20180529-download.webp"},
    {"id": 26, "titulo": "Garota Exemplar", "genero": "Suspense", "diretor": "David Fincher", "poster": "https://cinema-em-cena.nyc3.cdn.digitaloceanspaces.com/reviews/63/54nI3vSKlPp42WhJmKVRdmMbkzl.jpg"},
    {"id": 27, "titulo": "Corra!", "genero": "Terror", "diretor": "Jordan Peele", "poster": "https://m.media-amazon.com/images/I/61RsJbAFxbS._AC_UF894,1000_QL80_.jpg"},
    {"id": 28, "titulo": "Hereditário", "genero": "Terror", "diretor": "Ari Aster", "poster": "https://br.web.img3.acsta.net/pictures/18/06/14/13/11/1751062.jpg"},
]



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