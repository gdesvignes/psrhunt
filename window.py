import gtk
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

import config
import known_psrs
import candidate
import singlepulse
import os

class Cand_window:
    def __init__(self, Plot, Cands, Classification, Known_psrs, mode, dbname):
    #def __init__(self, Plot, mode):
        
	self.Plot = Plot
	self.Cands = Cands
	self.Classification = Classification
	self.candidates = candidate.Candidates()
	self.mode = mode
	self.dbname = dbname

	self.Known_psrs = Known_psrs
	#self.PSR_list = known_psrs.PSR_list()

	# def():
	#self.current_cand = self.candidates[0]
	#if config.VERBOSE:
	#    print "window::add_cands> Added %d cands to the list"%len(candlist)

    def show_cands(self):
        """
		Display the current cand in a popup
        """

	cand = self.candidates.get_cand()

        if config.VERBOSE: 
	    print "window::show_cands> Display cand \n", cand
	
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)

	# HBox with the frame plot and the known PSR
	p1 = gtk.HBox()

	# Frame Plot
	frame_plot = gtk.Frame()

	# Frame known PSRs
	scrolled_window = self.Known_psrs.show_known_psrs(cand)

	frame_known_psr = gtk.Frame()
	frame_known_psr.add(scrolled_window)

	p1.pack_start(frame_plot, expand=True, padding = 5)
	p1.pack_start(frame_known_psr, expand=True, padding = 5)

	#main_vbox.pack_start(frame_plot, padding=5)

	# Vertical box that contains the 2 horizontal subboxes
	main_vbox = gtk.VBox()
	main_window.add(main_vbox)
	main_vbox.pack_start(p1, padding = 5)


	# Frame Options 
	frame2 = gtk.Frame("Opts")
	main_window.buttons_box = gtk.HBox()
	frame2.add(main_window.buttons_box)

	# Frame Options - Detection Level - Call to set_cand_signal
	self.button1 = gtk.ToggleButton("Class 1")
	main_window.buttons_box.add(self.button1)
	self.button1.connect("toggled",self.set_cand_signal,"1")

	self.button2 = gtk.ToggleButton("Class 2")
	main_window.buttons_box.add(self.button2)
	self.button2.connect("toggled",self.set_cand_signal,"2")

	self.button3 = gtk.ToggleButton("Class 3")
	main_window.buttons_box.add(self.button3)
	self.button3.connect("toggled",self.set_cand_signal,"3")

	self.button4 = gtk.ToggleButton("RFI")
	main_window.buttons_box.add(self.button4)
	self.button4.connect("toggled",self.set_cand_signal,"4")

	self.button5 = gtk.ToggleButton("Not a pulsar")
	main_window.buttons_box.add(self.button5)
	self.button5.connect("toggled",self.set_cand_signal,"5")

	self.button6 = gtk.ToggleButton("Known Pulsar")
	main_window.buttons_box.add(self.button6)
	self.button6.connect("toggled",self.set_cand_signal,"6")

	self.button7 = gtk.ToggleButton("Harmonic")
	main_window.buttons_box.add(self.button7)
	self.button7.connect("toggled",self.set_cand_signal,"7")

	self.button_plot = gtk.Button("Print")
	main_window.buttons_box.add(self.button_plot)
	self.button_plot.connect("clicked", self.print_cand)

	# Keep track of the current candidate for calls
	self.key_event = main_window.connect('key_press_event', self.key_press)

	#print "GD", self.mode, cand

	if self.mode=="Fourier":
	    plot = gtk.Image()

	    main_window.set_size_request(1200, 800)
            main_window.set_title(cand.get_filename(dbname=self.dbname))
	    #plotfile = "%s/%s"%(cand.path, cand.filename)
	    #print "Will display %s"%plotfile
	    plot.set_from_pixbuf(cand.get_plot(dbname=self.dbname))
	    frame_plot.add(plot)

	if self.mode=="SinglePulse":
	    scroll_win = gtk.ScrolledWindow()
	    scrolled_window.set_border_width(4)
	    scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

	    main_window.set_size_request(1000,1000)

	    plots = gtk.VBox()

	    plot = gtk.Image()
	    plot.set_from_pixbuf(cand.get_plot(dbname=self.dbname))
	    plots.pack_start(plot)

	    plot2 = gtk.Image()
	    plot2.set_from_pixbuf(cand.get_plot(dbname=self.dbname, type_id=2))
	    plots.pack_start(plot2)

	    plot3 = gtk.Image()
	    plot3.set_from_pixbuf(cand.get_plot(dbname=self.dbname,type_id=3))
	    plots.pack_start(plot3)

	    scroll_win.add_with_viewport(plots)

	    """
	    if cand.get_type_id() == 1:
	        plot = gtk.Image()
	        plot.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(plotfile).scale_simple(700,700,gtk.gdk.INTERP_BILINEAR))
	    elif cand.get_type_id() == 2:		
	        plot = gtk.VBox()
	    	sp = singlepulse.SinglePulse( os.path.join(config.CC_RESULTS_DIR, cand.ftpfilepath, cand.filename) )
	        canvas = FigureCanvas(sp.get_fig())
		canvas.connect('button_release_event', sp.update)
		canvas.connect('key_press_event', sp.next_view)
		#canvas.mpl_connect('button_release_event', sp.update)
		#canvas.mpl_connect('key_press_event', sp.update)
		toolbar = NavigationToolbar(canvas, self)
		toolbar.connect('button_release_event', sp.update)
		plot.pack_start(canvas)
		plot.pack_start(toolbar, False, False)
	    """	
	        
	    frame_plot.add(scroll_win)


	# Set Previous status of toggle self.button
	if cand.status == 0: # Update point status if not seen
	    #print "window::show_cands> TODO"
	    self.set_cand_signal(self.button1, 5)
	elif cand.status == 1:
	    self.button1.set_active(True)
	elif cand.status == 2:
	    self.button2.set_active(True)
	elif cand.status == 3:
	    self.button3.set_active(True)
	elif cand.status == 4:
	    self.button4.set_active(True)
	elif cand.status == 5:
	    self.button5.set_active(True)
	elif cand.status == 6:
	    self.button6.set_active(True)
	elif cand.status == 7:
	    self.button7.set_active(True)

	main_vbox.pack_start(frame2, expand=False, padding=5)

	main_window.show_all()

	self.main_window = main_window
	#return main_window


    # Set Candidate to be a potential PSR
    def print_cand(self, widget=None, event=None, data=None):
        if config.VERBOSE:
	    print "window::print_cand> widget=%s, event=%s, data=%s,"%(widget, event, data)
	cand = self.candidates.get_cand()
	cand.print_cand(dbname=self.dbname)

    # Set Candidate to be a potential PSR
    def set_cand_signal(self, widget=None, event=None, data=None):
        if config.VERBOSE:
	    print "window::set_cand_signal> widget=%s, event=%s, data=%s,"%(widget, event, data)

        doit = 0

	try:    
            if widget.get_active() or widget == "keyboard":
	        doit = 1
	except:
	    print "window::set_cand_signal> Widget not recognized: ", widget
	    pass

	cand = self.candidates.get_cand()    

	if doit:
	    # Class 1 Cand
	    if event=="1":
		# Untoggle others buttons
	        self.button1.set_active(True)
	        self.button2.set_active(False)
	        self.button3.set_active(False)
	        self.button4.set_active(False)
	        self.button5.set_active(False)
	        self.button6.set_active(False)
	        self.button7.set_active(False)

                cand.set_status(1)

	    # Class 2 Cand
	    if event=="2":
		# Untoggle others buttons
	        self.button1.set_active(False)
	        self.button2.set_active(True)
	        self.button3.set_active(False)
	        self.button4.set_active(False)
	        self.button5.set_active(False)
	        self.button6.set_active(False)
	        self.button7.set_active(False)

                cand.set_status(2)

	    # Class 3 Cand
	    if event=="3":
		# Untoggle others buttons
	        self.button1.set_active(False)
	        self.button2.set_active(False)
	        self.button3.set_active(True)
	        self.button4.set_active(False)
	        self.button5.set_active(False)
	        self.button6.set_active(False)
	        self.button7.set_active(False)

                cand.set_status(3)

	    # RFI 
	    if event=="4":
		# Untoggle others buttons
	        self.button1.set_active(False)
	        self.button2.set_active(False)
	        self.button3.set_active(False)
	        self.button4.set_active(True)
	        self.button5.set_active(False)
	        self.button6.set_active(False)
	        self.button7.set_active(False)

                cand.set_status(4)

	    #  Not a pulsar 
	    if event=="5":
		# Untoggle others buttons
	        self.button1.set_active(False)
	        self.button2.set_active(False)
	        self.button3.set_active(False)
	        self.button4.set_active(False)
	        self.button5.set_active(True)
	        self.button6.set_active(False)
	        self.button7.set_active(False)

                cand.set_status(5)

	    # Known pulsar
	    if event=="6":
			# Untoggle others buttons
	        self.button1.set_active(False)
	        self.button2.set_active(False)
	        self.button3.set_active(False)
	        self.button4.set_active(False)
	        self.button5.set_active(False)
	        self.button6.set_active(True)
	        self.button7.set_active(False)

                cand.set_status(6)

	    # Harmonic
	    if event=="7":
			# Untoggle others buttons
	        self.button1.set_active(False)
	        self.button2.set_active(False)
	        self.button3.set_active(False)
	        self.button4.set_active(False)
	        self.button5.set_active(False)
	        self.button6.set_active(False)
	        self.button7.set_active(True)

                cand.set_status(7)

            #self.candidates.next_cand()
            #self.show_cands()
	else:
	    if cand.status==0:
	        cand.set_status(5)

	# Redraw graph taking into account the new rank of the vizualized candidate
	self.Plot.change_status(cand)
	self.Plot.draw_graph()
	# 
	self.Classification.write_classification(cand)





    def key_press(self, data, event):
        """
	Keys recognized in the candidate window
		1-7 : Set the status
		x   : Go to previous plot 
		c   : Go to next plot
		s   : Display SinglePulse plot
	"""

	# Detect a Status keyboard press
	keyname = gtk.gdk.keyval_name(event.keyval)
	if keyname in ['1', '2', '3', '4', '5', '6', '7']:
	    self.set_cand_signal("keyboard", keyname)

	# Go to previous Plot
	if keyname=='x':
	    if self.candidates.previous_cand():
	        self.main_window.destroy()
		self.show_cands()

	# Go to next candidate in the 'list_to_plot'
	if keyname=='c':
	    self.main_window.destroy()
	    if self.candidates.next_cand() :
		self.show_cands()

	# Exit the current list of cands to plot
	if keyname=='q':
	    self.main_window.destroy()
	    self.candidates.clear_cands()

	# Add to list of reobservations
	if keyname=='a':
	    self.Classification.reobs_cand(cand)


        """
	if keyname=='s' and self.mode=='Fourier':
	    # Display Single Pulse
	    self.spwin=gtk.Window(gtk.WINDOW_TOPLEVEL)
	
	    plot=gtk.Image()
	    self.spwin.set_title("Single Pulse")
	    self.spwin.set_size_request(800,800)

	    #plotfile=
	    try:
	        plot.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(plotfile).scale_simple(700,700,gtk.gdk.INTERP_BILINEAR))
	    except:
	        pass
	    	

	    # Main Frame
	    main_vbox = gtk.VBox()
	    self.spwin.add(main_vbox)

	    # Frame SinglePulse
	    frame_plot = gtk.Frame()
	    frame_plot.add(plot)
	    main_vbox.pack_start(frame_plot, padding=5)

	    # Frame Options 
	    frame2 = gtk.Frame("Opts")
	    self.spwin.buttons_box = gtk.HBox()
	    frame2.add(self.spwin.buttons_box)

	    # Frame Options - Detection Level
	    self.button1 = gtk.ToggleButton('Top Candidate')
	    self.spwin.buttons_box.add(self.button1)
	    self.button1.connect("toggled",self.set_cand,'1')

	    self.button2 = gtk.ToggleButton('Maybe')
	    self.spwin.buttons_box.add(self.button2)
	    self.button2.connect("toggled",self.set_cand,'2')

	    self.button3 = gtk.ToggleButton('Not sure at all')
	    self.spwin.buttons_box.add(self.button3)
	    self.button3.connect("toggled",self.set_cand,'3')

	    self.button_plot = gtk.Button("Print")
	    self.spwin.buttons_box.add(self.button_plot)

	    self.button_plot.connect("clicked", self.print_cand)

            # Set Previous status of toggle self.button
	    self.idx_sp=self.beam_id_list.index(self.cand_list[self.idx].beam)

	    if self.sp_status_list[self.idx_sp] == 5:
		self.button1.set_active(True)
	    elif self.sp_status_list[self.idx_sp] == 6:
		self.button2.set_active(True)
	    elif self.sp_status_list[self.idx_sp] == 7:
		self.button3.set_active(True)

	    main_vbox.pack_start(frame2, padding=5)

	    #self.spwin.add(plot)
	    self.spwin.show_all()
	"""    
