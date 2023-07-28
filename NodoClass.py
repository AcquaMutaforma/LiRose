"""
Classe Nodo mantiene tutte le info principali del dispositivo
"""
import DirectoryManager
import SafeBinManager
from DirectoryManager import Directory
import LogManager
import ConfigManager

log = LogManager.setName(__name__)


class NodoAmico:
    def __init__(self, nome: str, lastip: str = None):
        self.__nickname = nome
        self.__lastIP = lastip
        log.debug(f"Creato NodoAmico = {self.toDict()}")

    def toDict(self) -> dict:
        return {
            'nickname': self.__nickname,
            'lastIP': self.__lastIP,
        }

    def aggiornaIP(self, ipattuale: str):
        self.__lastIP = ipattuale


class Nodo:
    def __init__(self, nome: str, sbpath: dict = None, dirlist: list[dict] = None, nodi: list[dict] = None):
        self.__nickname = nome
        self.__safeBinPath = SafeBinManager.getSafeBinFromConfig(sbpath)
        self.__directoryList: list[Directory] = DirectoryManager.loadDirsFromConfig(dirlist)  # lista dalla config
        # NOTA: La view deve inserire i dati di ogni DIR e chiamare una "verificaEsistenza"
        self.__nodiAmici: list[NodoAmico] = creaListaNodoAmicoFromConfig(nodi)
        log.debug(f"Creato Nodo = {self.toDict()}")

    def toDict(self) -> dict:
        dirList = []
        for x in self.__directoryList:
            if isinstance(x, Directory):
                dirList.append(x.getPath())
        nodiAmichevoli = []
        for y in self.__nodiAmici:
            nodiAmichevoli.append(y.toDict())
        return {
            'nickname': self.__nickname,
            'safeBinPath': self.__safeBinPath.toDict(),
            'directoryList': dirList,  # lista con obj directory va trasformata in lista come "dirList" con solo i path
            'nodiAmici': nodiAmichevoli
        }

    def aggiungiDirectory(self, nuovadir: Directory) -> bool:
        if nuovadir is not None:
            self.__directoryList.append(nuovadir)
            return ConfigManager.aggiornaConfigNodo(contenuto=self.toDict())
        else:
            log.warning(f"Aggiunta di nuova DIR nella lista nodo fallita, Dir = None")
        return False

    def rimuoviDirectory(self, dirobj: Directory) -> bool:
        self.__directoryList.remove(dirobj)
        if self.__directoryList.count(dirobj):
            return False
        else:
            return ConfigManager.aggiornaConfigNodo(contenuto=self.toDict())

    def aggiungiNodoAmico(self, newnodo: NodoAmico) -> bool:
        if newnodo is not None:
            self.__nodiAmici.append(newnodo)
            return ConfigManager.aggiornaConfigNodo(contenuto=self.toDict())
        else:
            log.warning(f"Aggiunta di nuovo nodo amico nella lista nodo fallita, Nodo = None")
        return False

    def rimuoviNodoAmico(self, nodocattivo: NodoAmico) -> bool:
        self.__nodiAmici.remove(nodocattivo)
        if self.__nodiAmici.count(nodocattivo):
            return False
        else:
            return ConfigManager.aggiornaConfigNodo(contenuto=self.toDict())

    def modificaSafeBinPath(self, newPercorso: str) -> bool:
        return self.__safeBinPath.modificaPercorso(newPercorso)


def creaListaNodoAmicoFromConfig(lista: list[dict]) -> list[NodoAmico]:
    toret: list[NodoAmico] = []
    for x in lista:
        nome = x.get('nickname')
        lastip = x.get('lastIP')
        tmp = NodoAmico(nome, lastip)
        if tmp is not None:
            toret.append(tmp)
    return toret


def getNodoFromConfig(config: dict) -> Nodo | None:
    if config is None:
        return None
    nick = config.get('nickname')
    safeBin = config.get('safeBinPath')
    dirlist = config.get('directoryList')
    nodiAmici = config.get('nodiAmici')
    if nick is None or safeBin is None or dirlist is None or nodiAmici is None:
        return None
    else:
        return Nodo(nome=nick, sbpath=safeBin, dirlist=dirlist, nodi=nodiAmici)