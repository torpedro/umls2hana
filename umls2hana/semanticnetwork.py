import re
import sqlhelper as sql

def __createIfNotExists(cursor, sql):
	try:
		cursor.execute(sql)
	except Exception, e:
		s = str(e)
		if 'duplicate' in s:
			return False
		else:
			raise e
	return True

def createUMLSSchemaAndTables(connection):
	cursor = connection.cursor()

	# Create tht SCHEMA
	sql = 'CREATE SCHEMA "UMLS"'
	__createIfNotExists(cursor, sql)

	# Create Table SEMANTIC_TYPES
	sql = """
	CREATE ROW TABLE "UMLS"."SEMANTIC_TYPES" (
		"TID" NVARCHAR(4) CS_STRING,
		"NAME" NVARCHAR(128) CS_STRING,
		UNIQUE ("TID")
	)"""
	__createIfNotExists(cursor, sql)

	# Create Table SEMANTIC_TYPE_RELATIONS
	sql = """
	CREATE ROW TABLE "UMLS"."SEMANTIC_TYPE_RELATIONS" (
		"TYPE1" NVARCHAR(4) CS_STRING,
		"REL" NVARCHAR(4) CS_STRING,
		"TYPE2" NVARCHAR(4) CS_STRING,
		UNIQUE ("TYPE1", "REL", "TYPE2")
	)
	"""
	__createIfNotExists(cursor, sql)

	# Create Table SEMANTIC_GROUPS
	sql = """
	CREATE ROW TABLE "UMLS"."SEMANTIC_GROUPS" (
		"GROUP_KEY" NVARCHAR(4) CS_STRING,
		"GROUP_NAME" NVARCHAR(64) CS_STRING,
		"TID" NVARCHAR(4) CS_STRING,
		UNIQUE ("GROUP_KEY", "GROUP_NAME", "TID")
	)
	"""
	__createIfNotExists(cursor, sql)

	connection.commit()



def readSemanticTypes(cursor, path, table):
	print " * Semantic Types"

	print "   * Truncating..."
	cursor.execute('TRUNCATE TABLE %s' % (table))

	print "   * Reading types from %s..." % (path)
	types = []
	with open(path, 'r') as fh:
		for line in fh:
			typ = line.split('|')
			types.append((typ[1], typ[2]))

	print "   * Inserting types into %s..." % (table)
	for tid, name in sorted(types, key=lambda x: x[0]):
		sql = 'INSERT INTO %s VALUES (\'%s\', \'%s\')' % (table, tid, name)
		cursor.execute(sql);

	# cursor.execute('MERGE DELTA OF %s' % (table))



def readSemanticRelations(cursor, path, table):
	print " * Semantic Relations"

	print "   * Truncating..."
	cursor.execute('TRUNCATE TABLE %s' % (table))

	print "   * Reading relations from %s..." % (path)
	relations = []
	with open(path, 'r') as f:
		reg = re.compile(r'([^>]+)\|(.+)\|(.+)\|')

		for line in f.readlines():
			match = reg.search(line)
			if match:
				relations.append(match.groups())

	print "   * Inserting relations into %s..." % (table)

	for rel in relations:
		values = ["'" + s + "'" for s in rel]
		statement = 'INSERT INTO %s VALUES (%s)' % (table, ','.join(values))
		cursor.execute(statement)

	# cursor.execute('MERGE DELTA OF %s' % (table))


def readSemanticGroups(cursor, path, table):
	print " * Semantic Groups"

	print "   * Truncating..."
	cursor.execute('TRUNCATE TABLE %s' % (table))

	print "   * Reading groups from %s..." % (path)
	groups = []
	with open(path, 'r') as f:
		reg = re.compile(r'([^>]+)\|(.+)\|(.+)\|')

		for line in f.readlines():
			match = reg.search(line)
			if match:
				groups.append(match.groups())

	print "   * Inserting groups into %s..." % (table)

	for grp in groups:
		values = ["'" + s + "'" for s in grp]
		statement = 'INSERT INTO %s VALUES (%s)' % (table, ','.join(values))
		cursor.execute(statement)

	# cursor.execute('MERGE DELTA OF %s' % (table))