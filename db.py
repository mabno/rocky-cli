from pysqlcipher3 import dbapi2 as sqlite3

def error_handler(func):
	def inner(*args):
		try:
			return func(*args)
		except Exception as e:
			return e
	return inner

class Database:
	@error_handler
	def connect(self, file, key):
		self.connection = sqlite3.connect(file)
		self.cursor = self.connection.cursor()
		self.cursor.execute("PRAGMA key='{}'".format(key))
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS accounts
			(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			service TEXT NOT NULL,
			email TEXT NOT NULL,
			username TEXT NOT NULL,
			password TEXT NOT NULL,
			updated NUMERIC,
			created NUMERIC
			)
			""")
		self.connection.commit()

	@error_handler
	def create(self, values):
		self.cursor.execute("""INSERT INTO accounts(service, email, username, password, updated, created)
			VALUES (?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))
		""", (values[0], values[1], values[2], values[3]))
		self.connection.commit()

	@error_handler
	def update(self, id, values):
		result = self.cursor.execute(
		"""
			UPDATE accounts
			SET
			service=COALESCE(?,accounts.service),
			email=COALESCE(?,accounts.email),
			username=COALESCE(?,accounts.username),
			password=COALESCE(?,accounts.password),
			updated=datetime('now', 'localtime')
			WHERE id=?
		""", (values[0], values[1], values[2], values[3], id))
		self.connection.commit()
		return result.rowcount

	@error_handler
	def get_all(self):
		result = self.cursor.execute("SELECT * FROM accounts")
		return result.fetchall()

	@error_handler
	def get_one(self, id):
		result = self.cursor.execute("SELECT * FROM accounts WHERE id=?", (id,))
		return result.fetchall()

	@error_handler
	def search(self, text):
		result = self.cursor.execute("SELECT * FROM accounts WHERE service LIKE ?", ('%'+text+'%',))
		return result.fetchall()

	@error_handler
	def delete(self, id):
		result = self.cursor.execute(f'DELETE FROM accounts WHERE id IN ({",".join("?"*len(id))})', id)
		self.connection.commit()
		return result.rowcount

