"""Questo modulo rappresenta e gestisce le directory, ovvero le cartelle locali che vengono considerate dal nodo per
la sincronizzazione di files e backup"""
import os
import LogManager

log = LogManager.setName(__name__)


class Directory:
    def __init__(self, nome: str, path: str):
        self.__nome = nome
        self.__path = path
        # NOTA: La lista di File/Dir non la tengo in runtime, potrebbe essere pesante. L'aggiornamento lo faccio manuale
        # quindi quando è necessario si carica il tutto, si controllano le differenze, si effettuano cambi e si svuota
        # la memoria

    def toDict(self) -> dict:
        return {
            'nome': self.getNome(),
            'path': self.getPath()
        }

    def getPath(self):
        return self.__path

    def getNome(self):
        return self.__nome


class Ridondanza(Directory):
    def __init__(self, nome: str, path: str, parentPath: str):
        super().__init__(nome, path)
        self.__parent = parentPath

    def getParent(self):
        return self.__parent

    def toDict(self) -> dict:
        return {
            'nome': self.getNome(),
            'path': self.getPath(),
            'parent': self.getParent()
        }

    def diventaDir(self):
        return Directory(self.getNome(), self.getPath())

    def checkSincronizzazione(self) -> bool:
        """Penso dovrebbe usare il metodo presente in DirFilesManager che utilizza i file config per fare le differenze
        e valutare l'aggiornamento"""
        pass


def creaDir(nome: str, path: str) -> Directory | None:
    if nome is None or path is None:
        return None
    if verificaEsistenzaDir(path):
        tmp = Directory(nome=nome, path=path)
        log.debug(f"Creato oggetto Dir: {tmp.toDict()}")
        return tmp
    else:
        return None


def creaRidondanza(nome: str, path: str, parent: str) -> Directory | None:
    if nome is None or path is None or parent is None:
        return None
    if verificaEsistenzaDir(path):
        tmp = Ridondanza(nome=nome, path=path, parentPath=parent)
        log.debug(f"Creato oggetto Ridondanza: {tmp.toDict()}")
        return tmp
    else:
        return None


def loadDirList(listaDir: dict) -> list[Directory]:
    if len(listaDir) < 1:
        return []
    toRet: list[Directory] = []
    for x in listaDir:
        if x is None:
            continue
        if x.parent is None:
            tmp = creaDir(nome=x.nome, path=x.path)
            if tmp is not None:
                toRet.append(tmp)
        else:
            tmp = creaRidondanza(nome=x.nome, path=x.path, parent=x.parent)
            if tmp is not None:
                toRet.append(tmp)


def verificaEsistenzaDir(percorso: str) -> bool:
    return os.path.isdir(percorso)


# todo: delete ??
def getDirnameFromPath(percorso: str) -> str:
    if os.name == 'nt':
        separatore = '\\'
    else:
        separatore = '/'
    return percorso.split(sep=separatore).pop()
