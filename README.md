# JusBackend ⚖️ — API RESTful Jurídica (FastAPI + Supabase)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20%26%20PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

API RESTful desenvolvida **100% à mão em Python** com **FastAPI**, **Pydantic** e **Supabase** para gerenciamento cadastral e autenticação de advogados.

O objetivo central deste projeto foi consolidar na prática os fundamentos de arquitetura Back-End REST, validação de esquemas de entrada/saída, tratamento de códigos de status HTTP (`200`, `201`, `404`) e sincronização transacional entre o **Supabase Auth Admin (`UUID`)** e a tabela relacional `public.advogados` no **PostgreSQL**.

---

## ⚙️ Arquitetura e Destaques Técnicos

- **Sincronização Identidade ↔ Banco Relacional**:
  - No `POST /advogados/`, a API provisiona primeiro a credencial de acesso via `supabase.auth.admin.create_user()`, captura o `UUID` gerado (`resposta_auth.user.id`) e o utiliza como chave primária/estrangeira na tabela `advogados`.
  - No `DELETE /advogados/{id}`, realiza a exclusão combinada tanto do registro relacional quanto da conta de autenticação no Supabase Auth.
- **Atualização Parcial Segura (`PUT /advogados/{id}`)**:
  - Uso de `dados.model_dump(exclude_unset=True)` do Pydantic v2 para atualizar no PostgreSQL apenas os campos efetivamente enviados na requisição, evitando sobrescrever colunas existentes com `NULL`.
- **Busca por ID e Filtragem por OAB**:
  - Consulta individual (`GET /advogados/{id}`) com tratamento explícito de erro `404 Not Found` via `HTTPException` e busca filtrada por número/UF de OAB (`GET /advogados?num_oab=SP`).

---

## 🛣️ Endpoints da API

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **GET** | `/` | Healthcheck da API Jurídica. |
| **GET** | `/advogados` | Lista advogados cadastrados (aceita query param opcional `?num_oab=`). |
| **GET** | `/advogados/{id}` | Busca um advogado específico pelo seu `UUID` (retorna `404` se inexistente). |
| **POST** | `/advogados/` | Cria usuário no Supabase Auth Admin e persiste o perfil na tabela `advogados`. |
| **PUT** | `/advogados/{id}` | Atualiza parcialmente os dados de um advogado existente (`exclude_unset=True`). |
| **DELETE** | `/advogados/{id}` | Remove o advogado da tabela `advogados` e exclui sua conta no Supabase Auth. |

---

## 🛠️ Como Executar Localmente

1. **Instale as dependências**:
   ```bash
   pip install fastapi uvicorn supabase python-dotenv pydantic
   ```

2. **Configure as variáveis de ambiente (`.env`)**:
   ```env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua_service_role_key_do_supabase
   ```

3. **Inicie o servidor ASGI**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Documentação Interativa (Swagger UI)**:
   Acesse `http://127.0.0.1:8000/docs`.
