from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["db_livros_projeto"]
collection = db["livros"]

def obter_todos_livros(limit=100):
    livros = list(collection.find({}, {"_id": 0}).limit(limit))
    return livros

def buscar_livro_por_titulo(titulo: str):
    return collection.find_one({"titulo": {"$regex": titulo, "$options": "i"}}, {"_id": 0})

def obter_estatisticas_banco():
    total = collection.count_documents({})
    pipeline = [
        {"$group": {
            "_id": None,
            "preco_medio": {"$avg": "$preco"},
            "preco_maximo": {"$max": "$preco"},
            "preco_minimo": {"$min": "$preco"}
        }}
    ]
    stats = list(collection.aggregate(pipeline))
    
    if stats:
        return {
            "total_registros": total,
            "preco_medio": round(stats[0]["preco_medio"], 2),
            "preco_maximo": stats[0]["preco_maximo"],
            "preco_minimo": stats[0]["preco_minimo"]
        }
    return {"total_registros": 0, "preco_medio": 0, "preco_maximo": 0, "preco_minimo": 0}