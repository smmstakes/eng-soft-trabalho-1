from .connection import engine, metadata
from sqlalchemy import select, insert, update, delete, and_
import re 


PADRAO_CPF = r"^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"
PADRAO_FUNCAO = ["Dono do Produto", "Scrum Master", "Desenvolvedor"]

usuario_projeto = metadata.tables.get("usuario_projeto")
usuario = metadata.tables.get("usuario")
projeto = metadata.tables.get("projeto")
funcao = metadata.tables.get("funcao")

if usuario_projeto is None:
    raise Exception("Tabela 'usuario_projeto' não foi encontrada no banco.")
if usuario is None:
    raise Exception("Tabela usuario não foi encontrada no banco")
if projeto is None:
    raise Exception("Tabela projeto não foi encontrada no banco")
if funcao is None:
    raise Exception("Tabela função não foi encontrada no banco")

def adicionar_usuario_projeto(cpf: str, id_projeto: int, nome_funcao: str):
    
    if not isinstance(id_projeto, int):
        raise ValueError ("ID do Projeto Inválido.")
    
    if not re.match(PADRAO_CPF, cpf):
        raise ValueError ("CPF Inválido : \n"
                            "- Deve conter apenas números. \n" 
                            "- Formato desejado : XXX.XXX.XXX-XX \n")
    
    if nome_funcao not in PADRAO_FUNCAO:
        raise ValueError ("Função Inexistente \n" \
                          "- Dono do Produto, Scrum Master ou Desenvolvedor \n")

    stmt = insert(usuario_projeto).values(cpf = cpf, id_projeto = id_projeto, nome_funcao = nome_funcao)
    
    with engine.begin() as conn:
            conn.execute(stmt)


# Um usuário pode estar em vários projetos. Essa função lista todos seus projetos  
def listar_projeto_de_usuarios(cpf: str):

    if not re.match(PADRAO_CPF, cpf):
        raise ValueError ("CPF Inválido : \n"
                            "- Deve conter apenas números. \n" 
                            "- Formato desejado : XXX.XXX.XXX-XX \n")  
    
    stmt = select(usuario_projeto).where(usuario_projeto.c.cpf == cpf)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        lista_projetos = [dict(row) for row in result.mappings()]
    return lista_projetos

# Um projeto pode ter vários usuários. Essa função lista todos os usuarios 
def listar_usuarios_em_projeto(projeto_id: int):
    
    if not isinstance(projeto_id, int):
        raise ValueError ("ID do Projeto Inválido.")
 
    stmt = select(usuario_projeto).where(usuario_projeto.c.id_projeto == projeto_id)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        lista_usuarios = [dict(row) for row in result.mappings()]
    return lista_usuarios


def atualizar_usuario_projeto(cpf: str, projeto_id: int, nova_funcao: str):

    if not isinstance(projeto_id, int):
        raise ValueError ("ID do Projeto Inválido.")
    
    if not re.match(PADRAO_CPF, cpf):
        raise ValueError ("CPF Inválido : \n"
                            "- Deve conter apenas números. \n" 
                            "- Formato desejado : XXX.XXX.XXX-XX \n")
    
    if nova_funcao not in PADRAO_FUNCAO:
        raise ValueError ("Função Inexistente \n" \
                          "- Dono do Produto, Scrum Master ou Desenvolvedor \n")

    stmt = (
        update(usuario_projeto)
        .where(and_(usuario_projeto.c.cpf == cpf, usuario_projeto.c.id_projeto == projeto_id))
        .values(nome_funcao = nova_funcao)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhuma associação encontrado com esse ID e CPF.")
        print(f"Função para {nova_funcao}, Projeto id: {projeto_id}, CPF: {cpf} atualizado com sucesso!")


def deletar_usuario_projeto(cpf: str, projeto_id: int):
    stmt = delete(usuario_projeto).where(and_(usuario_projeto.c.cpf == cpf, usuario_projeto.c.id_projeto == projeto_id))

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Nenhum usuário encontrado com esse CPF.")
        print(f"Usuario CPF: {cpf} removido com sucesso!")