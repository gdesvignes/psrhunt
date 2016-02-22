#!/usr/bin/env python

import config
import database as db

class Classification:
    """
    """
    def __init__(self, Users, database, mode='Fourier'):
	self.queries = []
	self.Users = Users
	self.database = database
	self.mode = mode

    def __str__(self):
        for i, line in enumerate(self.queries):
	    print "classification> query %d: ", line

    def reobs_cand(selfi, cand):

	cand = self.candidates.get_cand()

	query = "INSERT IGNORE INTO Reobservations (pdm_cand_id, date, \
	    person_id) VALUES (%d, NOW(), %d)" % (cand.cand_id, self.Users.get_user_id())
	print query
	self.queries.append(query)

	

    def change_user(self, Users):	
        if config.VERBOSE:
	    print "classification::change_user> Change user to ", Users.get_username()
        self.save2db()
        self.User = Users

    def change_database(self, database):	
        if config.VERBOSE:
	    print "classification::change_database> Change database to ", database
        self.save2db()
        self.database = database

    def set_mode(self, mode):	
        self.mode = mode

    def write_classification(self, cand):
     
	class_type_id = 1
	query = ""

	if self.mode=='Fourier':
	    if self.database=='local-SPAN512' or self.database=='remote-SPAN512' or self.database=='local-test':
	        query = "REPLACE INTO pdm_classifications (pdm_cand_id, who, pdm_class_type_id, date, rank) VALUES (%s, '%s', %s, NOW(), %s);\n"%(cand.cand_id, self.Users.get_user(), class_type_id, cand.status)
	    elif self.database=='local-SPAN512-CC' or self.database=='local-FERRA-CC' or self.database=='remote-SPAN512-CC': 
	        #query = "REPLACE INTO PDM_Classifications (pdm_cand_id, person_id, pdm_class_type_id, date, rank) VALUES (%s, '%s', '%s', NOW(), %s);\n"%(cand.cand_id, self.Users.get_user_id(), class_type_id, cand.status)
	        query = "INSERT INTO PDM_Classifications \
		(pdm_cand_id, person_id, pdm_class_type_id, date, rank) VALUES \
		(%s, '%s', '%s', NOW(), %s) ON DUPLICATE KEY UPDATE \
		rank=VALUES(rank), date=NOW();\n"% \
		(cand.cand_id, self.Users.get_user_id(), class_type_id, cand.status)
	    else:
	        raise ClassificationError("classification::write_classification> database %s not implemented for mode=%s"%(self.database, self.mode))
	
	elif self.mode=='SinglePulse':
	    if self.database=='local-SPAN512-CC' or self.database=='local-FERRA-CC':
	        query = "REPLACE INTO SP_Classifications (sp_cand_id, person_id, sp_class_type_id, date, rank) VALUES (%s, '%s', '%s', NOW(), %s);\n"%(cand.header_id, self.Users.get_user_id(), class_type_id, cand.status)
		#print query
	    else:
	        raise ClassificationError("classification::write_classification> database %s not implemented for mode=%s"%(self.database, self.mode))

	else:
	    print "classification::write_classification> mode=%s not implemented"%(self.mode)
	    raise

	#if config.VERBOSE:
	#    print "classification::write_classification> ", query 
	if query:    
	    self.queries.append(query)

    def save2db(self):
	if not len(self.queries):
	    if config.VERBOSE:
	        print "classification::save2db> No classification to save"
	    return
	# Connect to DB
	self.db = db.Database(self.database)
	self.DBconn = self.db.conn
	self.DBcursor = self.db.cursor

	# Execute queries Assume connection to DB
	print "Writing classification into database %s"%self.database
	for query in self.queries:
	    #print "Execute :", query
	    self.DBcursor.execute(query)

	# Close connection
	self.DBconn.close()
	self.queries = []

