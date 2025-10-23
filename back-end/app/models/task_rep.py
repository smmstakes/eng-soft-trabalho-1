from connection import engine, metadata
import re
from sqlalchemy import select, insert, update, delete, text, exists

task = metadata.tables.get("task")

def adicionar_task(id_sprint, cpf, nome_estado = None, descricao_task = None, nivel_task = None):
    stmt = insert(task).values(
        id_sprint=id_sprint,
        cpf=cpf,
        nome_estado=nome_estado,
        descricao_task=descricao_task,
        nivel_task=nivel_task
    )
    with engine.begin() as conn:
        conn.execute(stmt)

#busca task pelo cpf ou id_sprint e default busca todas as tasks 
def listar_task(cpf=None, id_sprint=None):
    stmt = select(task)
    if cpf:
        stmt = stmt.where(task.c.cpf == cpf)
    if id_sprint:
        stmt = stmt.where(task.c.id_sprint == id_sprint)
    
    with engine.connect() as conn:
        result = conn.execute(stmt)
        tasks = [dict(row) for row in result.mappings()]
    if not tasks:
        print("nenhuma task encontrada")
    return tasks

def atualizar_task(id_task, **novos_valores):
    if "cpf" in novos_valores:
        usuario = metadata.tables["usuario"]
        with engine.connect() as conn:
            usuario_existe = conn.scalar(
                select(exists().where(usuario.c.cpf == novos_valores["cpf"]))
            )
        if not usuario_existe:
            print(f"Usuário com CPF {novos_valores["cpf"]} não encontrado.")
            return None
    if "nome_estado" in novos_valores:
        estado_task = metadata.tables["estado_task"]
        with engine.connect() as conn:
            estado_existe = conn.scalar(
                select(exists().where(estado_task.c.nome_estado == novos_valores["nome_estado"]))
            )
        if not estado_existe:
            print(f"Estado '{novos_valores["nome_estado"]}' não encontrado.")
            return None
    if "nivel_task" in novos_valores:
        prioridade_task = metadata.tables["prioridade_task"]
        with engine.connect() as conn:
            prioridade_existe = conn.scalar(
                select(exists().where(prioridade_task.c.nivel_task == novos_valores["nivel_task"]))
            )
        if not prioridade_existe:
            print(f"Prioridade'{novos_valores["nivel_task"]}' não encontrada.")
            return None

    stmt = (
        update(task).where(task.c.id_task == id_task).values(**novos_valores)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhuma task encontrada com o ID {id_task}")
        print("Task atualizada com sucesso")

def deletar_task(id_task):
    stmt = delete(task).where(task.c.id_task == id_task)

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhuma task encontrada com esse ID.")
    print(" Task deletada com sucesso!")

#adicionar_task(id_sprint= 1, cpf="123.456.789-00", nome_estado="", descricao_task="", nivel_task="")
#atualizar_task(id_task=1, cpf="123.456.789-99", nome_estado="Em progresso", nivel_task= "Alta")
#deletar_task(2)
#print(listar_task(id_sprint=1))
