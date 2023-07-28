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

    def verificaEsistenza(self) -> bool:
        return verificaEsistenzaDir(dirname=self.getNome(), percorso=self.getPath())


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
        # todo
        """Penso dovrebbe usare il metodo presente in DirFilesManager che utilizza i file config per fare le differenze
        e valutare l'aggiornamento"""
        pass


def creaDir(nome: str, path: str) -> Directory | None:
    if nome is None or path is None:
        return None
    tmp = Directory(nome=nome, path=path)
    log.debug(f"Creato oggetto Dir: [{tmp.toDict()}]")
    return tmp


def creaRidondanza(nome: str, path: str, parent: str) -> Directory | None:
    if nome is None or path is None or parent is None:
        return None
    tmp = Ridondanza(nome=nome, path=path, parentPath=parent)
    log.debug(f"Creato oggetto Ridondanza: [{tmp.toDict()}]")
    return tmp


def listaDirsToDict(listadir: list[Directory]) -> list[dict]:
    toret: list[dict] = []
    for x in listadir:
        toret.append(x.toDict())
    return toret


def loadDirsFromConfig(listaDir: list[dict]) -> list[Directory]:
    """Metodo che crea una lista di oggetti Dir attraverso i dati della configurazione"""
    if len(listaDir) < 1:
        return []
    toRet: list[Directory] = []
    for x in listaDir:
        if x is None:
            continue
        if x.get('parent') is None:
            tmp = creaDir(nome=x.get('nome'), path=x.get('path'))
            if tmp is None:
                continue
            '''if verificaEsistenzaDir(tmp.getNome(), tmp.getPath()):
                toRet.append(tmp)'''
        else:
            tmp = creaRidondanza(nome=x.get('nome'), path=x.get('path'), parent=x.get('parent'))
            if tmp is None:
                continue
            '''if verificaEsistenzaDir(tmp.getNome(), tmp.getPath()):
                toRet.append(tmp)'''
    return toRet


# Da chiamare quando si vanno a visualizzare/caricare le dirs
def verificaEsistenzaDir(dirname: str, percorso: str) -> bool:
    percorsoCompleto = percorso + '/' + dirname
    esito = os.path.isdir(percorsoCompleto)
    if not esito:
        log.warning(f"La Cartella [{percorsoCompleto}] non e' piu' presente o non si hanno i permessi necessari")
    return esito
