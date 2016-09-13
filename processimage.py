#!/usr/bin/python
import logging
import os
import shutil
import subprocess
import dropbox

import inotify.adapters

extensions=['.jpg','.JPG','.tif','.TIF','.tiff','.TIFF']

# ecch.  This stuff needs to be in a config file.
input_directory=b'/photos/eye-fi'
output_directory='/documents/'
archive_directory='/photos/archive'
dropbox_key='h9vmhucztbd7178'
dropbox_secret='phchee9h235s6m0'
lang='eng'

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)

def _dropbox_login():
    # Connect to Dropbox.  If a new token is needed, tell the user, otherwise
    #  the one we have should be sufficient.

    # Where are we keeping the token?
    # WARNING: this token will give someone unlimited access to your dropbox
    #  account.  Be safe!
    TOKENS = 'dropbox_token.txt'

    # If the token file doesn't exist, that's fine, ask the user to go to
    #  the dropbox site and get a key to then retrieve a token.
    if not os.path.isfile('dropbox_token.txt'):
      auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(dropbox_key,dropbox_secret)

      authorize_url = auth_flow.start()

      print "1. Go to: " + authorize_url
      print "2. Click \"Allow\" (you might have to log in first)."
      print "3. Copy the authorization code."

      auth_code = raw_input("Enter the authorization code here: ").strip()
      try:
        access_token, user_id = auth_flow.finish(auth_code)
      except Exception, e:
        print('Error: %s' % (e,))
        return

      token_file = open(TOKENS,'w')
      print(access_token)
      token_file.write("%s" % (access_token) )
      token_file.close()
    else:
      # If the token file already exists, then we'll need to assume that
      #  it has a valid token in it.  Use that.
      token_file = open(TOKENS)
      access_token = token_file.read()
      token_file.close()
    return access_token

def upload_file(access_token, file_from, file_to):
      """upload a file to Dropbox using API v2
      """
      dbx = dropbox.Dropbox(access_token)

      with open(file_from, 'rb') as f:
          dbx.files_upload(f, file_to)


def _main():
    i = inotify.adapters.InotifyTree(input_directory)

    for event in i.event_gen():
            # Did we get an actual event, or just a timeout?
            if event is not None:
                # pull out data from this event
                (header, type_names, watch_path, filename) = event
                # figure out the extension of the file
                (basename,extension) = os.path.splitext(filename.decode('utf-8'))
                # If this is a new file that was written (or appeded to) and the file was closed and the file
                # extension matches that of one of the known image extensions...
                if type_names[0] == "IN_CLOSE_WRITE" and extension in extensions:
                  # need to log this elsewhere...for later
                  _LOGGER.info("New file {}".format(filename.decode('utf-8')))
                  # build up where the input file is
                  infile=os.path.join(watch_path.decode('utf-8'), filename.decode('utf-8'))
                  # figure out where the file is going to but no extension
                  outfile=os.path.join(output_directory, basename)
                  # call tesseract which will append the extension to the end of the output file name
                  # for a personal reason I'm including the umask of 0002
                  subprocess.call("umask 002; /usr/bin/tesseract -psm 1 -l {} {} {} pdf".format(lang,infile,outfile),shell=True)
                  # upload the resulting file to dropbox
                  upload_source = outfile + ".pdf"
                  upload_target = os.path.join('/scans',basename + ".pdf")
                  upload_file(access_token,upload_source,upload_target)
                  # Move the original to its final archive location
                  shutil.move(infile, archive_directory)

# I should really make this a daemon.
if __name__ == '__main__':
    _configure_logging()
    access_token=_dropbox_login()
    _main()
