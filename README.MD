# 🏋️‍♂️ Gymbro API - Backend

> "Shut up and train." 🐍

Esta é a API RESTful que alimenta o ecossistema **Gymbro**. Construída com **Django REST Framework**, ela gerencia toda a lógica de negócios, autenticação, banco de dados e processamento de treinos e atividades cardiovasculares.

## 🧠 Funcionalidades do Backend

* **🔐 Autenticação Robusta:**
    * Login e Registro com Token Authentication.
    * Proteção contra duplicidade de dados (CPF/Email únicos).
* **💪 Gestão de Treinos (Core):**
    * **Catálogo Híbrido:** Exercícios globais (padrão) e customizados (criados pelo usuário).
    * **Fichas de Treino:** CRUD completo de fichas.
    * **Itens de Treino:** Adição de exercícios com séries, repetições, carga e tempo.
* **🏃 Módulo Cardio:**
    * Armazenamento de sessões de corrida.
    * Suporte a dados complexos de GPS (JSONField).
    * Cálculo automático de velocidade média.
* **🔎 Segurança:** Permissions (IsAuthenticated) e ReadOnly fields garantindo integridade.

## 🛠️ Tecnologias

* **Linguagem:** Python 3.x
* **Framework:** Django 5.x
* **API Toolkit:** Django REST Framework (DRF)
* **Banco de Dados:** SQLite (Desenvolvimento)

## ⚙️ Como Rodar a API Localmente

### Pré-requisitos
* Python instalado.
* Virtualenv (recomendado).

### Passos
1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SeuUsuario/Gymbro-API.git](https://github.com/SeuUsuario/Gymbro-API.git)
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Realize as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```
5.  Inicie o servidor:
    ```bash
    python manage.py runserver
    ```
    *A API estará rodando em:* `http://127.0.0.1:8000/`

## 📡 Endpoints Principais

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/login/` | Autenticação e obtenção de Token |
| `POST` | `/api/register/` | Cadastro de novo usuário |
| `GET/POST` | `/api/exercicios/` | Lista exercícios (Globais + Meus) ou cria Custom |
| `GET/POST` | `/api/fichas/` | Gerencia fichas de treino |
| `POST` | `/api/fichas/<id>/itens/` | Adiciona exercício na ficha |
| `GET/POST` | `/api/cardios/` | Registra e lista corridas |

---
Desenvolvido por **DaviCuscuz** 🚀