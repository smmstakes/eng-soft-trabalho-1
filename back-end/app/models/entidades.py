import re

class Usuario :

    PADRAO_NOME = r"^[a-zA-Z\s]{2,20}$"
    PADRAO_SENHA = r"^(?=.*[A-Z])(?=.*[!@#$%&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$"
    PADRAO_CPF = r"^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"
    PADRAO_EMAIL = r"^[A-Za-z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{,65}$"

    def __init__ (self, nome, email, cpf, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
     
    @property
    def nome(self): 
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome): 
        if not (re.match(Usuario.PADRAO_NOME, novo_nome)):
            raise ValueError ("Nome Inválido :\n"
                              "-Deve conter apenas letras e espaço, sem acentuação \n"
                              "-Deve conter entre 2 à 20 caracteres.")   
        self._nome=novo_nome

    @property
    def senha(self): 
        return self._senha
    
    @senha.setter
    def senha(self, nova_senha):
        if not(re.match(Usuario.PADRAO_SENHA, nova_senha)):
            raise ValueError ("Senha Inválida :\n"
                              "- Deve conter pelo menos 1 letra Maiúscula, 1 letra Minúscula, 1 numérico e 1 caractere especial \n"
                              "- Deve conter entre 8 à 15 caracteres.")
        self._senha=nova_senha

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, novo_cpf):
        if not(re.match(Usuario.PADRAO_CPF, novo_cpf)):
            raise ValueError ("CPF Inválido : \n"
                              "- Deve conter apenas números. \n" 
                              "- Formato desejado : XXX.XXX.XXX-XX \n")
        self._cpf = novo_cpf

    @property
    def email(self): 
        return self._email
    
    @email.setter
    def email(self, novo_email):
        if not(re.match(Usuario.PADRAO_EMAIL, novo_email)):
            raise ValueError("Email Inválido :\n" \
                             "- Deve conter padrao email : parte-local@dominio \n"
                             "- parte-local pode conter letras, numeros, hifen (-) e ponto (.) \n" \
                             "- dominio pode conter letras, numeros e hifen (-) separados por ponto (.) \n" \
                             "- Deve conter no máximo 64 caracteres. ")
        self._email=novo_email

    def to_dict(self):
        return {
            'nome': self._nome,
            'cpf' : self.cpf,
            'email': self._email,
            'senha': self._senha
        }

    def __repr__(self):
        return f'<Usuario: {self._nome}, Email : {self._email}>'

