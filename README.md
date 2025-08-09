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

A ideia do **Cardenetinha** nasceu da necessidade de uma ferramenta simples, porém poderosa, para o controle financeiro pessoal. Em vez de planilhas complexas ou aplicativos com excesso de funcionalidades, o Cardenetinha foca no essencial: registro rápido de transações, categorização automática e visualização clara dos dados para tomada de decisões inteligentes, tudo isso com uma interface intuitiva e visualmente agradável.

## Funcionalidades

-   [x] **Autenticação de Usuários:** Sistema seguro de registro, login e logout.
-   [x] **Perfil de Usuário:** Visualize e atualize suas informações, incluindo nome de usuário, e-mail e senha.
-   [x] **Banco de Dados SQLite:** Armazenamento leve e eficiente dos dados do usuário.
-   [x] **Gestão de Contas:** Crie, edite, desabilite e visualize suas contas financeiras.
-   [x] **Gestão de Transações:** Registre transações de entrada e saída, com atualização automática do saldo da conta.
-   [x] **Histórico de Transações Avançado:**
    -   Visualização detalhada e paginada do histórico de transações por conta.
    -   Filtros por descrição, categoria e período (data).
    -   Opção para limpar os filtros aplicados.
-   [x] **Gestão de Categorias:** Crie, edite e visualize categorias para suas transações.
-   [x] **Gestão de Metas:** Defina metas financeiras vinculadas a contas específicas, com acompanhamento automático do progresso percentual.
-   [x] **Dashboard Interativo:**
    -   Visão geral com total de receitas, despesas e saldo.
    -   Filtros por mês, ano e conta para análise temporal.
    -   Gráfico de pizza com a distribuição de despesas por categoria.
    -   Exibição do saldo global ou por conta selecionada.
-   [x] **Relatórios Detalhados:**
    -   Gere relatórios de entradas e saídas por período (data de início e fim).
    -   Filtre os relatórios por conta específica ou todas as contas.
    -   Visualize os totais de entrada, saída e o balanço do período.
    -   Exporte os relatórios para CSV.
-   [x] **Planejamento Financeiro:**
    -   Adicione despesas e receitas futuras para planejar o mês.
    -   Visualize o balanço mensal projetado (entradas vs. despesas).
    -   Edite e exclua itens do planejamento.
    -   Interface com abas para melhor organização.
-   [x] **Menu Otimizado:** Navegação mais limpa com um menu dropdown para acesso rápido ao perfil, categorias, metas e logout.
-   [ ] **(Planejado) Categorização Inteligente:** Sugestão de categorias para novas transações.
-   [ ] **(Planejado) Metas e Orçamentos:** Definição de metas de economia e acompanhamento de orçamentos mensais.

## Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:

* **Backend:**
    * [Python 3](https://www.python.org/)
    * [Flask](https://flask.palletsprojects.com/)
    * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
    * [Flask-Login](https://flask-login.readthedocs.io/)
    * [Flask-Migrate](https://flask-migrate.readthedocs.io/)
    * [WTForms-SQLAlchemy](https://wtforms-sqlalchemy.readthedocs.io/)
* **Banco de Dados:**
    * [SQLite 3](https://www.sqlite.org/index.html)
* **Frontend:**
    * HTML5, CSS3, JavaScript
    * [Bootstrap 5](https://getbootstrap.com/)
    * [Chart.js](https://www.chartjs.org/) para visualização de dados.
    * [Select2](https://select2.org/) para caixas de seleção aprimoradas.

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
    git clone https://github.com/profadevairvitorio/cardenetinha.git
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

5.  **Execute as migrações do banco de dados:**
    ```bash
    flask db upgrade
    ```

6.  **Execute a aplicação:**
    ```bash
    python run.py
    ```

7.  **Acesse no seu navegador:**
    Abra seu navegador e vá para `http://127.0.0.1:5000/`.

## Estrutura do Projeto

```
cardenetinha/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── account_form.py
│   │   ├── category_form.py
│   │   ├── edit_account_form.py
│   │   ├── financial_plan_form.py
│   │   ├── goal_form.py
│   │   ├── login_form.py
│   │   ├── registration_form.py
│   │   ├── report_form.py
│   │   ├── transaction_form.py
│   │   └── update_profile_form.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── category.py
│   │   ├── financial_plan.py
│   │   ├── goal.py
│   │   ├── transaction.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── account_routes.py
│   │   ├── category_routes.py
│   │   ├── dependencies.py
│   │   ├── financial_planning_routes.py
│   │   ├── goal_routes.py
│   │   ├── main_routes.py
│   │   ├── profile_routes.py
│   │   ├── report_routes.py
│   │   └── transaction_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── report_service.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   ├── select2.min.css
│   │   │   └── style.css
│   │   └── js/
│   │       ├── bootstrap.bundle.min.js
│   │       ├── dashboard.js
│   │       ├── detail.js
│   │       ├── jquery.min.js
│   │       └── select2.min.js
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── index.html
│       ├── login.html
│       ├── financial_planning.html
│       ├── register.html
│       ├── report.html
│       ├── account/
│       │   ├── detail.html
│       │   ├── edit.html
│       │   ├── index.html
│       │   └── new.html
│       ├── category/
│       │   ├── edit.html
│       │   ├── index.html
│       │   └── new.html
│       ├── financial_planning/
│       │   └── _items_table.html
│       ├── goal/
│       │   ├── edit.html
│       │   ├── index.html
│       │   └── new.html
│       ├── perfil/
│       │   ├── edit.html
│       │   └── index.html
│       └── transaction/
│           ├── history.html
│           └── new.html
├── migrations/
├── .gitignore
├── config.py
├── LICENSE
├── README.md
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

Este projeto está licenciado sob a **Creative Commons Attribution-NonCommercial 4.0 International Public License (CC BY-NC 4.0)**.
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
