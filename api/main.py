from fastapi import FastAPI, HTTPException
from database import obter_todos_livros, buscar_livro_por_titulo, obter_estatisticas_banco

app = FastAPI(title="API de Coleta de Dados de Livros")

@app.get("/")
def home():
    return {"status": "API online", "mensagem": "Acesse /docs para a documentacao interativa"}

@app.get("/items")
def listar_livros(limit: int = 100):
    return obter_todos_livros(limit)

@app.get("/items/buscar")
def buscar_livro(titulo: str):
    livro = buscar_livro_por_titulo(titulo)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    return livro

@app.get("/stats")
def estatisticas():
    return obter_estatisticas_banco()