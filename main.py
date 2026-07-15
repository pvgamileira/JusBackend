import os

from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from supabase import Client, create_client
from typing import Optional


#=====Criação da classe para cadastro=====
#=====e identificação de usuário==========
class NovoAdvogado(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: str
    num_oab: str
    senha: str 

#=====Criação da classe para atualizar advogados deixando a opção deles como optional=====
#=====para o update não fizer esses dados atualizarem para none===========================
class AtualizarAdvogado(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    num_oab: Optional[str] = None
    

#=====Carregamento do .env e conexão com supabase=====
load_dotenv()

#=====Colocando as variáveis do .env em variáveis do python=====
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
supabase.postgrest.auth(key)

# =====Iniciando o FastAPI =====
app = FastAPI()

# =====Rota principal =====
@app.get("/")
def boas_vindas():
    status = {"status": "API Jurídica operando com sucesso!"}
    return status


# =====Rota para listar advogados===== 
# =====Usando a sintaxe do supabase===== 
# =====pela primeira vez após leve consulta na DOC=====
@app.get("/advogados")
def listar_advogados():
    resposta = {"advogados": supabase.table("advogados").select("*").execute().data}
    return resposta



#=====Rota para criar advogados=====
#=====uso de create_user do supabase auth admin =====
#=====criação da inserção do usuário com email e senha =====
#=====para verificação da tabela auth para bater e enviar os dados =====
#=====para a tabela advogados=========================================
@app.post("/advogados/")
def criar_advogado(dados: NovoAdvogado):
    resposta_auth = supabase.auth.admin.create_user({
        "email": dados.email,
        "password": dados.senha,
        "email_confirm": True
    })
    new_id = resposta_auth.user.id

    criar = {
        "advogados": (
            supabase.table("advogados")
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



#=====Rota para atualizar advogados===== 
#=====atualizando somente o que não está===== 
#=====como optional=None=====================
#=====Primeiro uso do update entendendo que o 'where' é===== 
#=====o .eq no final da linha================================
@app.put('/advogados/{id}')
def atualizar_advogado(dados: AtualizarAdvogado, id: str):
    resposta_update = {
        f"advogados/{id}": supabase.table("advogados").update(dados.model_dump(exclude_unset=True)).eq('id',id).execute().data
    }
    return resposta_update


@app.delete('/advogados/{id}')
def deletar_advogado(id: str):
    resposta_delete = {f"advogados/{id}": supabase.table("advogados").delete().eq('id', id).execute().data}
    supabase.auth.admin.delete_user(id)
    resposta_delete = {
        'status': "Advogado excluído com sucesso do banco e do sistema de autenticação",
        'dados_removidos': resposta_delete   
    }
    return resposta_delete
