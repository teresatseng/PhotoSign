__author__="Teresa Tseng <teresa.tseng@columbia.edu>"
__date__="$Mar 3, 2019"

from OpenSSL import crypto, SSL
from socket import gethostname
from time import gmtime, mktime
from os.path import join
import getpass

"""
Generate a key pair and write out to file
"""

un = getpass.getuser()
CERT_FILE = un + ".crt"
KEY_FILE = un + ".key"

# create key pair
k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 1024)

# create self-signed cert
cert = crypto.X509()
cert.get_subject().C = "US"
cert.get_subject().O = un +"'s Company"
cert.get_subject().OU = un + " Incorporated"
cert.get_subject().CN = gethostname()
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(10*365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, 'sha1')

publicraw = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
f = open(CERT_FILE, "wb")
f.write(publicraw)

privateraw = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
f = open(KEY_FILE, "wb")
f.write(privateraw)

f.close()

