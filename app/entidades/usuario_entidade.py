class UsuarioEntidade:

    def __init__(self, email, apelido, senha, dt_nascimento, nome, is_active):
        self.__email = email
        self.__apelido = apelido
        self.__senha = senha
        self.__dt_nascimento = dt_nascimento
        self.__nome = nome
        self.__is_active = is_active

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active):
        self.__is_active = is_active

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def apelido(self):
        return self.__apelido

    @apelido.setter
    def apelido(self, apelido):
        self.__apelido = apelido

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        self.__senha = senha

    @property
    def dt_nascimento(self):
        return self.__dt_nascimento

    @dt_nascimento.setter
    def dt_nascimento(self, dt_nascimento):
        self.__dt_nascimento = dt_nascimento
