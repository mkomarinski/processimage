# processimage
Use inotify to watch for new incoming image files in a specific directory.  If new files show up, run them through tesseract and turn it into a PDF with selectable text.  Then put the file in a new location, leaving the original image in its current location.

Images can come from any source.  I'm using a Doxie go with an older Eye-Fi card.  When the Doxie scans an image, it goes to the Eye-Fi which sends to the local system and drops it in the specified dirdctory.

# required non-core packages (for now, will change over time)
- inotify (https://pypi.python.org/pypi/inotify)

# todo
- Copy original images to glacier?
- Or copy them to a new location and make immutable using chattr
- Upload to dropbox/google drive/onedrive?
