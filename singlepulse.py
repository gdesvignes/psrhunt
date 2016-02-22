import struct
import sys
import cProfile
import gtk

import numpy as np
#import matplotlib
#matplotlib.use('GTK')
import matplotlib.pyplot as plt

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


    def get_fig(self):
	self.fig = plt.figure()

	# SNR Histogram
	self.ax1 = self.fig.add_subplot(2, 3, 1, xlabel="SNR", ylabel="Number of events")
	self.ax1.hist(self.data[:,2].compressed(), bins=20, log=True)

	self.ax1.set_ylim(1 )

	# DM Histogram
	self.ax2 = self.fig.add_subplot(2, 3, 2, xlabel="DM (pc cm-3)", ylabel="Number of events")
	self.ax2.hist(self.data[:,0].compressed(), bins=20, log=True)
	self.ax2.set_ylim(1)

	# SNR vs DM
	self.ax3 = self.fig.add_subplot(2, 3, 3, xlabel="DM (pc cm-3)", ylabel="SNR")
	self.ax3.plot(self.data[:,0], self.data[:,2], 'k.')

	# DM vs Time plot
	self.ax4 = self.fig.add_subplot(2, 1, 2, xlabel="Time (s)", ylabel="DM (pc cm-3)")
	#self.ax4.plot(self.data[:,1], self.data[:,0], 'ko', ms=self.data[:,2]/6.0)
	#self.ax4.plot(self.data[:,1], self.data[:,0], 'k.')

	#self.fig.canvas.mpl_connect('motion_notify_event', self.update)
	#self.fig.canvas.mpl_connect('button_release_event', self.update)
	#self.fig.canvas.mpl_connect('key_press_event', self.update)
        if config.VERBOSE:
	    print "singlepulse::get_fig> Total nb of events: ", len(self.data[:,0].compressed())

	snr_list = [[6,8, 3], [8,10, 6] , [10,12, 9], [12,15, 15] , [20,100, 20]]
	for snr1,snr2,ms in snr_list:
	    mask = np.logical_or(self.data[:,2] <= snr1, self.data[:,2]>snr2)
	    print mask
	    snr_mask = np.repeat(mask, self.data.shape[1])
	    print snr_mask

            if config.VERBOSE:
	        print "singlepulse::get_fig> Range of SNR", snr1, snr2, ms
	    #snr_mask = np.repeat(self.data[:,2] < snr, self.data.shape[1])
	    tmp_data = np.ma.array(self.data, mask=snr_mask)
            if config.VERBOSE:
	        print "singlepulse::get_fig>      Nb of events: ", len(tmp_data[:,0].compressed())
	    self.ax4.plot(tmp_data[:,1], tmp_data[:,0], 'ko', ms=ms, markerfacecolor='none')
	    
        if config.VERBOSE:
	    print "singlepulse::get_fig> List of SNRs to be plotted", snr_list



	return self.fig

    def update(self, canvas, event):

        if config.VERBOSE:
	    print "singlepulse::update> Will update the canvas"
            #print "singlepulse::update> ", canvas, event

	if self.cur_view == 0:
	  self.ax4.set_ylim(-1, self.max_dm)
	elif self.cur_view == 1:
	  self.ax4.set_ylim(-1,120)
	elif self.cur_view == 2:
	  self.ax4.set_ylim(100,320)
	elif self.cur_view == 3:
	  self.ax4.set_ylim(300, self.max_dm)

	# Retrieve main plots limits
        time_lim = self.ax4.get_xlim()
        DM_lim = self.ax4.get_ylim()

	# Clear top panels
	self.ax1.cla() 
	self.ax2.cla() 
	self.ax3.cla() 

	snr_mask = np.repeat(np.logical_or(np.logical_or(self.data[:,1]<time_lim[0], self.data[:,1]>time_lim[1]), np.logical_or(self.data[:,0]<DM_lim[0], self.data[:,0]>DM_lim[1])), self.data.shape[1])
	data = np.ma.array(self.data, mask=snr_mask)

	# SNR Histogram
	self.ax1.hist(data[:,2].compressed(), bins=20, log=True)
	self.ax1.set_xlabel("SNR")
	self.ax1.set_ylabel("Number of events")
	self.ax1.set_ylim(1)

	# DM Histogram
	self.ax2.hist(data[:,0].compressed(), bins=20, log=True)
	self.ax2.set_xlabel("DM (pc cm-3)")
	self.ax2.set_ylabel("Number of events")
	self.ax2.set_ylim(1)

	# SNR vs DM
	self.ax3.plot(data[:,0], data[:,2], 'k.')
	self.ax3.set_xlabel("DM (pc cm-3)")
	self.ax3.set_ylabel("SNR")
	self.ax3.set_xlim(DM_lim)
	#self.ax3.set_ylim()

	self.fig.canvas.draw()

    def next_view(self, data, event):
        # Detect a keyboard press
	keyname = gtk.gdk.keyval_name(event.keyval)
	if keyname == 'z':
            self.cur_view += 1
	    self.cur_view = self.cur_view%NVIEW 
	    self.update(None, None)

#def main():
if __name__ == '__main__':
    sp = SinglePulse(sys.argv[1])    
    sp.get_fig()

#cProfile.run('main()')
