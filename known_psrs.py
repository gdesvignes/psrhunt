import gtk
import numpy

import psrhunt
import psr_utils
import psr_constants

class Pulsar:
    """ Produce a db of known pulsar """
    def __init__(self, idx, psrname, ra_str, dec_str, ra, dec, period, dm, survey):
        self.psrname = psrname
	self.ra_str = ra_str
	self.dec_str = dec_str
	self.ra = float(ra) * psr_constants.DEGTORAD
	self.dec = float(dec) * psr_constants.DEGTORAD
	try:
	    self.period = float(period) * 1000. # transform period in ms
	except:
	    self.period = 0.
	self.dm = dm
	self.survey = survey

class PSR_list:
    def __init__(self):
	self.psr_list = []

    def load_known_psrs(self):
	"""
	Load the list of known PSRs
	"""

	psrs = numpy.genfromtxt(psrhunt.KNOWN_PSR_filename, dtype= None)
	for psr in psrs:
	    self.psr_list.append(Pulsar(*psr))
	print "known_psrs::load_known_psrs> Loaded %d known PSRs"%(len(self.psr_list))	


    #def show_known_psrs(self #cand ra dec):
    def show_known_psrs(self, cand):
	txt = []

	# Convert RA and DEC of the candidate in rad
	print "known_psrs::show_known_psrs> Cand Positions: ", cand.ra , cand.dec
	cand_RA = psr_utils.ra_to_rad(cand.ra) 
	cand_DEC = psr_utils.dec_to_rad(cand.dec) 

	for i in range(len(self.psr_list)):
	    #print "cand RA = %s   psr RA = %s"%(cand.ra, self.psr_list[i].ra)
	    if abs(cand_RA - self.psr_list[i].ra) < 0.006 and abs(cand_DEC - self.psr_list[i].dec) < 0.006:
		doc = "%s\n  RA : %s\n  DEC : %s\n  Period : %s\n  Ratio : %.4f\n  DM : %s\n  Survey %s"% \
			(self.psr_list[i].psrname, self.psr_list[i].ra_str, \
			self.psr_list[i].dec_str, self.psr_list[i].period, \
			float(self.psr_list[i].period)/ cand.period, \
			 self.psr_list[i].dm, self.psr_list[i].survey)
		txt.append(doc)

	txt = "\n\n".join(txt)

	# create a new scrolled window.
	scrolled_window = gtk.ScrolledWindow()
	scrolled_window.set_border_width(10)
	scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

	if txt:
	    label = gtk.Label(txt)
	    scrolled_window.add_with_viewport(label)

	return scrolled_window    

