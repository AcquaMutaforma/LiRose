"""
Classe per gestire gli oggetti directory e relative funzioni.
Le info che questa classe contiene servono al main per gestire le varie directory
"""
from Status import Stato


class Directory:
    def __init__(self, nome: str, path: str, lastUpdate: str = None, stato: Stato = None):
        self.nome = nome
        self.path = path
        self.lastUpdate = lastUpdate
        self.stato = stato

    def toDict(self) -> dict:
        return {
            'nome': self.nome,
            'path': self.path,
            'lastUpdate': self.lastUpdate
        }
