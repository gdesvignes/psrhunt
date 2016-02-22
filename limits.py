import gtk

import config

class Limits:
    def __init__(self):
        self.limits_on = False

	self.dm_min="";self.dm_max=""
	self.snr_min="";self.snr_max=""
	self.score_min="";self.score_max=""
	self.ai_score_min="";self.ai_score_max=""
	self.nharm_min="";self.nharm_max=""
	self.p_min="";self.p_max=""
	self.rfi_max=""

	self.show_all = True

    def __str__(self):
            return \
	    "\nLimits\n" + \
	    "period   : %s - %s\n"%(self.p_min, self.p_max) + \
	    "dm       : %s - %s\n"%(self.dm_min, self.dm_max) + \
	    "snr      : %s - %s\n"%(self.snr_min, self.snr_max) + \
	    "score    : %s - %s\n"%(self.score_min, self.score_max) + \
	    "AI score : %s - %s\n"%(self.ai_score_min, self.ai_score_max) + \
	    "N harm   : %s - %s\n"%(self.nharm_min, self.nharm_max) + \
	    "RFI Per. :     - %s\n"%(self.rfi_max)

    def set_limits_on(self, on):
        self.limits_on = on

    def is_limits_on(self):
        return self.limits_on

    def check_dm(self, dm):
        if self.dm_min and dm < float(self.dm_min):
	    return False
	elif self.dm_max and dm > float(self.dm_max): 
	    return False
	else: return True    

    def check_snr(self, snr):
        if self.snr_min and snr < float(self.snr_min) or self.snr_max and snr > float(self.snr_max): 
	    return False
	return True    

    def check_score(self, score):
        if self.score_min and score < float(self.score_min) or self.score_max and score > float(self.score_max): 
	    return False
	return True    

    def check_ai_score(self, ai_score):
        if self.ai_score_min and ai_score < float(self.ai_score_min) or self.ai_score_max and ai_score > float(self.ai_score_max): 
	    return False
	return True    

    def check_nharm(self, nharm):
        if self.nharm_min and nharm < int(self.nharm_min) or self.nharm_max and nharm > int(self.nharm_max): 
	    return False
	return True    

    def check_period(self, period):
        if self.p_min and period < float(self.p_min) or self.p_max and period > float(self.p_max): 
	    return False
	return True    

    def check_rfi_per(self, rfi_per):
        if self.rfi_max and rfi_per > float(self.rfi_max): 
	    return False
	return True    

    def check_is_SPAN(self, is_SPAN):
        if self.show_all:
	    return True
        elif not self.show_all and is_SPAN: 
	    return True
        elif not self.show_all and not is_SPAN: 
	    return False
	else: return True


    def callback(self, widget, data=None):
	print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
	if widget.get_active():
	    self.show_all = True
	else:
	    self.show_all = False

    def set_limits(self):
	"""
	Set limits to the candidates being displayed. Current options are :
	DM, SNR, Score
	"""

	dialog = gtk.Dialog("Set limits", None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK, "_Cancel", gtk.RESPONSE_CANCEL))

	hbox = gtk.HBox(False, 8)
	hbox.set_border_width(8)
	dialog.vbox.pack_start(hbox, False, False, 0)

	table = gtk.Table(8,3) # gtk.Table(rows=1, columns=1, homogeneous=False)
	table.set_row_spacings(4)
	table.set_col_spacings(4)
	hbox.pack_start(table, True, True, 0)

	label = gtk.Label("DM")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 0, 1) # table.attach(child, left_attach, right_attach, top_attach, bottom_attach, xoptions=EXPAND|FILL, yoptions=EXPAND|FILL, xpadding=0, ypadding=0)
	local_entry1 = gtk.Entry()
	local_entry1.set_text(self.dm_min)
	table.attach(local_entry1, 1, 2, 0, 1)
	label.set_mnemonic_widget(local_entry1)
	local_entry1b = gtk.Entry()
	local_entry1b.set_text(self.dm_max)
	table.attach(local_entry1b, 2, 3, 0, 1)
	label.set_mnemonic_widget(local_entry1b)

	label = gtk.Label("SNR")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 1, 2)
	local_entry2 = gtk.Entry()
	local_entry2.set_text(self.snr_min)
	table.attach(local_entry2, 1, 2, 1, 2)
	label.set_mnemonic_widget(local_entry2)
	local_entry2b = gtk.Entry()
	local_entry2b.set_text(self.snr_max)
	table.attach(local_entry2b, 2, 3, 1, 2)
	label.set_mnemonic_widget(local_entry2b)

	label = gtk.Label("Score")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 2, 3)
	local_entry3 = gtk.Entry()
	local_entry3.set_text(self.score_min)
	table.attach(local_entry3, 1, 2, 2, 3)
	label.set_mnemonic_widget(local_entry3)
	local_entry3b = gtk.Entry()
	local_entry3b.set_text(self.score_max)
	table.attach(local_entry3b, 2, 3, 2, 3)
	label.set_mnemonic_widget(local_entry3b)

	label = gtk.Label("Nb harmonics")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 3, 4)
	local_entry4 = gtk.Entry()
	local_entry4.set_text(self.nharm_min)
	table.attach(local_entry4, 1, 2, 3, 4)
	label.set_mnemonic_widget(local_entry4)
	local_entry4b = gtk.Entry()
	local_entry4b.set_text(self.nharm_max)
	table.attach(local_entry4b, 2, 3, 3, 4)
	label.set_mnemonic_widget(local_entry4b)

	label = gtk.Label("Period (ms)")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 4, 5)
	local_entry5 = gtk.Entry()
	local_entry5.set_text(self.p_min)
	table.attach(local_entry5, 1, 2, 4, 5)
	label.set_mnemonic_widget(local_entry5)
	local_entry5b = gtk.Entry()
	local_entry5b.set_text(self.p_max)
	table.attach(local_entry5b, 2, 3, 4, 5)
	label.set_mnemonic_widget(local_entry5b)

	label = gtk.Label("AI Score")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 5, 6)
	local_entry6 = gtk.Entry()
	local_entry6.set_text(self.ai_score_min)
	table.attach(local_entry6, 1, 2, 5, 6)
	label.set_mnemonic_widget(local_entry6)
	local_entry6b = gtk.Entry()
	local_entry6b.set_text(self.ai_score_max)
	table.attach(local_entry6b, 2, 3, 5, 6)
	label.set_mnemonic_widget(local_entry6b)

	label = gtk.Label("RFI Percentage")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 6, 7)
	local_entry7b = gtk.Entry()
	local_entry7b.set_text(self.rfi_max)
	table.attach(local_entry7b, 2, 3, 6, 7)
	label.set_mnemonic_widget(local_entry7b)

	#label = gtk.Label("Display bad beams")
	#label.set_use_underline(True)
	#table.attach(label, 0, 1, 4, 5)
	print "Creating button: show_all", self.show_all
	span_but = gtk.CheckButton("Show all beams")
	if self.show_all:
	    span_but.set_active(True)
	else:
	    span_but.set_active(False)
	span_but.connect('toggled', self.callback, "SPAN512")
	table.attach(span_but, 1, 2, 7, 8)

	dialog.show_all()
	response = dialog.run()

	# Read values when clicking OK
	if response == gtk.RESPONSE_OK:
	    self.dm_min       = (local_entry1.get_text()); self.dm_max       = (local_entry1b.get_text())
	    self.snr_min      = (local_entry2.get_text()); self.snr_max      = (local_entry2b.get_text())
	    self.score_min    = (local_entry3.get_text()); self.score_max    = (local_entry3b.get_text())
	    self.nharm_min    = (local_entry4.get_text()); self.nharm_max    = (local_entry4b.get_text())
	    self.p_min        = (local_entry5.get_text()); self.p_max        = (local_entry5b.get_text())
	    self.ai_score_min = (local_entry6.get_text()); self.ai_score_max = (local_entry6b.get_text())
	    self.rfi_max = (local_entry7b.get_text())
	    #print self

	dialog.destroy()



    def activate_limits(self, widget, event, data):
	#if config.VERBOSE:
	#    print "limits::activate_limits> In Activate limits", widget, event, data

	# Limits activated
	if widget.get_active():
	    if config.VERBOSE:
		print "limits::activate_limits> Limits are activated"
	    self.limits_on = True
	# Limits not activated            
	else: 
	    self.limits_on = False 

	# Dispatch points following their status and the limits
	#dispatch_status(self)
	#self.draw_graph()
	

