import ConnectionManager
import NodoManager
from NodoManager import Nodo, NodoAmico, GlobalNodoLocale
import SafeBinManager
from SafeBinManager import SafeBin, GlobalSafeBin, BackupElem
import DirectoryManager
from DirectoryManager import Directory, Ridondanza
from DifferenzeManager import Differenza


SafeBinManager.GlobalSafeBin = SafeBinManager.getSafeBinFromConfig()
# NodoClass.GlobalNodoLocale = NodoClass.getNodoFromConfig()

# TODO: se nodo locale non "esiste" va creato, se in qualsiasi momento qualquadra non cosa il programma si DEVE bloccare
#   magari un thread a parte?

"""Lista funzioni disponibili nel programma ___________________________________________________________________ """

"""FUNZIONI RELATIVE AL NODO e INFO GENERICHE _________________________________________________________________ """


def getNomeNodoLocale() -> str:
    return GlobalNodoLocale.getNickname()


def editNomeNodo(nome: str) -> bool:
    return GlobalNodoLocale.cambiaNickname(nome=nome)


def getIPAttuale() -> str:
    return ConnectionManager.getLocalIP()


"""FUNZIONI RELATIVE A OGGETTI DIR ____________________________________________________________________________ """


def getListaDir():
    return GlobalNodoLocale.getListaDir()


def aggiungiDirAlNodo(path: str) -> bool:
    pass  # todo


def visualizzaDirNodo():
    pass  # todo


def rimuoviDirDalNodo() -> bool:
    # in input dovrebbe bastare il percorso
    pass  # todo


def ricercaUpdateDirSingola(dirobj: Directory):
    # tramite connection manager si invia un messaggio per richiedere la config di una specifica DIR
    # per ogni elemento (anche in base alla data) si va a proporre un'azione DEL or COPY.
    # Questa funzione deve ritornare una lista, un dict o quel che è per rappresentare tutte le info. FINE
    # poi? Dalla view, tramite Smistatore vengono recuperati i files
    # BUGIA! il main è il controller, la view invece è variabile, il main avvia la view
    pass  # todo


def ricercaUpdateNodo() -> bool:  # todo: split alla versione 2.0
    pass  # Ricorsivamente chiama ricercaUpdateDirSingola su ogni DIR del nodo


def applicaUpdateCompleto(diff: Differenza) -> bool:  # todo: split alla versione 2.0
    pass  # todo


def creaRidondanza():
    pass  # todo


def rimuoviRidondanza():
    pass  # todo


def sincronizzaRidondanza():
    pass  # todo


def inviaAggiornamentoDir(force: bool = False):
    pass  # todo


"""FUNZIONI RELATIVE A NODI AMICI ____________________________________________________________________________ """


def getListaNodiAmici():
    return GlobalNodoLocale.getNodiAmici()


def avviaRicercaNodiAmici() -> list[NodoAmico]:
    """Tramite connection manager "pinga" ogni host per cercare dei nodi. Attende qualche secondo per le risposte.
    Ritorna una lista di nodi trovati. Dalla view sarà possibile scegliere l'oggetto nodo da inserire
    tramite 'aggiungiNodoAmico'."""
    pass  # todo


def aggiungiNodoAmico(nodo: NodoAmico):
    pass  # todo


def aggiungiNodoAmicoViaIP(indirizzo: str) -> bool:
    pass  # todo


def rimuoviNodoAmico(nodo: NodoAmico) -> bool:
    pass  # todo


"""FUNZIONI RELATIVE A SAFE BIN ____________________________________________________________________________ """


def getPercorsoSafeBin():
    return GlobalSafeBin.getPath()


def modificaPercorsoSafeBin(path: str) -> bool:
    return GlobalSafeBin.modificaPercorso(path)


def modificaGiorniScadenza(gg: int):
    return GlobalSafeBin.modificaGiorniScadenza(gg=gg)


def modificaGrandezzaFileMassima(mb: int):
    return GlobalSafeBin.modificaGrandezzaMax(maxbyte=mb)


def getListRidondanze() -> list[Ridondanza]:
    return GlobalNodoLocale.getListaRidondanze()
