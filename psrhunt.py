#!/usr/bin/env python


# Changes :
# 26/10/10 : Major cleanup and modifications for PALFA (now use a mysql database to store the candidates)
# 12/04/09 : Automatic flag RFI
# 10/04/09 : Various modif for mkimposou
# 09/04/09 : Fullscreen window by default
# 18/03/09 : Add automatic backup every 2 min

import gobject, gtk
import os, socket, time



import menus

#if socket.gethostname() in ['gemini', 'clairvaux']:
#  print "Use Gemini Configuration"
#  def_printer="color"
#  INITIALS = "GD"
#  KNOWN_PSR_filename = "psr_catalog.txt"
#  VERBOSE = 0 

KNOWN_PSR_filename = "psr_catalog.txt"

if __name__ == '__main__':
    menus.Manager()
    gtk.main()

