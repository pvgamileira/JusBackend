# JusBackend ⚖️

Uma API REST desenvolvida em **FastAPI** e integrada ao **Supabase** para gerenciamento e cadastro de advogados. O projeto conta com um sistema de autenticação (via Supabase Auth Admin) e persistência de dados.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework moderno, rápido (de alto desempenho) e fácil de usar para construir APIs com Python.
- **Supabase**: Backend-as-a-Service (BaaS) utilizado para o banco de dados PostgreSQL e gerenciamento de autenticação.
- **Pydantic**: Validação de dados e definição de esquemas.
- **Uvicorn**: Servidor ASGI rápido para rodar a aplicação.

## 📂 Estrutura do Projeto

* `main.py`: Arquivo principal contendo a definição das rotas e inicialização do FastAPI.
* `.env`: Configurações de credenciais do Supabase (ignorado pelo Git por segurança).
* `.gitignore`: Arquivo para evitar o versionamento de arquivos locais desnecessários ou sensíveis.

## 🛣️ Endpoints da API

A API disponibiliza as seguintes rotas:

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| **GET** | `/` | Rota principal de boas-vindas. |
| **GET** | `/advogados` | Lista todos os advogados cadastrados no banco de dados. |
| **POST** | `/advogados/` | Cadastra um novo advogado. Cria o usuário no Supabase Auth e insere os dados de perfil na tabela `advogados`. |
| **PUT** | `/advogados/{id}` | Atualiza parcialmente os dados de um advogado existente com base no seu UUID. |
| **DELETE** | `/advogados/{id}` | Remove um advogado da tabela `advogados` e também exclui o seu usuário correspondente do Supabase Auth. |

---

## 🛠️ Como Executar o Projeto

1. **Instale as dependências** no seu ambiente virtual:
   ```bash
   pip install fastapi uvicorn supabase python-dotenv pydantic
   ```

2. **Configure as variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do projeto com as seguintes chaves obtidas no painel do seu projeto no Supabase:
   ```env
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_key_service_role_ou_anon_do_supabase
   ```

3. **Inicie o servidor local**:
   ```bash
   .venv/bin/uvicorn main:app --reload
   ```

4. **Acesse a documentação interativa**:
   Abra o seu navegador em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para testar os endpoints interativamente através do Swagger UI.
