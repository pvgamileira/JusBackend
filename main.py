import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from supabase import Client, create_client


# ===== Criação da classe para cadastro e identificação de usuário =====
class NovoAdvogado(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: str
    num_oab: str
    senha: str


# ===== Criação da classe para atualizar advogados (campos opcionais) =====
class AtualizarAdvogado(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    num_oab: Optional[str] = None


# ===== Carregamento do .env e conexão com Supabase =====
load_dotenv()

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")
supabase: Optional[Client] = create_client(url, key) if (url and key) else None
if supabase and key:
    supabase.postgrest.auth(key)


def _obter_supabase() -> Client:
    if supabase is None:
        raise HTTPException(
            status_code=503,
            detail="Conexão com o Supabase não configurada. Verifique SUPABASE_URL e SUPABASE_KEY no arquivo .env.",
        )
    return supabase


def _validar_uuid(id_str: str) -> str:
    try:
        return str(uuid.UUID(id_str))
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de ID inválido (esperado UUID).")


# ===== Iniciando o FastAPI =====
app = FastAPI(
    title="JusBackend API",
    description="API RESTful para gestão e autenticação de advogados integrada ao Supabase Auth & PostgreSQL.",
    version="1.1.0",
)


# ===== Rota principal =====
@app.get("/")
def boas_vindas():
    return {"status": "API Jurídica operando com sucesso!"}


# ===== Rota para listar advogados (com filtro opcional por número/UF da OAB) =====
@app.get("/advogados")
def listar_advogados(num_oab: Optional[str] = Query(default=None, description="Filtrar por número ou UF da OAB")):
    db = _obter_supabase()
    query = db.table("advogados").select("*")
    if num_oab:
        query = query.ilike("num_oab", f"%{num_oab}%")
    dados = query.execute().data
    return {"advogados": dados, "total": len(dados)}


# ===== Rota para buscar um advogado específico por ID (UUID) =====
@app.get("/advogados/{id}")
def obter_advogado_por_id(id: str):
    id_valido = _validar_uuid(id)
    db = _obter_supabase()
    resultado = db.table("advogados").select("*").eq("id", id_valido).execute().data
    if not resultado:
        raise HTTPException(status_code=404, detail="Advogado não encontrado.")
    return {"advogado": resultado[0]}


# ===== Rota para criar advogados =====
# Sincroniza o usuário criado no Supabase Auth Admin (UUID) com a tabela public.advogados
@app.post("/advogados/", status_code=201)
def criar_advogado(dados: NovoAdvogado):
    db = _obter_supabase()
    resposta_auth = db.auth.admin.create_user({
        "email": dados.email,
        "password": dados.senha,
        "email_confirm": True,
    })
    new_id = resposta_auth.user.id

    criar = {
        "advogados": (
            db.table("advogados")
            .insert({
                "nome": dados.nome,
                "cpf": dados.cpf,
                "telefone": dados.telefone,
                "email": dados.email,
                "num_oab": dados.num_oab,
                "id": new_id,
            })
            .execute()
            .data
        )
    }
    return criar


# ===== Rota para atualizar advogados parcialmente =====
@app.put("/advogados/{id}")
def atualizar_advogado(dados: AtualizarAdvogado, id: str):
    id_valido = _validar_uuid(id)
    db = _obter_supabase()
    payload = dados.model_dump(exclude_unset=True)
    if not payload:
        raise HTTPException(status_code=400, detail="Nenhum campo informado para atualização.")
    atualizado = db.table("advogados").update(payload).eq("id", id_valido).execute().data
    if not atualizado:
        raise HTTPException(status_code=404, detail="Advogado não encontrado para atualização.")
    return {f"advogados/{id_valido}": atualizado}


# ===== Rota para excluir advogado (Banco + Supabase Auth Admin) =====
@app.delete("/advogados/{id}")
def deletar_advogado(id: str):
    id_valido = _validar_uuid(id)
    db = _obter_supabase()
    removido = db.table("advogados").delete().eq("id", id_valido).execute().data
    if not removido:
        raise HTTPException(status_code=404, detail="Advogado não encontrado para exclusão.")
    db.auth.admin.delete_user(id_valido)
    return {
        "status": "Advogado excluído com sucesso do banco e do sistema de autenticação",
        "dados_removidos": {f"advogados/{id_valido}": removido},
    }

