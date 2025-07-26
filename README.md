# Cardenetinha - Seu Gerenciador Financeiro Inteligente

![Licença](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellowgreen.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-green.svg)

**Cardenetinha** é uma aplicação web desenvolvida com Flask e SQLite, projetada para ser um sistema inteligente e intuitivo de gerenciamento de finanças pessoais. O objetivo é oferecer aos usuários uma forma clara e eficiente de rastrear suas receitas e despesas, ganhar insights sobre seus hábitos de consumo e alcançar suas metas financeiras.

## Índice

* [Sobre o Projeto](#sobre-o-projeto)
* [Funcionalidades](#funcionalidades)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Como Iniciar](#como-iniciar)
    * [Pré-requisitos](#pré-requisitos)
    * [Instalação](#instalação)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Como Contribuir](#como-contribuir)
* [Licença](#licença)

## Sobre o Projeto

A ideia do **Cardenetinha** nasceu da necessidade de uma ferramenta simples, porém poderosa, para o controle financeiro pessoal. Em vez de planilhas complexas ou aplicativos com excesso de funcionalidades, o Cardenetinha foca no essencial: registro rápido de transações, categorização automática e visualização clara dos dados para tomada de decisões inteligentes.

## Funcionalidades

-   [x] **Autenticação de Usuários:** Sistema seguro de registro, login e logout.
-   [x] **Banco de Dados SQLite:** Armazenamento leve e eficiente dos dados do usuário.
-   [x] **Gestão de Contas:** Crie, edite, desabilite e visualize suas contas financeiras.
-   [x] **Gestão de Transações:** Registre transações de entrada e saída, com atualização automática do saldo da conta.
-   [x] **Histórico de Transações Paginado:** Visualize o histórico detalhado de transações por conta, com paginação.
-   [x] **Gestão de Categorias:** Crie, edite e visualize categorias para suas transações.
-   [x] **Dashboard Interativo:**
    -   Visão geral com total de receitas, despesas e saldo.
    -   Filtros por mês e ano para análise temporal.
    -   Gráfico de pizza com a distribuição de despesas por categoria.
-   [ ] **(Planejado) Categorização Inteligente:** Sugestão de categorias para novas transações.
-   [ ] **(Planejado) Metas e Orçamentos:** Definição de metas de economia e acompanhamento de orçamentos mensais.

## Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:

* **Backend:**
    * [Python 3](https://www.python.org/)
    * [Flask](https://flask.palletsprojects.com/)
    * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
    * [Flask-Login](https://flask-login.readthedocs.io/)
    * [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
* **Banco de Dados:**
    * [SQLite 3](https://www.sqlite.org/index.html)
* **Frontend:**
    * HTML5, CSS3, JavaScript
    * [Bootstrap 5](https://getbootstrap.com/)
    * [Chart.js](https://www.chartjs.org/) para visualização de dados.
    * [Select2](https://select2.org/) para caixas de seleção aprimoradas.
    * *Bibliotecas como Bootstrap, Select2 e jQuery são carregadas via CDN.*

## Como Iniciar

Para executar o projeto localmente, siga os passos abaixo.

### Pré-requisitos

Antes de começar, você vai precisar ter as seguintes ferramentas instaladas em sua máquina:
* [Git](https://git-scm.com)
* [Python 3.8+](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes do Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/cardenetinha.git](https://github.com/seu-usuario/cardenetinha.git)
    cd cardenetinha
    ```

2.  **Crie e ative um ambiente virtual:**
    * **Linux/macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *Um ambiente virtual é uma boa prática para isolar as dependências do projeto.*

3.  **Instale as dependências a partir do arquivo `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`.
    ```bash
    cp .env.example .env
    ```
    Abra o arquivo `.env` e preencha as variáveis necessárias, como a `SECRET_KEY`.

5.  **Execute a aplicação:**
    ```bash
    python run.py
    ```
    *O banco de dados `site.db` será criado automaticamente na raiz do projeto no primeiro acesso que envolver uma operação de banco de dados.*

6.  **Acesse no seu navegador:**
    Abra seu navegador e vá para `http://127.0.0.1:5000/`.

## Estrutura do Projeto
```
cardenetinha/
├── app/                
│   ├── __init__.py              
│   ├── models.py                
│   ├── routes.py               
│   ├── forms.py
│   ├── static/                  
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── detail.js
│   └── templates/               
│       ├── base.html
│       ├── dashboard.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── account/
│       │   ├── index.html
│       │   ├── new.html
│       │   ├── edit.html
│       │   └── detail.html
│       ├── category/
│       │   ├── edit.html
│       │   ├── index.html
│       │   └── new.html
│       └── transaction/
│           └── history.html
├── venv/                        
├── .gitignore                   
├── requirements.txt             
└── run.py                       
```

## Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito bem-vinda**.

Se desejar contribuir com o projeto, siga o fluxo de trabalho abaixo, que é um padrão para projetos no GitHub:

1.  **Faça um Fork do Projeto:** Clique no botão "Fork" no canto superior direito da página do repositório.
2.  **Crie uma Branch para sua Feature:**
    ```bash
    git checkout -b feature/sua-nova-feature
    ```
3.  **Faça o Commit de suas Alterações:** Utilize mensagens de commit claras, seguindo o padrão de [Conventional Commits](https://www.conventionalcommits.org/) se possível.
    ```bash
    git commit -m "feat: Adiciona funcionalidade de categorização de despesas"
    ```
4.  **Faça o Push para a sua Branch:**
    ```bash
    git push origin feature/sua-nova-feature
    ```
5.  **Abra um Pull Request:** Vá para a página do seu fork no GitHub e clique no botão "New pull request".

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
