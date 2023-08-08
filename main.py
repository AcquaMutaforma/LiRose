# Ara ara
import DifferenzeManager
import FileManager
from DirectoryManager import Directory
import NodoClass
import ConfigManager
from DifferenzeManager import Differenza

FileManager.verificaComponentiAvvio()

""" oggetti principali """
nodoLocale = NodoClass.getNodoFromConfig(ConfigManager.leggiConfigNodo())

# TODO: se nodo locale non "esiste" va creato, se in qualsiasi momento qualquadra non cosa il programma si DEVE bloccare

"""Lista funzioni disponibili nel programma ___________________________________________________________________ """

"""FUNZIONI RELATIVE A OGGETTI DIR ____________________________________________________________________________ """


def getListaDir():  # serve alla view
    return nodoLocale.getListaDir()


def aggiungiDirAlNodo(path: str) -> bool:
    pass  # todo


def visualizzaDirNodo():
    pass  # todo


def rimuoviDirDalNodo() -> bool:
    # in input dovrebbe bastare il percorso
    pass  # todo


def ricercaUpdateDirSingola(dirobj: Directory) -> Differenza:
    # effettua la ricerca tramite connection manager, recupera la config, genera gli oggetti e valuta il risultato
    # Se TRUE -> APPLICA MODIFICHE
    pass  # todo


def ricercaUpdateNodo() -> bool:
    pass  # Ricorsivamente chiama ricercaUpdateDirSingola su ogni DIR del nodo


def applicaUpdateCompleto(diff: Differenza) -> bool:
    pass  # todo


def frammentaUpdate():  # modalità per aggiornamento di file singoli
    pass  # todo


def creaRidondanza():
    pass  # todo


def rimuoviRidondanza():
    pass  # todo


def sincronizzaRidondanza():
    pass  # todo


"""FUNZIONI RELATIVE A NODI AMICI ____________________________________________________________________________ """


def getListaNodiAmici():
    return nodoLocale.getNodiAmici()


def avviaRicercaNodiAmici() -> list[NodoClass.NodoAmico]:
    """Tramite connection manager "pinga" ogni host per cercare dei nodi. Attende qualche secondo per le risposte.
    Ritorna una lista di nodi trovati. Dalla view sarà possibile scegliere l'oggetto nodo da inserire 
    tramite 'aggiungiNodoAmico'."""
    pass  # todo


def aggiungiNodoAmico(nodo: NodoClass.NodoAmico):
    pass  # todo


def aggiungiNodoAmicoViaIP(indirizzo: str) -> bool:
    pass  # todo


def rimuoviNodoAmico(nodo: NodoClass.NodoAmico) -> bool:
    pass  # todo


"""FUNZIONI RELATIVE A SAFE BIN ____________________________________________________________________________ """


def modificaPercorsoSafeBin(path: str) -> bool:
    return nodoLocale.modificaSafeBinPath(path)


def modificaGiorniScadenza():
    pass  # todo


def modificaGrandezzaFileMassima():
    pass  # todo

