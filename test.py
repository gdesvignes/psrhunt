import struct
import sys
import cProfile

import numpy as np

import config

NVIEW = 4 

class SinglePulse:
    def __init__(self, filename):
        self.readfile(filename)
	#self.display()

	# cur_view is 0, 1 ,2, 3
	self.cur_view = 0

    def readfile(self, filename):
	test = np.empty(shape=(config.MAX_SP_EVENTS,3))

	if config.VERBOSE:
	    print "singlepulse::readfile> Will open file %s"%filename
	try:
	    pfi = open(filename, 'rb')
	except:
	   print "singlepulse::readfile> Could not open file %s"%filename
	   raise
	nb_dms, = struct.unpack('<i', pfi.read(4))
	print nb_dms

	tot_events = 0
	
	for idm in range(nb_dms):
	    dm, nb_events, = struct.unpack('<fi', pfi.read(4+4))
	    #print dm, nb_events
	    events = struct.unpack('<%df'%(2*nb_events), pfi.read((4+4)*nb_events))

	    # Reorder the data
	    #events = np.asarray(events)
	    #events = events.reshape(events.shape[0]/2, 2)
	    #events = np.concatenate( ((np.asarray([[dm] * len(events)])).T, events), axis=1 )

	    for i in range(nb_events):
		test[tot_events+i,0] = dm
		test[tot_events+i,1] = events[2*i]
		test[tot_events+i,2] = events[2*i+1]
	    tot_events += nb_events    


	pfi.close()

	self.max_dm = max(test[:,0])

	# Removed unused rows
	test = np.delete(test, np.s_[tot_events:], 0)

	snr_mask = np.repeat(test[:,2]<config.SP_MIN_SNR, test.shape[1])
	#snr_mask = np.repeat(data[:,2]<5.0, data.shape[1])
	self.data = np.ma.array(test, mask=snr_mask)


