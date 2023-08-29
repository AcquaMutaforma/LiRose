"""Classe che contiene le differenze tra gli oggetti presenti in locale e la configurazione che viene comparata"""
import ConfigManager
import DirFilesManager
from DirFilesManager import Elemento, File, Dir


class Diff:
    def __init__(self):
        self.aggiunti: list[Elemento] = []
        self.rimossi: list[Elemento] = []
        self.differenti: list[Elemento] = []

    def sommaListe(self, agg: list[Elemento] = None, rim: list[Elemento] = None, dif: list[Elemento] = None):
        if agg is not None:
            self.aggiunti += agg
        if rim is not None:
            self.rimossi += rim
        if dif is not None:
            self.differenti += dif


class Differenza:
    def __init__(self, dirpath: str, fonteEsterna: str, diff: Diff = Diff()):
        self.dirLocale = dirpath
        self.fonteEsterna: str = fonteEsterna  # Path o Nome nodo
        if diff is None:
            self.diff = Diff()
        else:
            self.diff = diff

    def getAggiunti(self) -> list[Elemento]:
        return self.diff.aggiunti

    def getRimossi(self) -> list[Elemento]:
        return self.diff.rimossi

    def getDifferenti(self) -> list[Elemento]:
        return self.diff.differenti


def confrontaConfigEsterna(dirpath: str, fonteEsterna: str, confEsterna: list[dict]) -> Differenza | None:
    # Ci si aspetta che la cartella in questione ESISTA, qua non controlla nulla, al massimo un try-except
    if dirpath is None or fonteEsterna is None or confEsterna is None:
        return None
    diff = Diff()
    # Non ricalcolo tutto, prendo la CONFIG dei file dato viene ri-generata all'avvio del software
    listaLocale: list[Elemento] = DirFilesManager.creaListaElementiFromConf(
        configurazione=ConfigManager.leggiConfigFile(dirpath=dirpath))
    listaEsterna: list[Elemento] = DirFilesManager.creaListaElementiFromConf(configurazione=confEsterna)

    tmp = confrontoFiles(loc=listaLocale, est=listaEsterna)
    diff.sommaListe(agg=tmp.aggiunti, rim=tmp.rimossi, dif=tmp.differenti)

    for x in listaLocale:
        if isinstance(x, Dir):
            if x in listaEsterna:
                esterna = listaEsterna.pop(listaEsterna.index(x))
                if isinstance(esterna, Dir):
                    tmpDiff = confrontoContenutoDir(x, esterna)
                    diff.sommaListe(agg=tmpDiff.aggiunti, rim=tmpDiff.rimossi, dif=tmpDiff.differenti)
            else:
                diff.rimossi.append(x)
                listaLocale.remove(x)
    for y in listaEsterna:
        if isinstance(y, Dir):
            diff.aggiunti.append(y)
    return Differenza(dirpath=dirpath, fonteEsterna=fonteEsterna, diff=diff)


def confrontoFiles(loc: list[Elemento], est: list[Elemento]) -> Diff:
    diff = Diff()
    for x in loc:
        if isinstance(x, File):
            if x in est:
                y = est.pop(est.index(x))
                if isinstance(y, File) and x.getHashcode() != y.getHashcode():  # se differenti considero la modifica
                    diff.differenti.append(x)
                    loc.remove(x)
                else:  # senno sono uguali e li rimuovo dalla lista
                    loc.remove(x)
                    est.remove(x)
            else:
                diff.rimossi.append(x)
                loc.remove(x)
    for y in est:  # i files che non sono in locale li considero nuovi
        if isinstance(y, File):
            diff.aggiunti.append(y)
    return diff


def confrontoContenutoDir(locale: Dir, esterno: Dir, sh: Diff = None) -> Diff:
    """Avvia una "ricorsione" a "strascico", ovvero: svolgo i confronti e porto "avanti" gli elementi aggiunti """
    if sh is None:
        shelf = Diff()
    else:
        shelf = sh
    loc = locale.getContenuto()
    dirname = locale.getDirname()
    est = esterno.getContenuto()

    tmp = confrontoFiles(loc, est)
    shelf.sommaListe(agg=Dir(dirname, tmp.aggiunti).getContenuto(),
                     rim=Dir(dirname, tmp.rimossi).getContenuto(),
                     dif=Dir(dirname, tmp.differenti).getContenuto())

    for x in loc:
        if isinstance(x, Dir):
            if x in est:
                confrontoContenutoDir(locale=x, esterno=est.pop(est.index(x)), sh=shelf)
            else:
                a = Dir(dirname)
                a.aggiungiElemento(x)
                shelf.rimossi.append(a)
    for y in est:
        if isinstance(y, Dir):
            a = Dir(dirname)
            a.aggiungiElemento(y)
            shelf.aggiunti.append(a)
    return shelf
