import re
from connection import engine, metadata
from datetime import datetime, timedelta
from sqlalchemy import select, insert, update, delete

PADRAO_META = 100
PADRAO_REVISAO = 255
PADRAO_DATA = r"^\d{4}-\d{2}-\d{2}$"
FORMATO_DATA = '%Y-%m-%d'

sprint = metadata.tables.get("sprint")
if sprint is None:
    raise Exception("Tabela 'sprint' não encontrada no banco.")

user_story = metadata.tables.get("user_story")
if user_story is None:
    raise Exception("Tabela 'user_story' não encontrada no banco.")

user_story_sprint = metadata.tables.get("user_story_sprint")
if user_story_sprint is None:
    raise Exception("Tabela 'user_story_sprint' não encontrada no banco.")

projeto = metadata.tables.get("projeto")
if projeto is None:
    raise Exception("Tabela 'projeto' não encontrada no banco. ")

def adicionar_sprint(meta: str, inicio: str, termino: str, revisao_sprint: str, id_projeto: int):

    if len(meta) > PADRAO_META:
        raise ValueError ("Meta Inválida : \n"
                          "- Deve conter no máximo 100 caracteres \n")

    if len(revisao_sprint) > PADRAO_REVISAO:
        raise ValueError ("Revisão Inválida : \n"
                          "- Deve conter no máximo 255 caracteres \n")

    if not re.match(PADRAO_DATA, inicio) or not re.match(PADRAO_DATA, termino):
        raise ValueError ("Data Inválida : \n"
                          "- O formato deve ser AAAA-MM-DD (ex: 2025-10-01) \n")

    data_de_inicio = datetime.strptime(inicio, FORMATO_DATA).date()
    data_de_termino = datetime.strptime(termino, FORMATO_DATA).date()
    prazo = data_de_termino - data_de_inicio
    if prazo <= timedelta(days=0):
        raise ValueError ("Prazo Inválido : \n" \
                        "- A data de termino deve ser posterior à data de início \n")

    if prazo > timedelta(weeks =4):
        raise ValueError ("Prazo Inválido : \n" \
                        "- A duração da Sprint não pode exceder 4 semanas \n")

    with engine.connect() as conn:
        projeto_existe = conn.scalar(select(projeto.c.id_projeto).where(projeto.c.id_projeto == id_projeto))
        if not projeto_existe:
            raise ValueError(f"Projeto ID {id_projeto} não encontrado.")

    stmt = insert(sprint).values(
        meta = meta,
        inicio = data_de_inicio,
        termino = data_de_termino,
        revisao_sprint = revisao_sprint,
        id_projeto = id_projeto
    )

    with engine.begin() as conn:
        conn.execute(stmt)

def listar_todas_sprints():

    with engine.connect() as conn:
        result = conn.execute(select(sprint))
        sprints = [dict(row) for row in result.mappings()]
    return sprints

def buscar_sprint_por_id(sprint_id: int):

    with engine.connect() as conn:
        stmt = select(sprint).where(sprint.c.id_sprint == sprint_id)
        result = conn.execute(stmt).mappings().first()
    if result:
        return dict(result)
    else:
        print("Nenhuma sprint encontrada.")
        return None

def buscar_sprint_por_projeto(id_projeto: int):

    with engine.connect() as conn:
        stmt = select(sprint).where(sprint.c.id_projeto == id_projeto)
        result = conn.execute(stmt)
        sprints_do_projeto = [dict(row) for row in result.mappings()]
        if sprints_do_projeto:
            return sprints_do_projeto
        else:
            print("Nenhuma sprint encontrada.")
            return None

def atualizar_sprint(sprint_id: int, nova_meta = None, novo_inicio = None, novo_termino = None, nova_revisao_sprint = None):

    novos_valores = {}
    if nova_meta:
        if len(nova_meta) > PADRAO_META:
            raise ValueError ("Meta Inválida : \n"
                                "- Deve conter no máximo 100 caracteres \n")
        novos_valores["meta"] = nova_meta

    if nova_revisao_sprint:
        if len(nova_revisao_sprint) > PADRAO_REVISAO:
            raise ValueError ("Revisão Inválida : \n"
                                "- Deve conter no máximo 255 caracteres \n")
        novos_valores["revisao_sprint"] = nova_revisao_sprint

    if novo_inicio or novo_termino:
        with engine.connect() as conn_check:
            stmt_check = select(sprint).where(sprint.c.id_sprint == sprint_id)
            sprint_atual = conn_check.execute(stmt_check).mappings().first()
            if sprint_atual is None:
                raise ValueError("Nenhuma Sprint encontrada.")
            inicio_resolvido = novo_inicio if novo_inicio is not None else str(sprint_atual['inicio'])
            termino_resolvido = novo_termino if novo_termino is not None else str(sprint_atual['termino'])
            if not re.match(PADRAO_DATA, inicio_resolvido) or not re.match(PADRAO_DATA, termino_resolvido):
                raise ValueError ("Data Inválida : \n"
                                "- O formato deve ser AAAA-MM-DD (ex: 2025-10-01) \n")
            data_de_inicio = datetime.strptime(inicio_resolvido, FORMATO_DATA).date()
            data_de_termino = datetime.strptime(termino_resolvido, FORMATO_DATA).date()
            prazo = data_de_termino - data_de_inicio
            if prazo <= timedelta(days=0):
                raise ValueError ("Prazo Inválido : \n" \
                                "- A data de termino deve ser posterior à data de início \n")
            if prazo > timedelta(weeks=4):
                raise ValueError ("Prazo Inválido : \n" \
                                "- A duração da Sprint não pode exceder 4 semanas \n")
            if novo_inicio is not None:
                novos_valores["inicio"] = data_de_inicio
            if novo_termino is not None:
                novos_valores["termino"] = data_de_termino
    if not novos_valores:
        raise ValueError("Nenhum campo fornecido para atualização.")

    stmt = (
        update(sprint)
        .where(sprint.c.id_sprint == sprint_id)
        .values(**novos_valores)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Nenhuma Sprint encontrada com o ID: {sprint_id}.")
        print(f"Sprint ID: {sprint_id} atualizada com sucesso!")

def deletar_sprint(sprint_id: int):

    stmt = delete(sprint).where(sprint.c.id_sprint == sprint_id)
    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Nenhuma Sprint encontrada com o ID: {sprint_id}.")
        print(f"Sprint ID: {sprint_id} deletada com sucesso!")