#!/usr/bin/env python

import utils
import psr_utils
import psr_constants
import gtk
#from astropy import units as u
#from astropy.coordinates import SkyCoord


import database
import config

class FourierCand:
    """Candidate """
    def __init__(self, val, cand_type_id):

        self.ra         = val[0]
        self.dec        = val[1]
        self.cand_id    = val[2]
        self.header_id  = val[3]
        self.period     = val[4]
        self.dm         = val[5]
        self.snr        = val[6]
        self.cpow       = val[7]
        self.nhits      = val[8]
        self.nharm      = val[9]
        self.sigma      = val[10]
        self.path       = val[11]
        self.filename   = val[12]
        self.status     = val[13]
	self.score      = val[14]
	self.ai_score   = val[15]
	self.mjd        = val[16]
	self.rfi_per    = val[17]
	self.is_SPAN    = val[18]

	self.cand_type_id = cand_type_id
	self.freq = 1./(float(self.period) / 1000.)

	# Transform period from s to ms
	#self.period *= 1000.0 

	# Don't want to read another table, just replace .ps.gz by .png
	try:
	    self.filename = self.filename.replace("ps.gz","png")
	except: pass

	# Status is None when a candidate has not been visualized
	if self.status == None:
	    self.status = 0

	# Check RA and DEC are str    
	try:
	    tmp = self.ra.split(':')
	except:
	    tmp = psr_utils.hhmmss_to_hms(self.ra)
	    self.ra = "%d:%d:%d"%(tmp[0], tmp[1], tmp[2])
	    tmp = psr_utils.hhmmss_to_hms(self.dec)
	    self.dec = "%d:%d:%d"%(tmp[0], tmp[1], tmp[2])

	#print self.ra, self.dec
	#coord = SkyCoord(self.ra, self.dec, unit=(u.hourangle, u.deg))
	#print coord
        #self.gl = coord.galactic.l.deg
        #self.gb = coord.galactic.b.deg

    def __str__(self):
	#coord = SkyCoord(self.ra, self.dec, unit=(u.hourangle, u.deg))
        #self.gl = coord.galactic.l.deg
        #self.gb = coord.galactic.b.deg
        self.gl = None
        self.gb = None

        return \
         "Fourier Cand\n" + \
         "RA          : %s\n"%self.ra + \
         "DEC         : %s\n"%self.dec + \
         "l           : %s\n"%self.gl + \
         "b           : %s\n"%self.gb + \
         "MJD         : %s\n"%self.mjd + \
         "Header_id   : %s\n"%self.header_id + \
         "DB Cand_id  : %s\n"%self.cand_id + \
         "Period      : %s\n"%self.period + \
         "DM          : %s\n"%self.dm + \
         "SNR         : %s\n"%self.snr + \
         "Filename    : %s\n"%self.filename + \
         "Score       : %s\n"%self.score + \
         "AI Score    : %s\n"%self.ai_score + \
         "Nb of hits  : %s\n"%self.nhits + \
         "Nb of harms : %s\n"%self.nharm + \
         "RFI Per.    : %s\n"%self.rfi_per + \
         "Status      : %s\n\n"%self.status 

    def set_status(self, status):
        if config.VERBOSE:
	    print "candidate::FourierCand::set_status to %s"%status
        self.status = status

    # Print the postscript for the candidate 
    def print_cand(self, dbname='local-SPAN512-CC'):
        if hasattr(self, 'png'):
	    self.png.save(self.get_filename(dbname), "png")

	    #cmd = "gunzip -c %s/%s > /tmp/%s ; lp -d %s /tmp/%s"%(path, psfile+".gz", psfile, def_printer, psfile)
	    #os.system(cmd)

    def get_plot(self, dbname='local-SPAN512-CC'):
    	# Pipeline V1
        if self.cand_type_id == 1:
	    plotfile = "%s/%s"%(self.path, self.filename)
	    return gtk.gdk.pixbuf_new_from_file(plotfile).scale_simple(900,700,gtk.gdk.INTERP_BILINEAR)
    	# Pipeline V2
        elif self.cand_type_id == 2:

	    if not hasattr(self, 'png'):

	        db = database.Database(dbname)
	        DBconn = db.conn
	        DBcursor = db.cursor
	        query = "SELECT filedata from PDM_Candidate_plots WHERE pdm_cand_id=%d" % (self.cand_id)
	        DBcursor.execute(query)
	        filedata = DBcursor.fetchone()[0]
	        DBconn.close()

	        tmp = gtk.gdk.pixbuf_loader_new_with_mime_type('image/png')
	        tmp.write(bytes(filedata))
		tmp.close()
		self.png = tmp.get_pixbuf()

        
	    return self.png.scale_simple(900,700,gtk.gdk.INTERP_BILINEAR)

    def get_filename(self, dbname='local-SPAN512-CC'):
    	# Pipeline V1
        if self.cand_type_id == 1:
	    return self.filename
    	# Pipeline V2
        elif self.cand_type_id == 2:
	    db = database.Database(dbname)
	    DBconn = db.conn
	    DBcursor = db.cursor
	    query = "SELECT filename from PDM_Candidate_plots WHERE pdm_cand_id=%d" % (self.cand_id)
	    DBcursor.execute(query)
	    filedata = DBcursor.fetchone()[0]
	    DBconn.close()
	    return filedata


class SPCand:
    """Class for the SinglePulse beams
    """
    def __init__(self, val, cand_type_id):
        self.header_id   = val[0]
        self.ra          = val[1]
        self.dec         = val[2]
        self.ftpfilepath = val[3]
        self.filename    = val[4]
        self.status      = val[5]
	self.type_id     = cand_type_id

	# Check RA and DEC are str    
	try:
	    tmp = self.ra.split(':')
	except:
	    tmp = psr_utils.hhmmss_to_hms(self.ra)
	    self.ra = "%d:%d:%d"%(tmp[0], tmp[1], tmp[2])
	    tmp = psr_utils.hhmmss_to_hms(self.dec)
	    self.dec = "%d:%d:%d"%(tmp[0], tmp[1], tmp[2])

	#ra_rad           = psr_utils.ra_to_rad(self.ra)
	#dec_rad          = psr_utils.dec_to_rad(self.dec)
	#dl, db           = slalib.sla_eqgal(ra_rad, dec_rad)
	#coord = SkyCoord(self.ra, self.dec, unit=(u.hourangle, u.deg))
	#self.gl   = coord.galactic.l.deg
	#self.gb    = coord.galactic.b.deg
        self.gl = None
        self.gb = None

	# Don't want to read another table, just replace .ps.gz by .png
	self.filename = self.filename.replace("ps.gz","png")

	# Status is None when a candidate has not been visualized
	if self.status == None:
	    self.status = 0


    def __str__(self):
        return \
         "SP Plot\n" + \
         "RA          : %s\n"%self.ra + \
         "DEC         : %s\n"%self.dec + \
         "Longitude   : %s\n"%self.gl + \
         "Latitude    : %s\n"%self.gb + \
         "Filename    : %s\n"%self.filename 

    def set_status(self, status):
        if config.VERBOSE:
	    print "candidate::FourierCand::set_status to %s"%status
        self.status = status

    def get_type_id(self):
        return self.type_id

    def get_plot(self, dbname='local-SPAN512-CC', type_id=1):
        db = database.Database(dbname)
        DBconn = db.conn
        DBcursor = db.cursor
        query = "SELECT filedata from SP_Plots_Single_Beam WHERE header_id=%d AND sp_single_beam_plot_type_id=%d" % (self.header_id, type_id)
        DBcursor.execute(query)
        filedata = DBcursor.fetchall()
        DBconn.close()

        png = gtk.gdk.pixbuf_loader_new_with_mime_type('image/png')
        png.write(bytes(filedata[0][0]))
	png.close()

        #print png
        #print png.get_pixbuf().scale_simple(900,700,gtk.gdk.INTERP_BILINEAR)

        return png.get_pixbuf().scale_simple(950,950,gtk.gdk.INTERP_BILINEAR)

class Candidates:
    def __init__(self):
        self.cands = []
	self.current_cand_id = 0

    def __len__(self):
        return len(self.cands)

    def __getitem__(self, icand):
        return self.cands[icand]

    def __iter__(self):
        return iter(self.cands)

# TODO: mode should be in both cand declaration

#    def set_mode(self, mode):
#    	self.mode = mode
#
#    def get_mode(self):
#    	return self.mode
    def clear_cands(self):
        self.cands = []

    def add_cands(self, cand):	
    	candlist = utils.get_iterable(cand)
	self.cands.extend(candlist)

    def set_cands(self, cands):	
        self.cands = cands

    def get_cands(self):	
        return self.cands

    def get_cand(self):	
        return self.cands[self.current_cand_id]

    def previous_cand(self):	
        if self.current_cand_id > 0:
	    self.current_cand_id -= 1
	    return True
	else:
	    return False

    def next_cand(self):	
        if self.current_cand_id < len(self.cands)-1:
	    self.current_cand_id += 1
	    return True
	else:
	    return False

    def is_last_cand(self):
	if self.current_cand_id == len(self.cands)-2:
	    return True
	else:
	    return False

    """
    def review(action,self):
    
        try:
            del self.list_to_plot[:]
        except:
            self.list_to_plot=[]

        for i in range(len(self.cands)):
            if self.cands[i].status==1 or self.cands[i].status==2 or self.cands[i].status==3:
	        self.list_to_plot.append(i)
        
        self.cur_cand=0
        self.display_cand_plot(self.list_to_plot[self.cur_cand])
    """
	


