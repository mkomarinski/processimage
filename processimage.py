#!/usr/bin/python
import logging
import os
import subprocess

import inotify.adapters

extensions=['.jpg','.JPG','.tif','.TIF','.tiff','.TIFF']

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

input_directory=b'/photos/eye-fi'
output_directory='/documents'
lang='eng'

def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)

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
                  # part of a todo.  Make the file immutable so it can't be easily deleted?
                  #subprocess.call("chattr +i {}.pdf".format(outfile))

# I should really make this a daemon.
if __name__ == '__main__':
    _configure_logging()
    _main()
