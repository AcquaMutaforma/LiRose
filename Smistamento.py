"""Modulo che gestisce l'applicazione di Aggiornamenti e sincronizzazioni dei files.
Avvia la sovrascrittura dei files e lo spostamento a safebin

Principalmente si occupa di gestire gli oggetti DIFFERENZA con lo scopo di individuare gli elementi necessari, se servono
si occupa di avviare il recupero dalla fonte esterna"""
import ConnectionManager
import DifferenzeManager
from DifferenzeManager import Differenza
import FileManager
from DirFilesManager import Elemento, Dir, File
from DirectoryManager import Directory

# :((( i am so sad, please write me!! Q_Q ç_ç t_t


def creaListaAggiornamenti(dirpath: str, fonteEsterna: str, confEst: list[dict]) -> Differenza:
    diff = DifferenzeManager.confrontaConfigEsterna(dirpath=dirpath, fonteEsterna=fonteEsterna, confEsterna=confEst)
    return diff


'''def avviaAggiornamento(ipOrPath: str, parentDir: Directory, el: Elemento): 
    """tenta di recuperare il file e di sovrascriverlo"""
    # provo a vedere se è un IP, sennò sarà un path'''


def estraiPercorso(el: Elemento) -> str:
    """Gli elementi forniti dall'oggetto Differenza sono una "MATRIOSCA" di DIR fino ad arrivare ad un FILE, da questi
    va creato il percorso effettivo per procedere"""
    pass


def updateAggiungiFile(el: Elemento, sovrascrivi: bool = False):
    """L'aggiornamento consiste in un elemento in Differenza nella lista "aggiunti" quindi vado a recuperare il file
    per aggiungerlo nella dir."""
    if sovrascrivi:
        FileManager.scriviSuFile()
    else:
        FileManager.creaFile()
    pass


def updateRimuoviFile(el: Elemento):
    """L'aggiornamento consiste in un elemento in Differenza nella lista "rimossi" quindi vado a cancellare il file
        dalla sua dir."""
    pass


def updateAggiornaFile(el: Elemento):
    """L'aggiornamento consiste in un elemento in Differenza nella lista "differenti" quindi vado a recuperare il file
        per sovrascrivelo nella sua dir."""
    # praticamente usi il metodo sopra, " updateAggiungiFile " EASY
    updateAggiungiFile(el=el, sovrascrivi=True)
    pass

