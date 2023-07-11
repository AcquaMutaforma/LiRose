"""
Classe per gestire gli oggetti directory e relative funzioni.
Le info che questa classe contiene servono al main per gestire le varie directory
"""


class Directory:
    def __init__(self, nome: str, path: str, lastUpdate: str = None):
        self.nome = nome
        self.path = path
        self.lastUpdate = lastUpdate
        # todo: metodo verifica informazioni

    def toDict(self) -> dict:
        return {
            'nome': self.nome,
            'path': self.path,
            'lastUpdate': self.lastUpdate
        }

    def getPath(self):
        return self.path
