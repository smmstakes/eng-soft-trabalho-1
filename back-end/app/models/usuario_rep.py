from .connection import engine, metadata
import re
from sqlalchemy import select, insert, update, delete, text

PADRAO_NOME = r"^[a-zA-Z\s]{2,20}$"
PADRAO_SENHA = r"^(?=.*[A-Z])(?=.*[!@#$%&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$"
PADRAO_CPF = r"^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"
PADRAO_EMAIL = r"^[A-Za-z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{,65}$"

usuario = metadata.tables.get("usuario")
if usuario is None:
    raise ConnectionError("Tabela 'usuario' não encontrada no banco.")

def adicionar_usuario(cpf, email, nome, senha):
    if not re.match(PADRAO_NOME, nome):
        raise ValueError ("Nome Inválido :\n"
                            "-Deve conter apenas letras e espaço, sem acentuação \n"
                            "-Deve conter entre 2 à 20 caracteres.")
    if not re.match(PADRAO_EMAIL, email):
        raise ValueError("Email Inválido :\n" \
                            "- Deve conter padrao email : parte-local@dominio \n"
                            "- parte-local pode conter letras, numeros, hifen (-) e ponto (.) \n" \
                            "- dominio pode conter letras, numeros e hifen (-) separados por ponto (.) \n" \
                            "- Deve conter no máximo 64 caracteres. ")
    if not re.match(PADRAO_SENHA, senha):
        raise ValueError ("Senha Inválida :\n"
                            "- Deve conter pelo menos 1 letra Maiúscula, 1 letra Minúscula, 1 numérico e 1 caractere especial \n"
                            "- Deve conter entre 8 à 15 caracteres.")
    if not re.match(PADRAO_CPF, cpf):
        raise ValueError ("CPF Inválido : \n"
                            "- Deve conter apenas números. \n" 
                            "- Formato desejado : XXX.XXX.XXX-XX \n")
    
    # ... (validação de CPF e Senha) ...
    stmt = insert(usuario).values(cpf=cpf, email=email, nome=nome, senha=senha)
        
    with engine.begin() as conn:
        conn.execute(stmt)

#busca o usuario pelo cpf ou busca todos se não passar parametro
def listar_usuarios(cpf=None):

    stmt = select(usuario)
    if cpf:
        stmt = stmt.where(usuario.c.cpf == cpf)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        usuarios = [dict(row) for row in result.mappings()] 
    
    if cpf and not usuarios:
        raise LookupError("Usuario não encontrado") #404
    return usuarios

def atualizar_usuario(cpf, novo_email=None, nova_senha=None):
    novos_valores = {}

    if novo_email:
        if not re.match(PADRAO_EMAIL, novo_email):
            raise ValueError("Email Inválido :\n" \
                            "- Deve conter padrao email : parte-local@dominio \n"
                            "- parte-local pode conter letras, numeros, hifen (-) e ponto (.) \n" \
                            "- dominio pode conter letras, numeros e hifen (-) separados por ponto (.) \n" \
                            "- Deve conter no máximo 64 caracteres. ")
        novos_valores["email"] = novo_email
    
    if nova_senha:
        if not re.match(PADRAO_SENHA, nova_senha):
            raise ValueError ("Senha Inválida :\n"
                            "- Deve conter pelo menos 1 letra Maiúscula, 1 letra Minúscula, 1 numérico e 1 caractere especial \n"
                            "- Deve conter entre 8 à 15 caracteres.")
        novos_valores["senha"] = nova_senha

    if not novos_valores:
        raise ValueError("Nenhum campo fornecido para atualização.")

    stmt = (
        update(usuario)
        .where(usuario.c.cpf == cpf) #usuario.c.cpf é o mesmo que usuario.columns.cpf (serve para pegar a coluna de cpf)
        .values(**novos_valores)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise LookupError("Nenhum usuário encontrado com esse CPF.")
        print(f"Usuário com CPF {cpf} atualizado com sucesso!")

def deletar_usuario(cpf):
    stmt = delete(usuario).where(usuario.c.cpf == cpf)

    with engine.begin() as conn:
        result = conn.execute(stmt)
        if result.rowcount == 0:
            raise LookupError("Nenhum usuário encontrado com esse CPF.")
    print(f"Usuário com CPF {cpf} removido com sucesso!")
