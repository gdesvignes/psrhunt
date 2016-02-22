import gtk

import candidate
import database

class Query:

    def __init__(self, database, user):
	self.database = database
        self.user = user
	#self.is_SPAN = False

    """
    def is_SPAN_callback(self, widget, data=None):
	print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
	if widget.get_active():
	    if data == 'SPAN':
		self.is_SPAN = True
	else:
	    if data == 'SPAN':
		self.is_SPAN = False
    """


    def query_cands(self):

	# First connect
	db = database.Database(db = self.database)
	DBconn = db.conn
	DBcursor = db.cursor
	print "Connected to %s"%self.database

	# Read the number of available beams
	if self.database=='local-SPAN512-CC' or self.database=='local-FERRA-CC' or self.database=='remote-SPAN512-CC':
	    query = "SELECT count(*) FROM Headers"
	else:
	    query = "SELECT count(*) FROM headers"
	DBcursor.execute(query)
	nb_beams = DBcursor.fetchone()[0]	    

	print "%s available beams in the database %s"%(nb_beams, self.database)

	# Create the GTK dialog box
	dialog = gtk.Dialog("Query", None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK, "_Cancel", 
    gtk.RESPONSE_CANCEL))

	vbox = gtk.VBox(False, 8)
	vbox.set_border_width(8)
	dialog.vbox.pack_start(vbox, False, False, 0)

	label = gtk.Label()
	label.set_markup("%s beams available at %s"%(nb_beams, self.database))
	vbox.pack_start(label, False, False, 0)

	table = gtk.Table(3,2)
	table.set_row_spacings(4)
	table.set_col_spacings(4)
	vbox.pack_start(table, True, True, 0)

	label = gtk.Label("Beam Id")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 0, 1)
	local_entry1 = gtk.Entry()
	local_entry1.set_text("")
	table.attach(local_entry1, 1, 2, 0, 1)
	label.set_mnemonic_widget(local_entry1)
	local_entry1b = gtk.Entry()
	local_entry1b.set_text("")
	table.attach(local_entry1b, 2, 3, 0, 1)
	label.set_mnemonic_widget(local_entry1b)

	label = gtk.Label("SRV Id")
	label.set_use_underline(True)
	table.attach(label, 0, 1, 1, 2)
	local_entry2b = gtk.Entry()
	local_entry2b.set_text("")
	table.attach(local_entry2b, 2, 3, 1, 2)
	label.set_mnemonic_widget(local_entry2b)

	# is_SPAN button
	"""
	is_SPAN_but = gtk.CheckButton("Remove non-SPAN512 beams")
        is_SPAN_but.connect('toggled', self.is_SPAN_callback, "SPAN")
        if self.is_SPAN:
            is_SPAN_but.set_active(True)
	table.attach(is_SPAN_but, 1, 2, 1, 2)
	"""

	dialog.show_all()
	response = dialog.run()


	beam_id_min = 0
	beam_id_max = 99999999


	# Read values when clicking OK
	if response == gtk.RESPONSE_OK:
	    beam_id_min   = local_entry1.get_text()
	    beam_id_max   = local_entry1b.get_text()

	    try:
		srv     = int(local_entry2b.get_text())
	    except: srv=None	    

	    if srv:
		print "Select SRV%06d"%srv
	    else:
		print "beam  selected : %d - %d"%(int(beam_id_min),int(beam_id_max))
	    #print "other    : %d %d"%(int(other_min),int(other_max))
	    dialog.destroy()

	elif response == gtk.RESPONSE_CANCEL:

	    dialog.destroy()

	    # Close connection
	    DBconn.close()

	    return None
	    
	print "User              :", self.user.get_username()
	print "Database selected :", self.database

	if self.database=='local-PALFA':
	    query = "SELECT H.orig_right_ascension, H.orig_declination, C.pdm_cand_id,\
	    C.header_id, C.period, C.dm, C.snr, C.coherent_power, C.num_hits,\
	    C.num_harmonics, C.presto_sigma, P.path, P.filename, N.rank FROM headers AS\
	    H INNER JOIN pdm_candidates AS C ON H.header_id = C.header_id INNER JOIN\
	    pdm_plot_pointers AS P ON C.pdm_cand_id = P.pdm_cand_id LEFT JOIN pdm_classifications \
	    AS N ON C.pdm_cand_id = N.pdm_cand_id"

	elif self.database=='local-NBPP':
	    query = "SELECT H.right_ascension, H.declination, C.pdm_cand_id,\
	    C.header_id, C.period_topo, C.dm, C.snr, C.coherent_power, C.num_hits,\
	    C.num_harmonics, C.presto_sigma, P.path, P.ps_filename, N.rank, C.lkj1 FROM headers AS\
	    H INNER JOIN pdm_candidates AS C ON H.header_id = C.header_id INNER JOIN\
	    pdm_plot_pointers AS P ON C.pdm_cand_id = P.pdm_cand_id LEFT JOIN pdm_classifications AS \
	    N ON C.pdm_cand_id = N.pdm_cand_id"

	elif self.database=='local-SPAN512' or self.database=='remote-SPAN512' or self.database=='local-test':
	    query = "SELECT H.right_ascension, H.declination, C.pdm_cand_id,\
	    C.header_id, C.period_topo, C.dm, C.snr, C.coherent_power, C.num_hits,\
	    C.num_harmonics, C.presto_sigma, P.path, P.ps_filename, N.rank, C.lkj1 FROM headers AS\
	    H INNER JOIN pdm_candidates AS C ON H.header_id = C.header_id INNER JOIN\
	    pdm_plot_pointers AS P ON C.pdm_cand_id = P.pdm_cand_id LEFT JOIN pdm_classifications AS N \
	    ON C.pdm_cand_id = N.pdm_cand_id AND N.who='%s'"%self.user.get_user()
	    cand_type_id = 1
	elif self.database=='local-SPAN512-CC' or self.database=='local-FERRA-CC' or self.database=='remote-SPAN512-CC':
	    DBcursor.execute("SELECT person_id FROM auth_user WHERE username='%s'"%self.user.get_username())
	    person_id = DBcursor.fetchone()[0]
	    query = "SELECT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period*1000., \
	 C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, NULL, NULL, N.rank, R19.value, R20.value \
	 FROM PDM_Candidates AS C \
	 LEFT JOIN Headers AS H USING(header_id) \
	 LEFT JOIN PDM_Classifications AS N ON C.pdm_cand_id=N.pdm_cand_id AND N.person_id=%s \
	 LEFT JOIN pdm_rating AS R19 ON C.pdm_cand_id=R19.pdm_cand_id AND R19.pdm_rating_instance_id=19 \
	 LEFT JOIN pdm_rating AS R20 ON C.pdm_cand_id=R20.pdm_cand_id AND R20.pdm_rating_instance_id=20 "%person_id

            query = "SELECT H.right_ascension, H.declination, C.pdm_cand_id, C.header_id, C.period*1000., \
         C.dm, C.snr, C.coherent_power, C.num_hits, C.num_harmonics, C.presto_sigma, NULL, NULL, \
         N.rank, R19.value, R20.value, H.timestamp_mjd, D.diagnostic_value, G.is_SPAN \
	 FROM PDM_Candidates AS C \
         LEFT JOIN Headers AS H USING(header_id) \
         LEFT JOIN PDM_Classifications AS N ON C.pdm_cand_id=N.pdm_cand_id AND N.person_id=%s \
         LEFT JOIN pdm_rating AS R19 ON C.pdm_cand_id=R19.pdm_cand_id AND R19.pdm_rating_instance_id=19 \
         LEFT JOIN pdm_rating AS R20 ON C.pdm_cand_id=R20.pdm_cand_id AND R20.pdm_rating_instance_id=20 \
         LEFT JOIN Diagnostics AS D ON C.header_id=D.header_id AND D.diagnostic_type_id=1 \
	 LEFT JOIN SBON512.processing AS P ON P.pointing_name=H.source_name \
	 LEFT JOIN SBON512.NRT_grid AS G ON G.grid_id=P.grid_id "%person_id
	    cand_type_id = 2

	"""
	if self.is_SPAN:
	    condition = " LEFT JOIN SBON512.processing AS P ON P.pointing_name=H.source_name \
		LEFT JOIN SBON512.NRT_grid AS G ON G.grid_id=P.grid_id"
	    query = query + condition
	"""


	# Condition 
	if srv:
	    condition = " WHERE H.source_name='SRV%06d'"%(srv)
	else:
	    condition = " WHERE H.header_id BETWEEN %s AND %s"%(beam_id_min, beam_id_max) 
	query = query + condition

	"""
	if self.is_SPAN:
	    condition = " AND G.is_SPAN=True"
	    query = query + condition
	"""



	# Execute query
	print "Query :", query
	DBcursor.execute(query)
	result_query = [list(row) for row in DBcursor.fetchall()]	    

	candidates = candidate.Candidates()
	for cand in result_query:
	    candidates.add_cands(candidate.FourierCand(cand, cand_type_id))
	print "query::query_cands> Loaded %d candidates"%len(candidates)


	# Now query the SP
	sp_candidates = None
	if self.database=='local-SPAN512-CC' or self.database=='local-FERRA-CC':
	    query = "SELECT S.header_id, H.right_ascension, H.declination, S.ftpfilepath, S.filename, C.rank FROM SP_Files_Info AS S LEFT JOIN Headers AS H ON S.header_id=H.header_id LEFT JOIN SP_Classifications as C ON C.sp_cand_id=H.header_id"
	    cand_type_id = 2
	    # Condition 
	    condition = " WHERE sp_files_type_id=3 AND H.header_id BETWEEN %s AND %s"%(beam_id_min, beam_id_max) 
	    if condition:
	        query = query + condition
	    DBcursor.execute(query)
	    result_query = [list(row) for row in DBcursor.fetchall()]	    
	    #print result_query


	    sp_candidates = candidate.Candidates()
	    for cand in result_query:
	        sp_candidates.add_cands(candidate.SPCand(cand, cand_type_id))
	    print "query::query_cands> Loaded %d SP Plots"%len(sp_candidates)

	# Close connection
	DBconn.close()

	return candidates, sp_candidates

