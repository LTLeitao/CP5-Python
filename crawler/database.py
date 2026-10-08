from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["db_livros_projeto"]
collection = db["livros"]

def salvar_livro(livro_data):
    existente = collection.find_one({"titulo": livro_data["titulo"]})
    if not existente:
        collection.insert_one(livro_data)
        return True
    return False