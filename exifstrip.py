__author__ ="Teresa Tseng <teresa.tseng@columbia.edu>"
__date__="$Feb 24, 2019"

from PIL import Image
import piexif, OpenSSL, sys, shutil, getpass, base64
import piexif.helper
from OpenSSL import crypto, SSL

def usage():
	print("""
	python exifstrip.py [photo_to_sign.jpeg]
	    Strip EXIF data from photo and insert photo signature into duplicate img.
	""")

if __name__ == "__main__":
	if len(sys.argv) !=2: # Expect exactly one argument: photo file
		usage()
		sys.exit(2)

	photo = sys.argv[1]

	un = getpass.getuser()

	# Opening and closing a file removes its EXIF tags
	p = Image.open(sys.argv[1])
	p.save(sys.argv[1])

	fpk = open(un + ".key","r")
	buff = fpk.read()
	k = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, buff)
	fpk.close()


	# Open and sign EXIF-stripped file
	try: 
		f = open(photo,'rb')
		sign = OpenSSL.crypto.sign(k,f.read(),"sha256")
		f.close()
	except IOError:
		raise IOError("Cannot read input file %s\n" %photo)

	sign_base64 = base64.b64encode(sign)
	s = sign_base64.decode('ascii')


	exif_dict = piexif.load(photo)

	user_comment = piexif.helper.UserComment.dump(s)


	exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment

	exif_bytes = piexif.dump(exif_dict)

	new_photo = photo.split(".")[0] + "_signed.jpg"
	shutil.copy(photo, new_photo)
	piexif.insert(exif_bytes, new_photo)
	

