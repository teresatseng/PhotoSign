Teresa Tseng

Steps for running:

1. python keygen.py
	Generates a crt/key pair with some phony data and system username
2. python exifstrip.py [photo.jpg]
	Strips EXIF from photo, creates a duplicate, and inserts signature of original into the duplicate.

3. python verify.py [photo.jpg]
	Reads signature from duplicate photo, verifies user signature and outputs success message upon verification.
