import re
from connection import engine, metadata
from sqlalchemy import select, insert, update, delete

PADRAO_NOME = r"^[a-zA-Z\s]{2,20}$"
PADRAO_OBJETIVO = 100
PADRAO_BENEFICIO = 255
PADRAO_PRIORIDADE = r"Alta|Media|Baixa"

user_story = metadata.tables.get("user_story")
if user_story is None:
    raise Exception("Tabela 'user_story' não encontrada no banco.")

projeto = metadata.tables.get("projeto")
if projeto is None:
    raise Exception("Tabela 'projeto' não encontrada no banco.")

prioridade_story = metadata.tables.get("prioridade_story")
if prioridade_story is None:
    raise Exception("Tabela 'prioridade_story' não encontrada no banco.")

def adicionar_user_story(id_projeto: int, titulo_user_story: str, objetivo: str, beneficio: str, prioridade: str):

    if not re.match(PADRAO_NOME, titulo_user_story):
        raise ValueError ("Nome Inválido :\n"
                            "-Deve conter apenas letras e espaço, sem acentuação \n"
                            "-Deve conter entre 2 à 20 caracteres.")

    if len(objetivo) > PADRAO_OBJETIVO:
        raise ValueError ("Objetivo Inválida : \n"
                          "- Deve conter no máximo 100 caracteres \n")

    if len(beneficio) > PADRAO_BENEFICIO:
        raise ValueError ("Descrição Inválida : \n"
                          "- Deve conter no máximo 255 caracteres \n")

    if not re.fullmatch (PADRAO_PRIORIDADE, prioridade):
        raise ValueError ("Prioridade Inválida : \n" \
                            "- Deve ser 'Alta', 'Média' ou 'Baixa'")

    with engine.connect() as conn:
        stmt_proj = select(projeto).where(projeto.c.id_projeto == id_projeto)
        if conn.execute(stmt_proj).fetchone() is None:
            raise ValueError(f"Projeto com ID {id_projeto} não existe. User Story não pode ser criada.")

    stmt = insert(user_story).values(
        id_projeto=id_projeto,
        titulo_user_story=titulo_user_story,
        objetivo=objetivo,
        beneficio=beneficio,
        nivel_story=prioridade
        )

    with engine.begin() as conn:
        conn.execute(stmt)

def listar_todas_user_stories():

    with engine.connect() as conn:
        result = conn.execute(select(user_story))
        user_stories = [dict(row) for row in result.mappings()]
    return user_stories

def buscar_user_story_por_id(user_story_id: int):

    with engine.connect() as conn:
        stmt = select(user_story).where(user_story.c.id_user_story == user_story_id)
        result = conn.execute(stmt).mappings().first()
        if result:
            return dict(result)
        else:
            print("Nenhuma user_story encontrada.")
            return None

def buscar_user_stories_por_projeto(id_projeto: int):

    with engine.connect() as conn:
        stmt = select(user_story).where(user_story.c.id_projeto == id_projeto)
        result = conn.execute(stmt)
        user_stories_do_projeto = [dict(row) for row in result.mappings()]
        if user_stories_do_projeto:
            return user_stories_do_projeto
        else:
            print("Nenhuma user_story encontrada.")
            return []

def atualizar_user_story(user_story_id: int, novo_titulo_user_story = None, novo_objetivo = None, novo_beneficio = None, nova_prioridade = None):

    novos_valores = {}
    if novo_titulo_user_story:
        if not re.match(PADRAO_NOME, novo_titulo_user_story):
            raise ValueError ("Nome Inválido :\n"
                                "-Deve conter apenas letras e espaço, sem acentuação \n"
                                "-Deve conter entre 2 à 20 caracteres.")
        novos_valores["titulo_user_story"] = novo_titulo_user_story

    if novo_objetivo:
        if len(novo_objetivo) > PADRAO_OBJETIVO:
            raise ValueError ("Objetivo Inválida : \n"
                                  "- Deve conter no máximo 100 caracteres \n")
        novos_valores["objetivo"] = novo_objetivo

    if novo_beneficio:
        if len(novo_beneficio) > PADRAO_BENEFICIO:
            raise ValueError ("Descrição Inválida : \n"
                                "- Deve conter no máximo 255 caracteres \n")
        novos_valores["beneficio"] = novo_beneficio

    if nova_prioridade:
        if not re.fullmatch (PADRAO_PRIORIDADE, nova_prioridade):
            raise ValueError ("Prioridade Inválida : \n" \
                                "- Deve ser 'Alta', 'Média' ou 'Baixa'")
        novos_valores["nivel_story"] = nova_prioridade

    if not novos_valores:
        raise ValueError("Nenhum campo fornecido para atualização.")

    stmt = (
        update(user_story)
        .where(user_story.c.id_user_story == user_story_id)
        .values(**novos_valores)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Nenhuma User Story encontrada com o ID: {user_story_id}.")
        print(f"User Story ID: {user_story_id} atualizada com sucesso!")

def deletar_user_story(user_story_id: int):

    stmt = delete(user_story).where(user_story.c.id_user_story == user_story_id)
    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Nenhuma User Story encontrada com o ID: {user_story_id}.")
        print(f"User Story ID: {user_story_id} deletada com sucesso!")