from .connection import engine, metadata
import re
from sqlalchemy import select, insert, update, delete

user_story_sprint = metadata.tables.get("user_story_sprint")
user_story = metadata.tables.get("user_story")
sprint = metadata.tables.get("sprint")

def adicionar_user_story_sprint(id_user_story, id_sprint):
    stmt = insert(user_story_sprint).values(
        id_user_story=id_user_story,
        id_sprint=id_sprint
    )

    with engine.begin() as conn:
        story_existe = conn.scalar(
            select(user_story.c.id_user_story).where(user_story.c.id_user_story == id_user_story)
        )
        sprint_existe = conn.scalar(
            select(sprint.c.id_sprint).where(sprint.c.id_sprint == id_sprint)
        )
        if not story_existe:
            raise Exception(f"User Story {id_user_story} não encontrada.")
        if not sprint_existe:
            raise Exception(f"Sprint {id_sprint} não encontrada.")
        
        conn.execute(stmt)

#lista as relações de user story com sprint. pode filtrar com id da sprint ou user story
def listar_user_story_sprints(id_user_story=None, id_sprint=None):
    stmt = select(user_story_sprint)

    if id_user_story:
        stmt = stmt.where(user_story_sprint.c.id_user_story == id_user_story)
    if id_sprint:
        stmt = stmt.where(user_story_sprint.c.id_sprint == id_sprint)

    with engine.connect() as conn:
        result = conn.execute(stmt).mappings().all()
        relacoes = [dict(row) for row in result]

    if not relacoes:
        raise ValueError("Nenhuma relação encontrada.")
    return relacoes

#atualiza a sprint relacionada a user story
def atualizar_user_story_sprint(id_user_story, id_sprint_antigo, id_sprint_novo):
    stmt = (
        update(user_story_sprint)
        .where(
            (user_story_sprint.c.id_user_story == id_user_story)
            & (user_story_sprint.c.id_sprint == id_sprint_antigo)
        )
        .values(id_sprint=id_sprint_novo)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhuma relação encontrada para atualizar.")
        print("Relação atualizada com sucesso!")

#remove a relação entre user story e sprint
def deletar_user_story_sprint(id_user_story, id_sprint):
    stmt = (
        delete(user_story_sprint)
        .where(
            (user_story_sprint.c.id_user_story == id_user_story)
            & (user_story_sprint.c.id_sprint == id_sprint)
        )
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhuma relação encontrada para excluir.")
        print("Relação excluída com sucesso!")

#