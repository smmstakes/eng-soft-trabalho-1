from .connection import engine, metadata
from sqlalchemy import select, insert, update, delete
import re
import bcrypt

PADRAO_TITULO = r"^[-,.~'a-zA-Z0-9\s]{2,20}$"
PADRAO_DESCRICAO = 255
PADRAO_CPF = r"^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"
PADRAO_SENHA = r"^(?=.*[A-Z])(?=.*[!@#$%&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$" 

projeto = metadata.tables.get("projeto")
if projeto is None:
    raise ConnectionError("Tabela 'projeto' não encontrada no banco.")

usuario = metadata.tables.get("usuario")
if usuario is None:
    raise ConnectionError("Tabela usuario não encontrada no banco")


def adicionar_projeto(titulo: str, descricao: str, senha: str, cpf_dono: str):

    if not re.match(PADRAO_TITULO, titulo):
        raise ValueError ("Título Inválido: \n"
                          "- Deve conter apenas letras, números e espaços \n "
                          "- Deve conter no máximo 20 caracteres \n")

    if len(descricao) > PADRAO_DESCRICAO:
        raise ValueError ("Descrição Inválida : \n"
                          "- Deve conter no máximo 255 caracteres \n")
    
    if not re.match(PADRAO_SENHA, senha):
        raise ValueError ("Senha Inválida :\n"
                            "- Deve conter pelo menos 1 letra Maiúscula, 1 letra Minúscula, 1 numérico e 1 caractere especial \n"
                            "- Deve conter entre 8 à 15 caracteres.")
    
    if not re.match(PADRAO_CPF, cpf_dono):
        raise ValueError ("CPF Inválido : \n"
                            "- Deve conter apenas números. \n"
                            "- Formato desejado : XXX.XXX.XXX-XX \n")

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    stmt = insert(projeto).values(titulo_projeto=titulo, descricao=descricao, senha=senha_hash, cpf=cpf_dono)

    with engine.begin() as conn:
        result = conn.execute(stmt)
        
        if result.inserted_primary_key:
            return result.inserted_primary_key[0]
        return None


def listar_todos_projetos():

    stmt = select(projeto.c.titulo_projeto, projeto.c.descricao, projeto.c.cpf)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        projetos = [dict(row) for row in result.mappings()]
    return projetos


def buscar_projeto_por_id(projeto_id: int):

    stmt = select(projeto.c.titulo_projeto, projeto.c.descricao, projeto.c.cpf).where(
        projeto.c.id_projeto == projeto_id)

    with engine.connect() as conn:
        result = conn.execute(stmt).mappings().first()

    if result is None:
        raise LookupError(f"{projeto_id} não encontrado")

    return dict(result)

def buscar_projetos_por_cpf_dono(cpf_dono: str):
    
    stmt = select(projeto.c.id_projeto, projeto.c.titulo_projeto, projeto.c.descricao, projeto.c.cpf).where(
        projeto.c.cpf == cpf_dono)
    
    with engine.connect() as conn:
        result = conn.execute(stmt)
        projetos_do_cpf = [dict(row) for row in result.mappings()]

    if not projetos_do_cpf:
        raise LookupError("projeto do cpf {cpf_dono} não encontrado")

    return projetos_do_cpf

def verificar_credenciais_projeto(titulo:str, cpf: str, senha_enviada: str):

    stmt = select(projeto).where(projeto.c.titulo_projeto == titulo ,projeto.c.cpf == cpf)
    
    with engine.connect() as conn:
        resultado = conn.execute(stmt).mappings().first()
        if resultado:
            projeto_encontrado = dict(resultado)
            senha_banco = projeto_encontrado['senha']

    if not projeto_encontrado:
        raise LookupError("Credenciais inválidas: Nenhum projeto encontrado")
    
    senha_enviada_bytes = senha_enviada.encode('utf-8')
    senha_hasheada_bytes = senha_banco.encode('utf-8')
    
    senha_bate = bcrypt.checkpw(senha_enviada_bytes, senha_hasheada_bytes)

    if not senha_bate:
        raise LookupError("Credenciais inválidas: Senha Incorreta")
    
    return projeto_encontrado 

def atualizar_projeto(projeto_id: int, novo_titulo = None, nova_senha=None, nova_descricao=None):

    novos_valores = {}
    if novo_titulo:
        if not re.match(PADRAO_TITULO, novo_titulo):
            raise ValueError ("Título Inválido: \n"
                              "- Deve conter apenas letras, números e espaços \n "
                              "- Deve conter no máximo 20 caracteres \n")
        novos_valores["titulo_projeto"] = novo_titulo

    if nova_senha:
        if not re.match(PADRAO_SENHA, nova_senha):
            raise ValueError ("Senha Inválida :\n"
                            "- Deve conter pelo menos 1 letra Maiúscula, 1 letra Minúscula, 1 numérico e 1 caractere especial \n"
                            "- Deve conter entre 8 à 15 caracteres.")
        senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        novos_valores["senha"] = senha_hash

    if nova_descricao:
        if len(nova_descricao) > 255:
            raise ValueError ("Descrição Inválida : \n"
                              "- Deve conter no máximo 255 caracteres \n")
        novos_valores["descricao"] = nova_descricao

    if not novos_valores:
        raise ValueError("Nenhum campo fornecido para atualização.")

    stmt = (
        update(projeto)
        .where(projeto.c.id_projeto == projeto_id).values(**novos_valores)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise LookupError("Nenhum projeto encontrado com esse id.")


def deletar_projeto(projeto_id: int):
    stmt = delete(projeto).where(projeto.c.id_projeto == projeto_id)

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise LookupError("Nenhum usuário encontrado com esse CPF.")
