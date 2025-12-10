Markdown

# 🏋️‍♂️ GymBro API

Backend robusto desenvolvido em **Django REST Framework** para gerenciar a aplicação mobile GymBro. Responsável pela autenticação, persistência de treinos, perfis de usuários e catálogo de exercícios.

## 🚀 Tecnologias

- **Python 3.10+**
- **Django 5.x**
- **Django REST Framework**
- **JWT (Simple JWT)** para Autenticação Segura
- **SQLite** (Banco de Dados)
- **CORS Headers** (Integração com Frontend)

## ⚙️ Funcionalidades

- ✅ **Auth:** Login, Cadastro e Renovação de Token (JWT).
- ✅ **Perfil:** Gestão de dados do atleta (Medidas, Endereço, CPF).
- ✅ **Exercícios:** Sistema híbrido (Exercícios Globais do Sistema + Customizados do Usuário).
- ✅ **Fichas:** Criação de treinos personalizados com séries, repetições e carga.
- ✅ **Cardio:** Registro de atividades aeróbicas.

## 📦 Como Rodar

1. **Clone o repositório:**
   ```bash
   git clone <SEU_LINK_DO_GITHUB_BACKEND>
   cd gymbro-backend

    Crie e ative o ambiente virtual:
    Bash

python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

Instale as dependências:
Bash

pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

Aplique as migrações:
Bash

python manage.py migrate

(Opcional) Popule o banco com exercícios padrão:

    Execute o script de população via python manage.py shell.

Rode o servidor:
Bash

    python manage.py runserver

👨‍💻 Squad de Desenvolvimento
Nome	Cargo
Davi	Full Stack Developer
Thiago Ribeiro	Back-end Developer
João Rafael	Front-end Developer
André	QA / Tester
