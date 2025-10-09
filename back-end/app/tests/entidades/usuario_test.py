from app.models import Usuario
import unittest

class TUUsuario(unittest.TestCase):
    NOME_VALIDO = "Joao Alvares"
    CPF_VALIDO = "123.456.789-00"
    EMAIL_VALIDO = "joao.alvares@yahoo.com.br"
    SENHA_VALIDA = "$JoaoAlvares123"

    def setUp(self):
        self.entidade = Usuario(self.NOME_VALIDO,self.EMAIL_VALIDO, self.CPF_VALIDO, self.SENHA_VALIDA)
        self.estado = 1
    
    def test_valido(self):
        self.assertEqual(self.entidade.nome, self.NOME_VALIDO, "Teste inválido -> Nome")
        self.assertEqual(self.entidade.cpf, self.CPF_VALIDO, "Teste inválido -> CPF")
        self.assertEqual(self.entidade.email, self.EMAIL_VALIDO, "Teste inválido -> Email")
        self.assertEqual(self.entidade.senha, self.SENHA_VALIDA, "Teste inválido -> Senha")


if __name__ == "__main__":
    unittest.main()