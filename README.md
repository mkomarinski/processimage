# processimage
Use inotify to watch for new incoming image files in a specific directory.  If
new files show up, run them through tesseract and turn it into a PDF with
selectable text.  Copy the PDF to two locations (one is Dropbox) and then move
the original image file to an archive location.


Images can come from any source.  I'm using a Doxie Go with an Eye-Fi card.
When the Doxie scans an image, it goes to the Eye-Fi which sends to the
local system and drops it in the specified dirdctory.

# required non-core packages (for now, will change over time)
- inotify (https://pypi.python.org/pypi/inotify)
- configparser
- dropbox

# todo
- Copy original images to glacier?
- Or copy them to a new location and make immutable using chattr
- integrate eyefiserver?
- Upload to dropbox/google drive/onedrive?
  - dropbox integration is easy.  onedrive blows
