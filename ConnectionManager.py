'''
 socket.inet_aton(ip_string)

Convert an IPv4 address from dotted-quad string format (for example, ‘123.45.67.89’) to 32-bit packed binary format,
as a bytes object four characters in length.

 socket.inet_ntoa(packed_ip)
Convert a 32-bit packed IPv4 address (a bytes-like object four bytes in length) to its standard dotted-quad string
representation (for example, ‘123.45.67.89’).
'''
import LogManager
import Autenticator
import socket
import asyncio
import json

log = LogManager.setName(__name__)
clients = {}

server_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
server_status = False

carattere_fine_messaggio = b'LR_0x3f'


class Messaggio:
    def __init__(self, codice: int, addrSocket: tuple, dati_request: str, id_procedura: int):
        self.address = addrSocket
        self.codice = codice
        self.richiesta = dati_request
        self.procedura = id_procedura
        # todo: aggiungere chiave per la firma? boh forse basta Cryptare e ggwp
        # Il formato sarà sempre JSON, l'header avrà dei caratteri "iniziali" e "finali" cosi ignoro totalmente la
        #   grandezza dell'header. Vado ad utilizzare il buffer del socket come un array STR

    def messToStr(self) -> str:
        toret: dict = {
            'host': str(self.address[0]),
            'port': str(self.address[1]),  # todo CHECK se sia corretto
            'code': self.codice,
            'request': self.richiesta,
            'procedura': self.procedura
        }
        return json.dumps(toret)


def dictToMessaggio(mess: dict) -> Messaggio | None:
    host = mess.get('host')
    porta = mess.get('port')
    cod = mess.get('code')
    req = mess.get('request')
    id_proc = mess.get('procedura')
    if host is None or porta is None or cod is None or req is None or id_proc is None:
        return None
    else:
        return Messaggio(codice=cod, addrSocket=(host,porta), dati_request=req, id_procedura=id_proc)


def stringToIP(indirizzo: str) -> bytes | None:  # todo: era una bozza, anche il return type è sbagliato
    try:
        return socket.inet_aton(indirizzo)
    except OSError as e:
        log.debug(f"Errore trasformazione STR -> IP addr - {e}")
    return None


def IPToString(indirizzo: socket.socket) -> str:
    pass


# TODO : Questo utilizza {Autenticator.py} per verificare i nodi prima di parlarci !!!

# todo: la componente server deve utilizzare smistamento per applicare gli aggiornamenti avviati da esterno

def getBannerFromNodo(indirizzo):
    """Per verificare che sia effettivamente lui"""
    return None


def inviaMessaggio():
    pass


def creaMessErrore(codice: int) -> str:
    """Crea un Messaggio da inviare e :return: la sua versione STR """
    # piu in basso ho "get local ip", non so se mi serve per creare un messaggio qua
    pass


def doIKnowHim():
    """chiedo a esecutore se X è nella lista dei nodi amici"""
    pass


def getLocalIP() -> str:
    # todo
    return ''


def elabora_connessione(inputStream, outputStream):
    task = asyncio.Task(handle_client(inputStream, outputStream))
    clients[task] = (inputStream, outputStream)

    def client_done(taskk):
        del clients[taskk]
        outputStream.close()
        log.debug("End Connection")

    log.debug("New Connection")
    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(client_reader: asyncio.StreamReader, client_writer):
    # connessione stabilita -> invio conferma
    timeoutConnessione = 6.0
    client_writer.write("RDY\n".encode())
    # attesa risposta per "timeoutConnessione" secondi
    data = yield from asyncio.wait_for(client_reader.readuntil(carattere_fine_messaggio), timeout=timeoutConnessione)
    # silenzio radio
    if data is None:
        log.debug(f"Non ho ricevuto messaggi in {timeoutConnessione} sec dopo l'handshake")
        return

    recived_data = json.loads(data.decode())
    log.warning(f"Messaggio in input = [{data}]")
    if isinstance(recived_data, dict):
        # messaggio valido -> risposta
        client_writer.write(eseguiRichiesta(recived_data).encode())
    else:
        # messaggio NON valido -> risposta
        client_writer.write(creaMessErrore(codice=2).encode())
        log.warning(f"Messaggio in input NON elaborato [{data}] not DICT")


def start_server():
    global server_loop, server_status
    server_loop = asyncio.get_event_loop()
    server_status = True
    f = asyncio.start_server(elabora_connessione, host=None, port=2991)
    server_loop.run_until_complete(f)
    server_loop.run_forever()


def stop_server():
    global server_loop, server_status
    server_loop.stop()
    # todo: controllare se il while sia corretto. Stop gli dice di smettere e close lo uccide
    while not server_loop.is_running():
        server_loop.close()
        server_status = False


def getStatoServer() -> bool:
    """True = online, False = offline"""
    return server_status


def eseguiRichiesta(mess: dict) -> str:
    """Crea un oggetto Messaggio dall'input, prova ad eseguire il comando e
    :return: un MESSAGGIO con l'esito dell'operazione, sotto forma di STR.
    1) verifica che il messaggio sia stato inviato da un nodo amico
    2) controllo se sono presenti tutti i campi e se sono validi
    3) in base al codice valuto la richiesta (non posso mandare files estranei all'applicazione :c )
    4) tento di eseguire la richiesta
    5) creo un messaggio con l'esito e lo ritorno
    """
    messaggio = dictToMessaggio(mess)
    if messaggio is None:
        return ''  # errore
    match messaggio.codice:
        case 0:
            return ''
        case 1:
            return '2'
        case _:
            return 'default'

