"""Classe che contiene le differenze tra gli oggetti presenti in locale e la configurazione che viene comparata"""
import DirFilesManager
from DirFilesManager import Elemento
import Nodo


class Diff:
    def __init__(self, dirpath: str, fonteEsterna: str | Nodo.Nodo):
        self.dirLocale = dirpath
        self.fonteEsterna: str | Nodo.Nodo = fonteEsterna  # Path o Nome nodo

        self.aggiunti: list[Elemento] = []
        self.rimossi: list[Elemento] = []
        self.differenti: list[Elemento] = []
        self.spostati: list[Elemento] = []


def __creaDiff(dirpath: str, fonteEsterna: str | Nodo.Nodo) -> Diff:
    return Diff(dirpath=dirpath, fonteEsterna=fonteEsterna)


def confrontaConfigEsterna(dirpath: str, fonteEsterna: str | Nodo.Nodo, confEsterna: list[dict]) -> Diff | None:
    # Ci si aspetta che la cartella in questione ESISTA, qua non controlla nulla, al massimo un try-except
    if dirpath is None or fonteEsterna is None:
        return None
    toret = __creaDiff(dirpath=dirpath, fonteEsterna=fonteEsterna)
    # NOPE! Non ricalcolare tutto, prendi la CONFIG dei file, viene rigenerata all'avvio del software
    listaLocale = DirFilesManager.getListaElementiLocali(dirpath=dirpath)
    listaEsterna = DirFilesManager.creaListaElementiFromConf(configurazione=confEsterna)

    """
    Cerco uguali, valuto hash, aggiungo in "differenti" o li elimino dalla lista (cosi e' piu' leggera)
    Se non trovo li aggiungo in "rimossi"
    I rimanenti li aggiungo in "aggiunti"
    """

    return toret
    # NOTA: nella valutazione, se l'hash è uguale, skippo


