import os


def executeSQL(connection, sql):
	cursor = connection.cursor()
	try:
		cursor.execute(sql)
	except Exception, e:
		print sql
		raise e
	
	connection.commit()


def createSynonymTable(connection, tablename):
	sql = 'CREATE COLUMN TABLE %s (\
		"NORMALIZED" NVARCHAR(512) CS_STRING,\
		"SYNONYM" NVARCHAR(512) CS_STRING\
	)' % (tablename)

	executeSQL(connection, sql)


def truncateTable(connection, tablename):
	sql = 'TRUNCATE TABLE %s' % (tablename)
	executeSQL(connection, sql)

def dropTable(connection, tablename):
	sql = 'DROP TABLE %s' % (tablename)
	try:
		executeSQL(connection, sql)
	except Exception, e:
		print e
		# TODO: Check if correct exception was thrown
		pass
	
def mergeDelta(connection, tablename):
	sql = 'MERGE DELTA OF %s' % (tablename)
	executeSQL(connection, sql)




"""
[CONTROL FILE]
IMPORT DATA
INTO TABLE S0004108322.USERS
FROM '/dropbox/S0004108322/USERS.CSV'
FIELDS DELIMITED BY ';'
OPTIONALLY ENCLOSED BY '"'
ERROR LOG '/dropbox/S0004108322/USERS.ERR'

[SQL]
IMPORT FROM <control_file>
 [WITH [THREADS <thread_num>] [BATCH <batch_size>]]
 [WITH TABLE LOCK [WITHOUT TYPE CHECK]]
"""
def createCSVImportControlFile(control_path, table, csv_path):
	error_log = "%s.err" % (os.path.abspath(control_path))
	
	fh = open(control_path, 'w')
	fh.write("IMPORT DATA\n")
	fh.write("INTO TABLE %s\n" % (table))
	fh.write("FROM '%s'\n" % (os.path.abspath(csv_path)))
	fh.write("FIELDS DELIMITED BY ';'\n")
	fh.write("OPTIONALLY ENCLOSED BY '\"'\n")
	fh.write("ERROR LOG '%s'\n" % (error_log))
	fh.close()

	# Create an empty error Log
	fh = open(error_log, 'a')
	fh.close()
