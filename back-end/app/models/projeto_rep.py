from connection import engine, metadata
import re
from sqlalchemy import select, insert, update, delete

PADRAO_TITULO = r"^[-,.~'a-zA-Z0-9\s]{2,20}$"
PADRAO_DESCRICAO = 255
PADRAO_CPF = r"^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"

projeto = metadata.tables.get("projeto")
if projeto is None:
    raise Exception("Tabela 'projeto' não encontrada no banco.")

usuario = metadata.tables.get("usuario")
if usuario is None:
    raise Exception("Tabela usuario não encontrada no banco")


def adicionar_projeto(titulo: str, descricao: str, cpf_dono: str):

    if not re.match(PADRAO_TITULO, titulo):
        raise ValueError ("Título Inválido: \n" 
                          "- Deve conter apenas letras, números e espaços \n "
                          "- Deve conter no máximo 20 caracteres \n")
    
    if len(descricao) > PADRAO_DESCRICAO:
        raise ValueError ("Descrição Inválida : \n" 
                          "- Deve conter no máximo 255 caracteres \n")
    
    if not re.match(PADRAO_CPF, cpf_dono):
        raise ValueError ("CPF Inválido : \n"
                            "- Deve conter apenas números. \n" 
                            "- Formato desejado : XXX.XXX.XXX-XX \n")


    stmt = insert(projeto).values(titulo_projeto=titulo, descricao=descricao, cpf=cpf_dono)

    with engine.begin() as conn:
        conn.execute(stmt)

  
def listar_todos_projetos():

    with engine.connect() as conn:
        result = conn.execute(select(projeto))
        projetos = [dict(row) for row in result.mappings()]
    return projetos


def buscar_projeto_por_id(projeto_id: int):

    with engine.connect() as conn:
        stmt = select(projeto).where(projeto.c.id_projeto == projeto_id)
        result = conn.execute(stmt).mappings().first()
    if result:
        return dict(result)
    else:
        print("Nenhum projeto encontrado.")
        return None   
 
def buscar_projetos_por_cpf_dono(cpf_dono: str):
    
    with engine.connect() as conn:
        result = conn.execute(select(projeto, usuario).select_from(projeto.join(usuario,
            projeto.c.cpf == usuario.c.cpf)).where(projeto.c.cpf==cpf_dono))
        projetos_do_cpf = [dict(row) for row in result.mappings()]
    return projetos_do_cpf

def atualizar_projeto(projeto_id: int, novo_titulo = None, nova_descricao=None):

    novos_valores = {}
    if novo_titulo:
        if not re.match(PADRAO_TITULO, novo_titulo):
            raise ValueError ("Título Inválido: \n" 
                              "- Deve conter apenas letras, números e espaços \n "
                              "- Deve conter no máximo 20 caracteres \n")
        novos_valores["titulo_projeto"] = novo_titulo

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
            raise ValueError("Nenhum projeto encontrado com esse id.")
        print(f"Projeto id: {id} atualizado com sucesso!")


def deletar_usuario(projeto_id: int):
    stmt = delete(projeto).where(projeto.c.id_projeto == projeto_id)

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhum usuário encontrado com esse CPF.")
        print(f"Projeto id: {projeto_id} atualizado com sucesso!")
    
# adicionar_projeto("Projeto01","Primeiro Projeto de engenharia de Software do Jonas","234.567.890-11")
# adicionar_projeto("Projeto02","Segundo Projeto de engenharia de Software do João","456.789.012-33")
# print(listar_todos_projetos())
print(buscar_projeto_por_id(2))
# print(buscar_projetos_por_cpf_dono("234.567.890-11"))
# atualizar_projeto(1,None,"Projeto Final de Engenharia de Software do Jonas")
# print(buscar_projeto_por_id(1))
# deletar_usuario(1)
