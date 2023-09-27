# https://stuvel.eu/python-rsa-doc/usage.html
import rsa
import LogManager
import ConnectionManager

log = LogManager.setName(__name__)

# Nota: la chiave va cambiata? se il file key viene eliminato, gli altri nodi non potranno collegarsi, come fare?
#   casomai inserisco un errore durante le comunicazioni, in quel caso va eliminato il nodo e ri-aggiunto

filename_priv_key = 'privateKey.pem'
filename_pub_key = 'publicKey.pem'


def generaNuoveChiavi():
    try:
        pub, priv = rsa.newkeys(nbits=1024, poolsize=2)
        fpub = open('keys/' + filename_pub_key, 'wb')
        fpub.write(pub.save_pkcs1('PEM'))
        fpub.close()
        fpriv = open('keys/' + filename_priv_key, 'wb')
        fpriv.write(priv.save_pkcs1('PEM'))
        fpriv.close()
    except PermissionError as e:
        log.critical(f"Scrittura chiavi RSA fallita - {e}")


def __getChiave(filename: str) -> bytes:
    f = open('keys/' + filename, 'rb')
    data = f.read()
    f.close()
    return data


def caricaChiavePrivata() -> rsa.PrivateKey | None:
    try:
        return rsa.PrivateKey.load_pkcs1(keyfile=__getChiave(filename_priv_key), format='PEM')
    except rsa.pkcs1.CryptoError as e:
        log.error(f"Errore recupero chiave privata - {e}")
        return None
    except PermissionError as e:
        log.error(f"Impossibile accedere a [keys/{filename_priv_key}] - {e}")
    except FileNotFoundError:
        generaNuoveChiavi()
        return caricaChiavePrivata()


def caricaChiavePubblica() -> rsa.key.PublicKey | None:
    try:
        return rsa.PublicKey.load_pkcs1(keyfile=__getChiave(filename_pub_key), format='PEM')
    except rsa.pkcs1.CryptoError as e:
        log.error(f"Errore recupero chiave privata - {e}")
        return None
    except PermissionError as e:
        log.error(f"Impossibile accedere a [keys/{filename_pub_key}] - {e}")
    except FileNotFoundError:
        generaNuoveChiavi()
        return caricaChiavePubblica()


def criptaMsg(testo: str, key: rsa.PrivateKey):
    pass


def decriptaMsg(testo: str, key: rsa.PublicKey):
    pass


def verificaNodoAmico(nome: str, indirizzo) -> bool:
    """Successivamente utilizzera' ConnectionManager per recuperare una chiave e valutare se il nodo è valido.
    In questa versione Beta rimane semplificato, mi limito a confrontare il nome preso da un nodo con IP X """
    a: dict = ConnectionManager.getBannerFromNodo(indirizzo)
    if a is None:
        return False
    return a.get('nickname') == nome
