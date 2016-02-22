#!/usr/bin/env python

import struct, sys
import datetime
#from ppgplot import *
from math import *
from optparse import OptionParser
from psr_utils import *
import jobtracker
import numpy as np
import psr_utils
import slalib
from pylab import *

KNOWN_PSR_filename = 'psr_catalog.txt'

full_usage = """
TBD
usage : pltasc.py [options] .asc files

  [-h, --help]        : Display this help
  [-r, --rot]         : Rotate the profile


"""
usage = "usage: %prog [options]"


class Pulsar:
    """ Produce a db of known pulsar """
    def __init__(self, idx, psrname, ra_str, dec_str, ra, dec, period, dm, survey):
        self.psrname = psrname
	self.ra_str = ra_str
	self.dec_str = dec_str
	self.ra = float(ra) * np.pi / 180.
	self.dec = float(dec) * np.pi / 180.
	self.period = period
	self.dm = dm
	self.survey = survey

class PSR_list:
    def __init__(self):
	self.psr_list = []

    def __len__(self):
	return len(self.psr_list)

    def load_known_psrs(self):
	"""
	Load the list of known PSRs
	"""

	psrs = np.genfromtxt(KNOWN_PSR_filename, dtype= None)
	for psr in psrs:
	    self.psr_list.append(Pulsar(*psr))
	#print "known_psrs::load_known_psrs> Loaded %d known PSRs"%(len(self.psr_list))	


    #def show_known_psrs(self #cand ra dec):
    def find_known_psrs(self, ra, dec):
	txt = []

	# Convert RA and DEC of the candidate in rad
	#print "known_psrs::show_known_psrs> Cand Positions: ", ra , dec

	for i in range(len(self.psr_list)):
	    if abs(ra - self.psr_list[i].ra) < 0.006 and abs(dec - self.psr_list[i].dec) < 0.006:
		return i

    def show_known_psrs(self, i):
	doc = "%s\n  RA : %s\n  DEC : %s\n  Period : %s\n  DM : %s\n  Survey %s"% \
			(self.psr_list[i].psrname, self.psr_list[i].ra_str, \
			self.psr_list[i].dec_str, self.psr_list[i].period, \
			 self.psr_list[i].dm, self.psr_list[i].survey)
	#txt.append(doc)
	#return "\n\n".join(txt)
	return doc

    def get_psrname(self, i):
	return self.psr_list[i].psrname

    def get_ra(self, i):
	return self.psr_list[i].ra_str

    def get_dec(self, i):
	return self.psr_list[i].dec_str

    def get_period(self, i):
	return self.psr_list[i].period

    def get_DM(self, i):
	return self.psr_list[i].dm

    def get_survey(self, i):
	return self.psr_list[i].survey


def main():
  parser = OptionParser(usage)

  parser.add_option("-d", "--days", type="float", dest="nb_days", default=60.0,
                          help="Minimum number of days for plannified observations (default=60)")

  (opts, args) = parser.parse_args()			
	

  QUERY = "SELECT * FROM Headers AS H LEFT JOIN PDM_Candidates AS C ON \
	H.header_id=C.header_id LEFT JOIN PDM_Classifications AS R ON \
	R.pdm_cand_id=C.pdm_cand_id WHERE R.person_id=2 AND R.rank=6;"  

  results = jobtracker.query(QUERY, db="remote-SPAN512")
  print "Found %d known pulsars in the database"%(len(results)) 

  Known_psrs = PSR_list()
  Known_psrs.load_known_psrs()
  print "Read %d known pulsars from %s"%(len(Known_psrs), KNOWN_PSR_filename)

  psrnames = np.array([]) 
  snr = np.array([])
  sig = np.array([])

  for res in results:
      #print res
      print "SRC = %s  Period = %s  Tint = %s  SNR = %s  Sigma = %s"%(res['source_name'], res['bary_period'], res['observation_time'], res['snr'], res['rescaled_prepfold_sigma'])
      ra_rad, dec_rad = slalib.sla_galeq(res['galactic_longitude'] * np.pi/180., res['galactic_latitude'] * np.pi/180.)

      psr_id = Known_psrs.find_known_psrs(ra_rad, dec_rad)

      if psr_id:
	  print Known_psrs.show_known_psrs(psr_id)
	  print " "

	  snr = np.append(snr, res['snr'])
	  psrnames = np.append(psrnames, Known_psrs.get_psrname(psr_id))

      else:
	  print "None found\n"
 
  plot(snr, 'ro')
  xticks(np.arange(len(psrnames)), psrnames, rotation=90)
  tight_layout(pad=1.2)
  ylabel('SNR')
  show()
  

if __name__ == '__main__':
  main()
