# Ara ara

import FileManager
from DirectoryManager import Directory
import NodoClass
import ConfigManager
from DifferenzeClass import Diff

FileManager.verificaComponentiAvvio()

# oggetti principali
nodoLocale = NodoClass.getNodoFromConfig(ConfigManager.leggiConfigNodo())

"""Lista funzioni disponibili nel programma ___________________________________________________________________ """

"""FUNZIONI RELATIVE A OGGETTI DIR ____________________________________________________________________________ """


def aggiungiDirAlNodo(path: str) -> bool:
    pass  # todo


def visualizzaDirNodo():
    pass # todo


def rimuoviDirDalNodo() -> bool:
    # in input dovrebbe bastare il percorso
    pass  # todo


def ricercaUpdateDirSingola(dirobj: Directory) -> Diff:
    # effettua la ricerca tramite connection manager, recupera la config, genera gli oggetti e valuta il risultato
    # Se TRUE -> APPLICA MODIFICHE
    pass  # todo


def applicaUpdate(diff: Diff) -> bool:
    pass  # todo


def ricercaUpdateNodo() -> bool:
    pass  # Ricorsivamente chiama ricercaUpdateDirSingola su ogni DIR del nodo


"""FUNZIONI RELATIVE A NODI AMICI ____________________________________________________________________________ """


def avviaRicercaNodiAmici():
    f"""Tramite connection manager "pinga" ogni host per cercare dei nodi. Attende qualche secondo per le risposte.
    Ritorna una lista di nodi trovati. Dalla view sarà possibile scegliere l'oggetto nodo da inserire 
    tramite {aggiungiNodoAmico()}."""
    pass  # todo


def aggiungiNodoAmico():
    pass  # todo


def aggiungiNodoAmicoViaIP():
    pass  # todo


def rimuoviNodoAmico():
    pass  # todo


"""FUNZIONI RELATIVE A SAFE BIN ____________________________________________________________________________ """


def modificaPercorsoSafeBin(path: str) -> bool:
    return nodoLocale.modificaSafeBinPath(path)
