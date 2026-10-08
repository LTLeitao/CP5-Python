from datetime import datetime
import requests
from bs4 import BeautifulSoup
from database import salvar_livro

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def extrair_livros(qtd_paginas=5):
    total_novos = 0
    total_duplicados = 0

    print(f"Iniciando coleta em {qtd_paginas} paginas...")

    for pagina in range(1, qtd_paginas + 1):
        url = f"http://books.toscrape.com/catalogue/page-{pagina}.html"
        print(f"\nAcessando Pagina {pagina}: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erro ao acessar a pagina {pagina}. Status: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        livros_html = soup.select(".product_pod")

        for item in livros_html:
            titulo = item.h3.a["title"]
            preco_raw = item.select_one(".price_color").text
            avaliacao_classe = item.select_one(".star-rating")["class"][1]
            estoque_raw = item.select_one(".instock.availability").text.strip()

            preco = float(preco_raw.replace("£", "").replace("Â", "").strip())
            avaliacao = RATING_MAP.get(avaliacao_classe, 0)
            em_estoque = "In stock" in estoque_raw

            documento = {
                "titulo": titulo,
                "preco": preco,
                "avaliacao": avaliacao,
                "em_estoque": em_estoque,
                "url_origem": url,
                "data_coleta": datetime.utcnow()
            }

            if salvar_livro(documento):
                total_novos += 1
                print(f"  [+] Salvo: {titulo}")
            else:
                total_duplicados += 1
                print(f"  [-] Ja existe: {titulo}")

    print("\n--- Resumo Final da Coleta ---")
    print(f"Total de novos registros inseridos: {total_novos}")
    print(f"Total de registros duplicados ignorados: {total_duplicados}")

if __name__ == "__main__":
    extrair_livros(qtd_paginas=5)