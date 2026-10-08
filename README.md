# Pipeline de Dados e Dashboard - Books to Scrape

Este projeto consiste em uma pipeline completa de engenharia de dados e visualização de métricas, composta por um Web Crawler para coleta automatizada de dados, persistência em banco de dados NoSQL (MongoDB), uma API RESTful desenvolvida em FastAPI e um Dashboard interativo construído em Streamlit.

---

## 📁 Estrutura do Projeto

```text
projeto_livros/
├── api/
│   ├── database.py       # Conexão e consultas ao MongoDB para a API
│   └── main.py           # Endpoints da FastAPI (/items, /stats, etc.)
├── crawler/
│   ├── database.py       # Persistência e verificação de duplicatas no MongoDB
│   └── scraper.py        # Web Crawler multipágina (BeautifulSoup)
├── dashboard/
│   ├── app.py            # Interface gráfica e gráficos no Streamlit
│   └── style.css         # Estilização externa customizada (Bootstrap 5)
├── .gitignore
├── README.md
└── requirements.txt

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.10+

Web Scraping: BeautifulSoup4, Requests

Banco de Dados: MongoDB (PyMongo)

Backend / API: FastAPI, Uvicorn

Frontend / Dashboard: Streamlit, Pandas

Estilização: CSS3 Customizado, Bootstrap 5 & Bootstrap Icons

⚙️ Pré-requisitos
Antes de iniciar, certifique-se de ter instalado em sua máquina:

Python 3.10+

MongoDB rodando na porta padrão (localhost:27017)

Git

🚀 Instalação e Configuração
1. Clonar o Repositório
Bash
git clone https://github.com/LTLeitao/CP5-Python.git
cd SCP5-Python

2. Criar e Ativar o Ambiente Virtual
Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\Activate
Linux / macOS:

Bash
python3 -m venv venv
source venv/bin/activate

3. Instalar as Dependências
Bash
pip install -r requirements.txt

🏃‍♂️ Execução do Projeto
Siga a ordem de execução abaixo para rodar a pipeline completa:

Passo 1: Executar o Web Crawler
Popula o banco de dados MongoDB (db_livros_projeto, coleção livros) extraindo dados das páginas do site Books to Scrape:

Bash
python crawler/scraper.py

Passo 2: Iniciar a API REST (FastAPI)
Em um terminal separado (com o ambiente virtual ativo), inicie o servidor backend:

Bash
uvicorn api.main:app --reload
Documentação Interativa (Swagger UI): http://127.0.0.1:8000/docs

Endpoint de Registros: http://127.0.0.1:8000/items

Endpoint de Estatísticas: http://127.0.0.1:8000/stats

Passo 3: Iniciar o Dashboard (Streamlit)
Em outro terminal (com o ambiente virtual ativo), rode o painel visual:

Bash
streamlit run dashboard/app.py
Acesso ao Dashboard: http://localhost:8501