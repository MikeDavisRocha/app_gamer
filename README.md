# App Gamer API 🎮

API RESTful robusta e escalável para gerenciamento de jogos e consoles, desenvolvida com foco em Clean Architecture, performance assíncrona e segurança (RBAC).

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)

## 📑 Índice
- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Decisões Técnicas](#-decisões-técnicas)
- [Tecnologias](#-tecnologias)
- [Como Rodar Localmente](#-como-rodar-localmente)
- [Como Rodar os Testes](#-como-rodar-os-testes)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)

---

## Sobre o Projeto
Este projeto simula um backend real de produção para catalogação de videogames. O foco principal não é apenas o CRUD, mas a **maturidade de engenharia**, demonstrando:
* Autenticação segura (JWT + Refresh Token).
* Controle de Acesso Baseado em Função (RBAC - Admin vs User).
* Consistência de dados (Soft Delete e Integridade Referencial).
* Observabilidade (Logging Estruturado).

## 🏗 Arquitetura
O projeto segue rigorosamente os princípios da **Clean Architecture** para garantir desacoplamento, testabilidade e manutenibilidade a longo prazo.

A estrutura de pastas reflete as camadas:
1.  **Domain (`src/domain`):** O "coração" do software. Contém as Entidades (`User`, `Game`, `Console`) e Interfaces de Repositório. É pura e não depende de frameworks ou banco de dados.
2.  **Application (`src/application`):** Contém os Casos de Uso (Regras de Negócio) e DTOs. Orquestra o fluxo de dados entre o Domínio e a Interface.
3.  **Infrastructure (`src/infra`):** Implementações concretas. Banco de dados (SQLAlchemy/AsyncPG), Repositórios, Models do ORM e criptografia.
4.  **Interface (`src/interface`):** Camada de entrada. Controllers (Rotas FastAPI), Middlewares, Schemas de Request/Response e Tratamento de Exceções.

---

## 💡 Decisões Técnicas

### 1. Banco de Dados Assíncrono (AsyncPG + SQLAlchemy)
Optou-se pelo uso de drivers 100% assíncronos (`asyncpg`) para maximizar o throughput da API. O FastAPI brilha em cenários de alta concorrência (I/O Bound), e usar um driver síncrono seria um gargalo.

### 2. Estratégia de Deleção (Soft Delete)
Para garantir histórico e integridade, implementamos **Soft Delete** (`deleted_at`) para Consoles.
* **Regra de Negócio:** Ao deletar um console, ele não é removido fisicamente. Porém, a API garante consistência: jogos associados a consoles deletados deixam de aparecer nas listagens públicas, simulando uma exclusão em cascata lógica sem perda de dados.

### 3. Autenticação e Segurança
* **JWT & Refresh Token:** Implementado fluxo completo com `access_token` (curta duração) e `refresh_token` (longa duração) com rotação, mitigando riscos de roubo de credenciais.
* **Hashing:** Senhas protegidas com **Argon2**, o algoritmo vencedor da competição de hashing de senhas (mais seguro que BCrypt).
* **RBAC:** Decorators personalizados garantem que apenas `admins` acessem rotas críticas (DELETE).

### 4. Testes e Infraestrutura
* **Docker:** O banco de dados roda isolado em container, garantindo que o ambiente de dev/teste seja idêntico para todos os desenvolvedores.
* **Pytest Asyncio:** Configuração de policies de Event Loop específicas para garantir compatibilidade total com Windows e Linux.

---

## 🚀 Tecnologias
* **Linguagem:** Python 3.13
* **Framework:** FastAPI
* **ORM:** SQLAlchemy 2.0 (Async)
* **Migrations:** Alembic
* **Gerenciador de Deps:** Poetry
* **Linter/Formatter:** Ruff
* **Testes:** Pytest + HTTPX

---

## 🛠 Como Rodar Localmente

### Pré-requisitos
* Docker e Docker Compose instalados.
* Python 3.10+ e Poetry instalados (`pip install poetry`).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MikeDavisRocha/app-gamer.git
    cd app-gamer
    ```

2.  **Configure as variáveis de ambiente:**
    Copie o exemplo para o arquivo real.
    ```bash
    cp .env.example .env
    ```

3.  **Suba o Banco de Dados (Docker):**
    ```bash
    docker compose up -d
    ```

4.  **Instale as dependências e rode as migrações:**
    ```bash
    poetry install
    poetry run alembic upgrade head
    ```

5.  **Inicie a API:**
    ```bash
    poetry run task run
    ```
    Acesse a documentação automática em: **http://127.0.0.1:8000/docs**

---

## ✅ Como Rodar os Testes

O projeto possui uma suíte de testes robusta cobrindo unitários, integração e casos de borda.

```bash
poetry run pytest -v