import numpy
#import matplotlib.nxutils
from matplotlib.path import Path
from matplotlib.pyplot import figure
#from matplotlib.widgets import Lasso
import lasso

import candidate
import config
import window

class Plot:
    """Plot class """
    def __init__(self):

        # Lists of different class of candidates
        self.l1 = []; self.l2 = []; self.l3 = []; self.l4 = []; self.l5 = [];
        # Lists of coordinates for the different class of candidates
        self.X1 = []; self.X2 = []; self.X3 = []; self.X4 = []; self.X5 = [];
        self.Y1 = []; self.Y2 = []; self.Y3 = []; self.Y4 = []; self.Y5 = [];

        self.value_x = []
        self.value_y = []

    
	self.fig = figure()
	self.ax1 = self.fig.add_subplot(111)

	# Display Label
	self.xlabel="Frequency (Hz)"
	self.ylabel="Sigma"
	self.ax1.set_xlabel(self.xlabel)
	self.ax1.set_ylabel(self.ylabel)

	self.mode = ""
	self.change_axis = 1

	self.cands = ""
	self.fcands = ""
	self.spcands = ""
	self.dbname = ""

        #self.Cand_window = window.Cand_window(self, self.cands, self.Classification, self.mode)
	self.picked = False

    def set_mode(self, mode):
    	self.mode = mode
	if self.mode == "Fourier":
	    self.cands = self.fcands
	elif self.mode == "SinglePulse":
	    self.cands = self.spcands
	self.Cand_window = window.Cand_window(self, self.cands, self.Classification, self.Known_psrs, self.mode, self.dbname)

    def get_mode(self):
    	return self.mode

    def set_dbname(self, dbname):
    	self.dbname = dbname

    def get_dbname(self):
        return self.dbname

    def set_xlabel(self, label):
    	self.xlabel = label

    def set_ylabel(self, label):
    	self.ylabel = label

    def get_xlabel(self):
    	return self.xlabel

    def get_ylabel(self):
    	return self.ylabel

    def get_fig(self):
        return self.fig
        
    def set_fcands(self, fcands):
        self.fcands = fcands
	#self.Cand_window = window.Cand_window(self, self.cands, self.Classification, self.Known_psrs, self.mode)

    def set_spcands(self, spcands):
        self.spcands = spcands
	#self.Cand_window = window.Cand_window(self, self.cands, self.Classification, self.Known_psrs, self.mode)

    def set_limits(self, Limits):
        self.Limits = Limits

    def set_Classification(self, Classification):
        self.Classification = Classification

    def set_Known_psrs(self, Known_psrs):
        self.Known_psrs = Known_psrs

    def set_canvas(self, canvas):
        self.canvas = canvas

    def draw_graph(self):

        if config.VERBOSE:
              print "plot::draw_graph X1:%d X2:%d X3:%d x4:%d X5:%d"%(len(self.X1), len(self.X2), len(self.X3), len(self.X4), len(self.X5))

        # Xmin Xmax
        xmin,xmax=self.ax1.get_xlim()
        ymin,ymax=self.ax1.get_ylim()

        # Clear and redraw plot
        self.ax1.cla()

        self.pts,self.rfi,self.cand,self.known,self.rfid, = self.ax1.plot( \
		self.X1, self.Y1, 'bo', \
		self.X2, self.Y2, 'k.', \
		self.X3, self.Y3, 'ro', \
		self.X4, self.Y4, 'yo', \
		self.X5, self.Y5, 'g.', picker=5)

        if self.change_axis == 0:
            self.ax1.set_xlim(xmin,xmax)
            self.ax1.set_ylim(ymin,ymax)
        else :
            self.change_axis = 0
	    #GD
        self.ax1.set_xlabel(self.xlabel)
        self.ax1.set_ylabel(self.ylabel)
	self.fig.canvas.draw()
        

    def key_press(self, widget):
        """
	Keys recognized in the main window
	    n : Move the current window to the right
            b : Move the current window to the left
	    r : Try to automatically flag RFIs
	"""
        
        xmin,xmax=self.ax1.get_xlim()
        ymin,ymax=self.ax1.get_ylim()

	# Move the current window to the right
        if widget.key=='n':
            xmin2=xmax-(xmax-xmin)/10.
	    xmax2=xmin2+(xmax-xmin)

            self.ax1.set_xlim(xmin2,xmax2)
            self.ax1.set_ylim(ymin,ymax)
            self.fig.canvas.draw()


	# Move the current window to the left
        if widget.key=='b':
            xmax2=xmin+(xmax-xmin)/10.
	    xmin2=xmax2-(xmax-xmin)

            self.ax1.set_xlim(xmin2,xmax2)
            self.ax1.set_ylim(ymin,ymax)
            self.fig.canvas.draw()


        # Try to automatically flag candidates as RFI 
	"""
	if widget.key=='r':
	    rfid={}
	    tot_rfi_removed=0
	    for i in range(self.tot_cands):
	        #print str(self.list[i].period)[0:6]
	        per = str(self.cand_list[i].period)[0:5]
		if rfid.has_key(per):
		    rfid[per]=rfid[per]+1
		else:
		    rfid[per]=1
	    for per in rfid:
	        if rfid[per] > int(self.tot_cands*10/100.):
		    tot_rfi_removed+=rfid[per]
		    print per, rfid[per]
	    print "total removed : ",tot_rfi_removed

	    # Put flag to value "11"
	    for i in range(self.tot_cands):
	        per = str(self.cand_list[i].period)[0:5]
		if rfid[per] > 10:		
	            self.cand_list[i].status=11

	    # Redraw plot
	    dispatch_status(self) 
	    self.draw_graph()
	"""


    # Select a single candidate to view
    def onpick(self, event):
	if not self.picked:
	    self.picked = True
	    display = True
	else:
	    display = False

        ind = event.ind
        N = len(ind)
        if not N: return True

	if config.VERBOSE:
	    print "plot::onpick> event.artist", event.artist
	    print "plot::onpick> indices", ind


	for pick_id in ind:
	    cand_id = None

	    if event.artist==self.pts:    # l1
		cand_id = self.l1[pick_id]
	    if event.artist==self.rfi:    #l2
		cand_id = self.l2[pick_id]
	    if event.artist==self.cand:   #l3 
		cand_id = self.l3[pick_id]
	    if event.artist==self.known:  #l4 
		cand_id = self.l4[pick_id]
	    if event.artist==self.rfid:  #l5
		cand_id = self.l5[pick_id]


	    if cand_id:
		print "plot::onpick> Picked cand %d \n"% (cand_id)
		cand = self.cands[cand_id]
        	self.Cand_window.candidates.add_cands(cand)



        # Display the selected cand in a popup
        # GD self.Cand_window = window.Cand_window(self, self.cands, self.Classification, self.mode)
        #self.Cand_window.candidates.add_cands(cand)
	#if self.Cand_window.candidates.is_last_cand():
	if display:
	    self.Cand_window.candidates.next_cand()
	    self.Cand_window.show_cands()
	    timer = self.fig.canvas.new_timer(interval=200)
	    timer.add_callback(self.reset_picked)
	    timer.start()
	    
    def reset_picked(self):
	self.picked = False


    # Activate LASSO with butt 3
    def onpress(self, event):

	#print event
        if event.button != 3: return
        if self.fig.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
	#print "Get Lasso"
        self.lasso = lasso.Lasso(event.inaxes, (event.xdata, event.ydata), self.select_mlt)

        # acquire a lock on the widget drawing
        self.fig.canvas.widgetlock(self.lasso)

    def review(self):
        self.Cand_window.candidates.clear_cands()
	for cand in self.cands:
	    if cand.status==1 or cand.status==2 or cand.status==3:
	        self.Cand_window.candidates.add_cands(cand)
        self.Cand_window.candidates.next_cand()
        self.Cand_window.show_cands()

	
    # Sort the candidates defined with LASSO
    def select_mlt(self, verts=None):
        """
        create a list of candidate to plot
        list_to_plot

        """
        i=0
        all_pts=[]
	ind = []
	path = Path(verts)

        for i in range(len(self.X1)):
            #all_pts.append((self.X1[i], self.Y1[i]))
	    #print "plot::select_mlt> point: ", (self.X1[i], self.Y1[i])
	    try:
	        if path.contains_point((self.X1[i], self.Y1[i])):
		    ind.append(i)
	    except:
	        continue

	#ind = numpy.nonzero(matplotlib.nxutils.points_inside_poly(all_pts, verts))[0]
	#path = Path(verts)
	#ind = path.contains_point(all_pts)
	print ind


	self.canvas.draw_idle()
	self.canvas.widgetlock.release(self.lasso)
	del self.lasso

	indices = [self.l1[idx] for idx in ind]
	if config.VERBOSE:
	    print "plot::select_mlt> Picked l1 cands: ", ind
	    print "plot::select_mlt> conversion to global cands: ", indices



	if len(ind):
	    #self.Cand_window(self.cands[cand_id])
	    #self.Cand_window.show_cands()
	    self.Cand_window.candidates.add_cands([self.cands[idx] for idx in indices])
	    self.Cand_window.candidates.next_cand()
	    self.Cand_window.show_cands()


    def change_status(self, cand):
	"""
	Human 8-Level Classification by Patrick Lazarus

	0 	: l1 	 Cand
	1 	: l3	 Class 1 cand, good 
	2 	: l3	 Class 2 cand, why not 
	3 	: l3	 Class 3 cand, not good 
	4 	: l5	 RFI 
	5 	: l2	 Not a pulsar 
	6 	: l4	 Known
	7 	: l2	 Harmonics
	"""   

	cand_id = self.cands.index(cand)
	if config.VERBOSE:
	    print "plot::change_status> Changing cand_id %s to list for status %s"%(cand_id, cand.status)

	#if self.mode=="Fourier":
	if 1:

	    # Remove current cand from list
	    if cand_id in self.l1:
		idx = self.l1.index(cand_id) 
		self.l1.remove(cand_id)
		x_tmp = self.X1[idx]; y_tmp = self.Y1[idx]
		self.X1 = numpy.delete(self.X1, idx)
		self.Y1 = numpy.delete(self.Y1, idx)

	    elif cand_id in self.l2:
		idx = self.l2.index(cand_id) 
		self.l2.remove(cand_id)
		x_tmp = self.X2[idx]; y_tmp = self.Y2[idx]
		self.X2 = numpy.delete(self.X2, idx)
		self.Y2 = numpy.delete(self.Y2, idx)

	    elif cand_id in self.l3:
		idx = self.l3.index(cand_id) 
		self.l3.remove(cand_id)
		x_tmp = self.X3[idx]; y_tmp = self.Y3[idx]
		self.X3 = numpy.delete(self.X3, idx)
		self.Y3 = numpy.delete(self.Y3, idx)

	    elif cand_id in self.l4:
		idx = self.l4.index(cand_id) 
		self.l4.remove(cand_id)
		x_tmp = self.X4[idx]; y_tmp = self.Y4[idx]
		self.X4 = numpy.delete(self.X4, idx)
		self.Y4 = numpy.delete(self.Y4, idx)

	    elif cand_id in self.l5:
		idx = self.l5.index(cand_id) 
		self.l5.remove(cand_id)
		x_tmp = self.X5[idx]; y_tmp = self.Y5[idx]
		self.X5 = numpy.delete(self.X5, idx)
		self.Y5 = numpy.delete(self.Y5, idx)

	    # Now add the candidate to the correct list
	    if cand.status==0:
		self.l1.append(cand_id)
		self.X1 = numpy.append(self.X1, x_tmp)
		self.Y1 = numpy.append(self.Y1, y_tmp)

	    elif cand.status==1 or cand.status==2 or cand.status==3:
		self.l3.append(cand_id)
		self.X3 = numpy.append(self.X3, x_tmp)
		self.Y3 = numpy.append(self.Y3, y_tmp)

	    elif cand.status==4:
		self.l5.append(cand_id)
		self.X5 = numpy.append(self.X5, x_tmp)
		self.Y5 = numpy.append(self.Y5, y_tmp)

	    elif cand.status==5 or cand.status==7:
		self.l2.append(cand_id)
		self.X2 = numpy.append(self.X2, x_tmp)
		self.Y2 = numpy.append(self.Y2, y_tmp)

	    elif cand.status==6:
		self.l4.append(cand_id)
		self.X4 = numpy.append(self.X4, x_tmp)
		self.Y4 = numpy.append(self.Y4, y_tmp)


    def dispatch_status(self):
	"""
	Dispatch the candidates from the x-y numpy.arrays 'self.value_x'
	into 5 numpy.arrays depending on their status
	Human 8-Level Classification by Patrick Lazarus

	0 	: 	 Cand
	1 	: 	 Class 1 cand, good 
	2 	: 	 Class 2 cand, why not 
	3 	: 	 Class 3 cand, not good 
	4 	: 	 RFI 
	5 	: 	 Not a pulsar 
	6 	:	 Known
	7 	:	 Harmonics
	"""   
	x_val_1=[];y_val_1=[]
	x_val_2=[];y_val_2=[]
	x_val_3=[];y_val_3=[]
	x_val_4=[];y_val_4=[]
	x_val_5=[];y_val_5=[]

	del self.l1[:];del self.l2[:];del self.l3[:];del self.l4[:];del self.l5[:]

	if config.VERBOSE:
	    print "plot::dispatch_status> Mode=%s, limits activated=%s"%(self.get_mode(), self.Limits.is_limits_on())

	#if self.get_mode() == "Fourier":
	#if self.get_mode() == "Fourier"
	for i,cand in enumerate(self.cands):
		if self.get_mode() == "Fourier" and self.Limits.is_limits_on() and (\
			    not self.Limits.check_dm(cand.dm)  or \
			    not self.Limits.check_snr(cand.snr)  or \
			    not self.Limits.check_score(cand.score)   or \
			    not self.Limits.check_nharm(cand.nharm) or \
			    not self.Limits.check_period(cand.period) or \
			    not self.Limits.check_ai_score(cand.ai_score) or \
			    not self.Limits.check_rfi_per(cand.rfi_per) or \
			    not self.Limits.check_is_SPAN(cand.is_SPAN)): 
		    continue		    

		if cand.status==0:
		    x_val_1.append(self.value_x[i])
		    y_val_1.append(self.value_y[i])
		    self.l1.append(i)
		    continue
		if cand.status==5 or cand.status==7:
		    x_val_2.append(self.value_x[i])
		    y_val_2.append(self.value_y[i])
		    self.l2.append(i)
		    continue
		if cand.status==1 or cand.status==2 or cand.status==3:
		    x_val_3.append(self.value_x[i])
		    y_val_3.append(self.value_y[i])
		    self.l3.append(i)
		    continue
		if cand.status==6:
		    x_val_4.append(self.value_x[i])
		    y_val_4.append(self.value_y[i])
		    self.l4.append(i)
		    continue
		if cand.status==4:
		    x_val_5.append(self.value_x[i])
		    y_val_5.append(self.value_y[i])
		    self.l5.append(i)
		    continue
	"""
	if self.get_mode() == "SinglePulse":
	    for sp in self.cands:
		if sp.status==0:
		    x_val_1.append(self.value_x[i])
		    y_val_1.append(log10(self.value_y[i]))
		    self.l1.append(i)
		    continue
		if sp.status==1:
		    x_val_2.append(self.value_x[i])
		    y_val_2.append(log10(self.value_y[i]))
		    self.l2.append(i)
		    continue
		if sp.status==5 or sp.status==6 or sp.status==7:
		    x_val_3.append(self.value_x[i])
		    y_val_3.append(log10(self.value_y[i]))
		    self.l3.append(i)
	"""	    

	self.X1 = numpy.array(x_val_1); self.Y1 = numpy.array(y_val_1)
	self.X2 = numpy.array(x_val_2); self.Y2 = numpy.array(y_val_2)
	self.X3 = numpy.array(x_val_3); self.Y3 = numpy.array(y_val_3)
	self.X4 = numpy.array(x_val_4); self.Y4 = numpy.array(y_val_4)
	self.X5 = numpy.array(x_val_5); self.Y5 = numpy.array(y_val_5)

	#if VERBOSE:
	#print "psrhunt> %d candidates : "%(len(self.cands)), " ",len(self.X1), len(self.X2), len(self.X3), len(self.X4), len(self.X5)


    def dispatch_x_axis(self, label):
	if config.VERBOSE:
	    print "plot::dispatch_x_axis>  label: %s"%label 

	del self.value_x[:]

	# Fourier Mode
	if self.get_mode() == 'Fourier':
	    if "Period" in label:
		for cand in self.cands:
		    self.value_x.append(cand.period)
	    elif "Frequency" in label:
		for cand in self.cands:
		    self.value_x.append(cand.freq)
	    elif "MJD" in label:
		for cand in self.cands:
		    self.value_x.append(cand.mjd)
	    elif "DM" in label:
		for cand in self.cands:
		    self.value_x.append(cand.dm)
	    elif "AI" in label:
		for cand in self.cands:
		    self.value_x.append(cand.ai_score)
	    elif "ID" in label:
		for cand in self.cands:
		    self.value_x.append(cand.header_id)

	elif self.get_mode() == 'SinglePulse':
	    for cand in self.cands:
		self.value_x.append(cand.longitude)


    def dispatch_y_axis(self, label):
	if config.VERBOSE:
	    print "plot::dispatch_y_axis>  label: %s"%label

	del self.value_y[:]

	# Fourier Mode
	if self.get_mode() == 'Fourier':
	    if "Sigma" in label:
		for cand in self.cands:
		    self.value_y.append(cand.sigma)
	    elif "SNR" in label:
		for cand in self.cands:
		    self.value_y.append(cand.snr)
	    elif "Coherent Pow" in label:
		for cand in self.cands:
		    self.value_y.append(cand.cpow)
	    elif "Score" in label:
		for cand in self.cands:
		    self.value_y.append(cand.score)
	    elif "AI" in label:
		for cand in self.cands:
		    self.value_y.append(cand.ai_score)

	elif self.get_mode() == 'SinglePulse':
	    for cand in self.cands:
		self.value_y.append(cand.latitude)
