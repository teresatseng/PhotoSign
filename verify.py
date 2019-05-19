__author_="Teresa Tseng <teresa.tseng@columbia.edu>"
__date__="$Mar 3, 2019"

from PIL import Image
import piexif, OpenSSL, sys, base64, getpass
import piexif.helper
from OpenSSL import crypto, SSL

def usage():
	print("""
	python verify.py [photo_to_verify.jpeg]
	    Get signature from signer_photo EXIF and verify signature.
	""")

if __name__ == "__main__":
	if len(sys.argv) !=2: # Expect exactly one argument: photo file
		usage()
		sys.exit(2)

	photo = sys.argv[1]

	un = getpass.getuser()

	fc = open(un + ".crt", "r")
	buff = fc.read()
	cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, buff)

	signed_photo = photo.split(".")[0] + "_signed.jpg"
	
	# Open and sign EXIF-stripped file
	try: 
		f =open(photo,'rb')
		
	except IOError:
		raise IOError("Cannot read input file %s\n" %photo)


	exif_dict = piexif.load(signed_photo)

	user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
	sign = base64.b64decode(user_comment)

	if (OpenSSL.crypto.verify(cert, sign, f.read(), "sha256") == None):
		print("Signature verified with " + un + ".crt!")

	fc.close()
	f.close()
	
	
