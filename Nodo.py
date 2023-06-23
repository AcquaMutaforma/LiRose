"""
Classe Nodo mantiene tutte le info principali del dispositivo
"""
import DirectoryManager as dm


class Nodo:
    """Questo viene creato dal main come nuovo nodo o caricato da un file config"""
    def __init__(self, nome: str, idn: int, sbpath: str = "/", dirlist: list = None, nodiconosciuti: list = None):
        self.nome = nome
        self.idNodo = idn
        self.safeBinPath = sbpath
        self.directoryList = dm.loadDirList(dirlist)
        self.nodiAmiciList = nodiconosciuti


    def toDict(self) -> dict:
        pass # la lista con obj directory va trasformata in lista come "dirList" e con solo i pathname delle dirs
