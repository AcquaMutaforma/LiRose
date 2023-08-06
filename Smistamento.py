"""Modulo che gestisce l'applicazione di Aggiornamenti e sincronizzazioni dei files."""
import ConnectionManager
import DifferenzeClass
import NodoClass
from DifferenzeClass import Differenza
import FileManager
from DirFilesManager import Elemento, Dir, File
from DirectoryManager import Directory

# :((( i am so sad, please write me!! Q_Q ç_ç t_t


def creaListaAggiornamenti(dirpath: str, fonteEsterna: str, confEst: list[dict]) -> list[Elemento]:
    diff = DifferenzeClass.confrontaConfigEsterna(dirpath=dirpath, fonteEsterna=fonteEsterna, confEsterna=confEst)
    toret: list[Elemento] = diff.getAggiunti() + diff.getRimossi() + diff.getDifferenti()
    return toret


def applicaAggiornamento(dirpath: str, ipOrPath: str, parentDir: Directory, el: Elemento):
    # provo a vedere se è un IP, sennò sarà un path
    if isinstance(el, File):
        fileDaRichiedere = el.getFilename()
    pass

