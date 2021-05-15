class SiteEntidade:
    def __init__(self, url):
        self.__url = url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url
