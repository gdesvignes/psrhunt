#!/usr/bin/env python

import struct, sys
import numpy as np 
import datetime
#from ppgplot import *
from math import *
from optparse import OptionParser
from database import *
from psr_utils import *


full_usage = """
TBD
usage : pltasc.py [options] .asc files

  [-h, --help]        : Display this help
  [-r, --rot]         : Rotate the profile


"""
usage = "usage: %prog [options]"


def main():
  parser = OptionParser(usage)

  parser.add_option("-d", "--days", type="float", dest="nb_days", default=60.0,
                          help="Minimum number of days for plannified observations (default=60)")

  (opts, args) = parser.parse_args()			
	
  # Scan files
  db = Database(db="local-SPAN512-CC")
  DBconn = db.conn
  DBcursor = db.cursor

  a = datetime.datetime.now()

  #QUERY = "SELECT DISTINCT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period, C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, NULL, P.filename, N.rank, R.value FROM PDM_Candidates AS C LEFT JOIN Headers AS H ON H.header_id = C.header_id             LEFT JOIN PDM_Candidate_plots AS P ON C.pdm_cand_id = P.pdm_cand_id LEFT JOIN PDM_Classifications AS N ON C.pdm_cand_id = N.pdm_cand_id LEFT JOIN auth_user AS U ON N.person_id=U.person_id LEFT JOIN pdm_rating AS R ON C.pdm_cand_id=R.pdm_cand_id"

  #QUERY = "SELECT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period, C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, NULL, P.filename, N.rank FROM PDM_Candidates AS C LEFT JOIN Headers AS H USING(header_id) LEFT JOIN PDM_Candidate_plots AS P USING(pdm_cand_id) LEFT JOIN PDM_Classifications AS N USING(pdm_cand_id) RIGHT JOIN auth_user AS U USING(person_id) WHERE U.pdm_rating_instance_id=19"
  QUERY = "SELECT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period, C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, NULL, NULL, N.rank, R1.value FROM PDM_Candidates AS C LEFT JOIN Headers AS H USING(header_id) LEFT JOIN PDM_Classifications AS N ON C.pdm_cand_id=N.pdm_cand_id AND N.person_id=2 LEFT JOIN pdm_rating AS R1 ON C.pdm_cand_id=R1.pdm_cand_id AND R1.pdm_rating_instance_id=19"
  #QUERY = "SELECT DISTINCT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period, C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, NULL, N.rank, R1.value FROM PDM_Candidates AS C LEFT JOIN Headers AS H USING(header_id) LEFT JOIN PDM_Classifications AS N USING(pdm_cand_id) LEFT JOIN auth_user AS U USING(person_id) LEFT JOIN pdm_rating AS R1 ON C.pdm_cand_id=R1.pdm_cand_id AND R1.pdm_rating_instance_id=19 AND U.username='desvignes'"

  #QUERY = "SELECT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period, C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, P.filename FROM PDM_Candidates AS C LEFT JOIN Headers AS H ON H.header_id = C.header_id             LEFT JOIN PDM_Candidate_plots AS P ON C.pdm_cand_id = P.pdm_cand_id"
  DBcursor.execute(QUERY)
  result_query = [list(row) for row in DBcursor.fetchall()]
  print len(result_query)
  print result_query[0]

  b = datetime.datetime.now()
  c = b - a
  print c

  
  DBconn.close()

if __name__ == '__main__':
  main()
