class HotelEntidade:
    def __init__(self, nome: str, estrelas: float, diaria: float, cidade: str, estado: str, site_id :int):
        self.__nome = nome
        self.__estrelas = estrelas
        self.__diaria = diaria
        self.__cidade = cidade
        self.__estado = estado
        self.__site_id = site_id

    @property
    def site_id(self):
        return self.__site_id

    @site_id.setter
    def site_id(self, site_id):
        self.__site_id == site_id

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        self.__estado = estado

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def estrelas(self):
        return self.__estrelas

    @estrelas.setter
    def estrelas(self, estrelas):
        self.__estrelas = estrelas

    @property
    def diaria(self):
        return self.__diaria

    @diaria.setter
    def diaria(self, diaria):
        self.__diaria = diaria

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade
