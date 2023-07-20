from Crypto.PublicKey import RSA

private_key = RSA.generate(2048)
pubkey = private_key.publickey()

private_key = private_key.exportKey().decode("utf-8")
pubkey = pubkey.exportKey().decode("utf-8")

# --------------------

from Crypto.PublicKey import RSA


key = RSA.generate(2048)
f = open('mykey.pem', 'wb')
f.write(key.export_key('PEM'))  # c'e' anche OpenSSH
f.close()

f = open('mykey.pem','r')
key = RSA.import_key(f.read())

# NOTA: Questi sono stati copiati, ora divertiti te :3
