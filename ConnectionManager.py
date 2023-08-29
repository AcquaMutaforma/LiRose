# TODO : Questo utilizza {Autenticator.py} per verificare i nodi prima di parlarci !!!

'''
 socket.inet_aton(ip_string)

Convert an IPv4 address from dotted-quad string format (for example, ‘123.45.67.89’) to 32-bit packed binary format,
as a bytes object four characters in length.

 socket.inet_ntoa(packed_ip)
Convert a 32-bit packed IPv4 address (a bytes-like object four bytes in length) to its standard dotted-quad string
representation (for example, ‘123.45.67.89’).
'''
import LogManager
import socket
import Autenticator

__inputPort = 31411
__outputPort = 31410
log = LogManager.setName(__name__)


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
