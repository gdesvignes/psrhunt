import database as db

class Users:
    """
    """
    def __init__(self, user, database):
        self.user = user
	self.database = database
	self.lookup = {'GD': 'desvignes', 'IC': 'cognard', 'KL': 'kliu', 'G1': 'guest1', 'DS': 'dsmith', 'FO': 'foctau'}

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def get_username(self):
        return self.lookup[self.user]

    def set_database(self, database):
        self.database = database

    def get_user_id(self):
        # Connect to DB
	Db = db.Database(self.database)
	DBconn = Db.conn
	DBcursor = Db.cursor

	query = "SELECT person_id FROM auth_user WHERE username='%s'"%(self.lookup[self.user])
	DBcursor.execute(query)

	user_id = DBcursor.fetchone()[0]

	# Close connection
	DBconn.close()

	return user_id
