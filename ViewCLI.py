from NodoManager import Nodo, NodoAmico
from SafeBinManager import SafeBin
from DifferenzeManager import Differenza
import Controller


def getComando():
    print("richiesta > ")
    com = input()
    match com:
        case 'exit':
            printExit()
        case 'help':
            printHelp()
        case 'home':
            printIndex()


def pListaAggiornamentiDir(agg: Differenza):
    """Devo creare un dizionario o una lista per distinguere se gli elementi sono da aggiungere o rimuovere, inoltre è
    necessario "identificarli" con un numero da far inserire nella view. Alle GUI non serve, quindi questo meccanismo
    va scritto qua :( """
    listaOggetti = ''
    loopAggiornamento(listaOggetti)  # todo: definire il tipo di lista o dict
    pass


def loopAggiornamento(oggetti):  # todo: definire il tipo di lista o dict
    """Una volta stampata la lista degli aggiornamenti possibili, si puo inserire un numero o una lista di numeri
    che identificano gli elementi da "aggiornare". Per renderlo più modulare utilizzo questo loop che aspetta gli ID
    degli Elemento da aggiornare o una parola di uscita (ext o ENTER forse). Essendo legato alla CLI deve essere
    sviluppato solo in questo modulo."""
    pass


def printDir(x):
    pass


def printNodiAmici():
    pass


def printIndex():
    # La view deve inserire i dati di ogni DIR e chiamare una "verificaEsistenza" per poi inserire il relativo "stato"
    print("\n")
    print("-- info nodo locale --")
    print("Nickname : " + Controller.getNomeNodoLocale())
    print("IP attuale : " + Controller.getIPAttuale())
    print("SafeBin : " + Controller.getPercorsoSafeBin())
    print("---------------------")
    for x in Controller.getListaDir():
        printDir(x)
    for y in Controller.getListRidondanze():
        printDir(y)
    printNodiAmici()


def printStart():
    print("\n")
    print(
        "  _            _____                       \n"
        " | |      (_) |  __ \                      \n"
        " | |       _  | |__) |   ___    ___    ___ \n"
        " | |      | | |  _  /   /   \  / __|  / _ \\\n"
        " | |____  | | | | \ \  | (_) | \__ \ |  __/\n"
        " |______| |_| |_|  \_\  \___/  |___/  \___|\n"
        "                         By Acqua Mutaforma\n\n")
    print("Rose Jenkins >> Bentornato nella mia biblioteca!\nSe ti serve aiuto scrivi \" help \" ;)")


def printExit():
    print("\nRose Jenkins >> Spero di esserti stata utile ^-^ Ciaoo !")
    exit(0)


def avviaView():
    printStart()
    printIndex()
    try:
        while 1:
            getComando()
    except KeyboardInterrupt:
        printExit()


def printHelp():
    pass
