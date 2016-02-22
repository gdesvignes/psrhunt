import getpass
import gtk
import gobject

from matplotlib.pyplot import figure, show
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

import config
import candidate
import plot
import classification
import limits
import known_psrs
import query
import users



class Manager(gtk.Window):


    def menu_activate_action(self, widget=None, event=None, data=None):
	print 'Action "%s" activated' % widget.get_name()
	if "Save" in widget.get_name():
	    self.Classification.save2db()

    def menu_review(self, widget=None, event=None, data=None):
        print 'Reviewing candidates'
        self.Plot.review()

    def menu_set_limits(self, widget=None, event=None, data=None):
        self.Limits.set_limits()

    def menu_mysqlquery(self, widget=None, event=None, data=None):
        
	print "self.database: ", self.database
	Query = query.Query(self.database, self.Users)

	fcands, spcands = Query.query_cands()
	if fcands:
	    self.Plot.set_fcands(fcands.get_cands())
	if spcands:
	    self.Plot.set_spcands(spcands.get_cands())

	# Update the main plot
	self.Plot.set_mode(self.mode)
	self.update_main_plot()

    def menu_activate_limits(self, widget=None, event=None, data=None):
        if config.VERBOSE:
	    print "menus::menu_activate_limits> ", widget, event, data
        self.Limits.activate_limits(widget, event, data)
	self.Plot.set_limits(self.Limits)
	self.Plot.dispatch_status()
	print 'nb cand:', len(self.Plot.X1), len(self.Plot.X2), len(self.Plot.X5) 
	self.Plot.draw_graph()
	    
    #def radio_action(action, ):
    def radio_action(self, widget=None, event=None, data=None):
	"""
	Process the events from the radio buttons
	"""
	if config.VERBOSE:
	    print "psrhunt> radio_action: '%s' '%s' %s"%( widget.get_name(), event.get_name(), data)

	if "SinglePulse" in event.get_name():
	    self.Classification.set_mode("SinglePulse")
	    self.Plot.set_mode("SinglePulse")
	    self.Plot.set_xlabel("Longitude")
	    self.Plot.set_ylabel("Latitude")
	    self.update_main_plot()

	if "Fourier" in event.get_name():
	    self.Classification.set_mode("Fourier")
	    self.Plot.set_mode("Fourier")
	    self.Plot.set_xlabel("Frequency (Hz)")
	    self.Plot.set_ylabel("Sigma")
	    self.update_main_plot()

	# X SCALE
	if "Period" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_xlabel("Period (ms)")
	    self.update_main_plot()
	if "Frequency" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_xlabel("Frequency (Hz)")
	    self.update_main_plot()
	if "MJD" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_xlabel("MJD")
	    self.update_main_plot()
	if "DM" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_xlabel("DM")
	    self.update_main_plot()
	if "AI X" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_xlabel("AI")
	    self.update_main_plot()
	if "ID" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_xlabel("ID")
	    self.update_main_plot()

	# Y SCALE
	if "Sigma" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_ylabel("Sigma")
	    self.update_main_plot()
	if "SNR" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_ylabel("SNR")
	    self.update_main_plot()
	if "Coherent Pow" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_ylabel("Coherent Power")
	    self.update_main_plot()
	if "Score" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_ylabel("Score")
	    self.update_main_plot()
	if "AI Y" in event.get_name() and self.mode=="Fourier":
	    self.Plot.set_ylabel("AI")
	    self.update_main_plot()

	# User Name actions
	if "Gregory" in event.get_name():
	    self.Users.set_user("GD")
	    self.Classification.change_user(self.Users)
	    return
	elif "Ismael" in event.get_name():
	    self.Users.set_user("IC")
	    self.Classification.change_user(self.Users)
	    return
	elif "Kuo" in event.get_name():
	    self.Users.set_user("KL")
	    self.Classification.change_user(self.Users)
	    return
	elif "Franca" in event.get_name():
	    self.Users.set_user("G1")
	    self.Classification.change_user(self.Users)
	    return
	elif "David" in event.get_name():
	    self.Users.set_user("DS")
	    self.Classification.change_user(self.Users)
	    return
	elif "Franck" in event.get_name():
	    self.Users.set_user("FO")
	    self.Classification.change_user(self.Users)
	    return



	# Database choice
	if "PALFA" == event.get_name():
	    self.database="local-PALFA"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return
	elif "NBPP" == event.get_name():
	    self.database="local-NBPP"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return
	elif "SPAN512" == event.get_name():
	    self.database="local-SPAN512"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return
	elif "FERRA" == event.get_name():
	    self.database="local-FERRA-CC"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return
	elif "Remote SPAN512" == event.get_name():
	    self.database="remote-SPAN512-CC"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return
	elif "Local SPAN512" == event.get_name():
	    self.database="local-test"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return
	elif "SPAN512-CC" == event.get_name():
	    self.database="local-SPAN512-CC"
	    self.Plot.set_dbname(self.database)
	    self.Classification.change_database(self.database)
	    self.Plot.set_Classification(self.Classification)
	    self.Users.set_database(self.database)
	    return


	#self.update_main_plot()    


    def update_main_plot(self):
	self.Plot.dispatch_x_axis(self.Plot.get_xlabel())
	self.Plot.dispatch_y_axis(self.Plot.get_ylabel())
	self.Plot.dispatch_status()
	self.Plot.change_axis=1
	#self.Plot.set_cands(self.cands)
	self.Plot.draw_graph()

    # Quit Function
    def quit(self, widget=None, event=None, data=None):
	# Write commands to save to the database when exiting
	print "menus::quit> ",widget, event, data
	self.Classification.save2db()
	gtk.main_quit();


    def __init__(self, parent=None):

	# Check Args ?
	gtk.Window.__init__(self)
	try:
		self.set_screen(parent.get_screen())
	except AttributeError:
		self.connect('destroy', quit)
	# GD
	self.connect('delete-event', self.quit)
	self.set_title("Presto Hunter")
	#self.fullscreen()
	self.set_size_request(800,600)
	self.set_border_width(0)



	entries = (
	  ( "FileMenu", None, "File" ),               # name, stock id, label
	  ( "Save", gtk.STOCK_SAVE, "_Save","<control>S", "Save  file", self.menu_activate_action ),
	  ( "SaveAs", gtk.STOCK_SAVE, "Save _As...","<control>A", "Save to a file", self.menu_activate_action ),
	  ( "Quit", gtk.STOCK_QUIT, "_Quit", "<control>Q", "Quit", self.quit),

	  ( "PreferencesMenu", None, "Preferences" ), # name, stock id, label
	  ( "Review", None, "_Review", "<control>R", "Blood", self.menu_review ), 
	  ( "Mode", None, "_Mode"  ),
	  ( "X-Axis", None, "_X-Axis"  ),
	  ( "Y-Axis", None, "_Y-Axis"  ),
	  ( "Limits", None, "_Limits"  ),
	  ( "Set Limits", None, "_Set Limits", "<control>I", "Blood", self.menu_set_limits ), 

	  ( "DatabaseMenu", None, "Database" ), # name, stock id, label
	  ( "User", None, "_User"  ),
	  ( "Connect", None, "_Connect"  ),
	  #( "Load Known PSRs", None, "Load PSRs","<control>K", "Load Known PSRs", self.menu_load_known_psrs ),
	  ( "Query", None, "Query","<control>Y", "Query the database", self.menu_mysqlquery ),

	  ( "HelpMenu", None, "Help" ),               # name, stock id, label
	  ( "About", None, "_About", "<control>H", "About", self.menu_activate_action ),
	)

	( FOURIER, SP, ) = range(2)
	mode_entries = (
	  ( "Fourier", None, "_Fourier", "<control>N", "Blood", FOURIER ),
	  ( "SinglePulse", None, "Single_Pulse", "<control>P", "Grass", SP ),
	)

	( X_PERIOD, X_FREQ, X_MJD, X_DM, X_AI_SCORE, X_ID) = range(6)
	x_entries = (
	  ( "Period", None, "_Period", "<control>P", "Blood", X_PERIOD ),
	  ( "Frequency", None, "_Frequency", "<control>F", "Blood", X_FREQ ),
	  ( "MJD", None, "_MJD", "<control>M", "Blood", X_MJD ),
	  ( "DM", None, "_DM", "<control>D", "Grass", X_DM ),
	  ( "AI X", None, "_AI Score", None, "Grass", X_AI_SCORE ),
	  ( "ID", None, "_ID", None, "Grass", X_ID ),
	)

	( GREGORY, ISMAEL, KUO, GUEST1, DAVID, FRANCK ) = range(6)
	user_entries = (
	  ( "Gregory", None, "_Gregory", None, "Blood", GREGORY ),
	  ( "Ismael", None, "_Ismael", None, "Grass", ISMAEL ),
	  ( "Kuo", None, "_Kuo", None, "Grass", KUO ),
	  ( "Franca", None, "_Franca", None, "Grass", GUEST1 ),
	  ( "David", None, "_David", None, "Grass", DAVID ),
	  ( "Franck", None, "_Franck", None, "Grass", FRANCK ),
	)

	( SPAN512, SPAN512_CC, FERRA, rSPAN512, lSPAN512, PALFA, NBPP, ) = range(7)
	connect_entries = (
	  ( "SPAN512", None, "SPAN512", None, "Grass", SPAN512 ),
	  ( "SPAN512-CC", None, "SPAN512-CC", None, "Grass", SPAN512_CC ),
	  ( "FERRA", None, "FERRA", None, "Grass", FERRA ),
	  ( "Remote SPAN512", None, "Remote SPAN512", None, "Grass", rSPAN512 ),
	  ( "Local SPAN512", None, "Local SPAN512", None, "Grass", lSPAN512 ),
	  ( "PALFA", None, "PALFA", None, "Blood", PALFA ),
	  ( "NBPP", None, "NBPP", None, "Grass", NBPP ),
	)

	( Y_SIGMA, Y_SNR, Y_COH, Y_SCORE, Y_AI_SCORE) = range(5)
	y_entries = (
	  ( "Sigma", None, "_Sigma", "<control>W", "Blood", Y_SIGMA ),
	  ( "SNR", None, "_SNR", "<control>X", "Grass", Y_SNR ),
	  ( "Coherent Pow", None, "_Coherent Pow", "<control>C", "Grass", Y_COH ),
	  ( "Score", None, "_Score", "<control>O", "Grass", Y_SCORE ),
	  ( "AI Y", None, "_AI Score", "<control>A", "Grass", Y_AI_SCORE ),
	)

	limits_entries = (
	  ( "Use Limits", gtk.STOCK_BOLD, "_Use Limits", "<control>J", "Use Limits",  self.menu_activate_limits, False),
	)

	ui_info = \
	'''<ui>
	  <menubar name='MenuBar'>
	    <menu action='FileMenu'>
	      <menuitem action='Save'/>
	      <menuitem action='SaveAs'/>
	      <separator/>
	      <menuitem action='Quit'/>
	    </menu>
	    <menu action='PreferencesMenu'>
	      <menuitem action='Review'/>
	      <menu action='Mode'>
		<menuitem action='Fourier'/>
		<menuitem action='SinglePulse'/>
	      </menu>
	      <menu action='X-Axis'>
		<menuitem action='Period'/>
		<menuitem action='Frequency'/>
		<menuitem action='MJD'/>
		<menuitem action='DM'/>
		<menuitem action='AI X'/>
		<menuitem action='ID'/>
	      </menu>
	      <menu action='Y-Axis'>
		<menuitem action='Sigma'/>
		<menuitem action='SNR'/>
		<menuitem action='Coherent Pow'/>
		<menuitem action='Score'/>
		<menuitem action='AI Y'/>
	      </menu>
	      <menu action='Limits'>
		<menuitem action='Set Limits'/>
		<menuitem action='Use Limits'/>
	      </menu>
	    </menu>
	    <menu action='DatabaseMenu'>
	      <menu action='User'>
		<menuitem action='Gregory'/>
		<menuitem action='Ismael'/>
		<menuitem action='Kuo'/>
		<menuitem action='Franca'/>
		<menuitem action='David'/>
		<menuitem action='Franck'/>
	      </menu>
	      <menu action='Connect'>
		<menuitem action='SPAN512'/>
		<menuitem action='SPAN512-CC'/>
		<menuitem action='FERRA'/>
		<menuitem action='Remote SPAN512'/>
		<menuitem action='Local SPAN512'/>
		<menuitem action='PALFA'/>
		<menuitem action='NBPP'/>
	      </menu>
	      <menuitem action='Query'/>
	    </menu>
	    <menu action='HelpMenu'>
	      <menuitem action='About'/>
	    </menu>
	  </menubar>
	</ui>'''

	"""
	  <toolbar  name='ToolBar'>
	    <toolitem action='Quit'/>
	    <separator action='Sep1'/>
	  </toolbar>
	"""  


	# Variables Init
	self.list_plotted=[]
	self.cur_cand=0
	self.show_bad_beams=True
	self.mode = "Fourier"

	self.database = "local-SPAN512"

	self.actions = gtk.ActionGroup("Actions")
	self.actions.add_actions(entries,self)
	self.actions.add_radio_actions(mode_entries, FOURIER, self.radio_action)
	self.actions.add_radio_actions(x_entries, X_FREQ, self.radio_action)
	self.actions.add_radio_actions(y_entries, Y_SIGMA, self.radio_action)
	# Enforce that the stage user is the default user
	if getpass.getuser()=='stage':
	    self.actions.add_radio_actions(user_entries, GUEST1, self.radio_action)
	else:
	    self.actions.add_radio_actions(user_entries, GREGORY, self.radio_action)
	self.actions.add_radio_actions(connect_entries, SPAN512, self.radio_action)
	self.actions.add_toggle_actions(limits_entries,self)

	ui = gtk.UIManager()
	ui.insert_action_group(self.actions, 0)
	self.add_accel_group(ui.get_accel_group())

	try:
		mergeid = ui.add_ui_from_string(ui_info)
	except gobject.GError, msg:
		print "building menus failed: %s" % msg

	box1 = gtk.VBox(False, 0)
	self.add(box1)
	box1.pack_start(ui.get_widget("/MenuBar"), False, False, 0)


	# Init the system with Fourier candidates	
	self.cands = candidate.Candidates()
	#self.cands.set_mode(self.mode)

	# Init the main graph
	self.Plot = plot.Plot()
	self.Plot.set_dbname(self.database)

	#self.Plot.set_mode(self.mode)
	# Init Users
	if getpass.getuser()=='stage':
	    self.Users = users.Users("G1", self.Plot.get_dbname()) # Default value
	else:    
	    self.Users = users.Users("GD", self.Plot.get_dbname()) # Default value
	
	# Init the classification
	self.Classification = classification.Classification(self.Users, self.Plot.get_dbname())
	
	# Init limits
	self.Limits = limits.Limits()

	# Init known psrs
	self.Known_psrs = known_psrs.PSR_list()
	self.Known_psrs.load_known_psrs()

	# Init the main graph
	#self.Plot = plot.Plot()
	#self.Plot.set_mode(self.mode)
	self.Plot.set_Classification(self.Classification)
	self.Plot.set_Known_psrs(self.Known_psrs)
	self.Plot.set_limits(self.Limits)


	self.Plot.set_canvas( FigureCanvas(self.Plot.get_fig()) )
	box1.pack_start(self.Plot.canvas)
	toolbar = NavigationToolbar(self.Plot.canvas, self)
	box1.pack_start(toolbar, False, False)

	# Event handling 
	self.Plot.canvas.mpl_connect('pick_event', self.Plot.onpick)
	self.Plot.canvas.mpl_connect('key_press_event', self.Plot.key_press)
	self.Plot.canvas.mpl_connect('button_press_event', self.Plot.onpress)

	# Automatic backup
	#backup = gobject.timeout_add(120000,savefile)
	#backup = gobject.timeout_add(120000,savefile,".cand_list.dat.bck",self.list,self.nb_beams,self.nb_cands,self.nb_sp_list,self.sp_status_list)

	self.show_all()
