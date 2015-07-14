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
		"ID" INT,
		"TID" NVARCHAR(4) CS_STRING,
		"NAME" NVARCHAR(128) CS_STRING,
		UNIQUE ("ID"),
		UNIQUE ("TID")
	)"""
	__createIfNotExists(cursor, sql)

	# Create Table SEMANTIC_TYPE_RELATIONS
	sql = """
	CREATE ROW TABLE "UMLS"."SEMANTIC_TYPE_RELATIONS" (
		"TYPE1_ID" INT,
		"REL_ID" INT,
		"TYPE2_ID" INT,
		UNIQUE ("TYPE1_ID", "REL_ID", "TYPE2_ID")
	)
	"""
	__createIfNotExists(cursor, sql)

	# Create Table SEMANTIC_GROUPS
	sql = """
	CREATE ROW TABLE "UMLS"."SEMANTIC_GROUPS" (
		"ID" INT,
		"KEY" NVARCHAR(4) CS_STRING,
		"NAME" NVARCHAR(64) CS_STRING,
		"TYPE_ID" INT,
		UNIQUE ("ID", "TYPE_ID"),
		UNIQUE ("KEY", "TYPE_ID")
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
	for tid_str, name in sorted(types, key=lambda x: x[0]):
		tid_int = int(tid_str[1:])
		sql = 'INSERT INTO %s VALUES (%d, \'%s\', \'%s\')' % (table, tid_int, tid_str, name)
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

	for relation in relations:
		# crop the beginning 'T' from the id
		values = [s[1:] for s in relation]

		statement = 'INSERT INTO %s VALUES (%s)' % (table, ','.join(values))
		cursor.execute(statement)

	# cursor.execute('MERGE DELTA OF %s' % (table))


def readSemanticGroups(cursor, path, table):
	print " * Semantic Groups"

	print "   * Truncating..."
	cursor.execute('TRUNCATE TABLE %s' % (table))

	print "   * Reading groups from %s..." % (path)
	groups = []
	group_keys = {}
	with open(path, 'r') as f:
		reg = re.compile(r'([^>]+)\|(.+)\|(.+)\|(.+)')

		for line in f.readlines():
			match = reg.search(line)
			if match:
				group = match.groups()
				groups.append(group)

				if group[0] not in group_keys:
					group_keys[group[0]] = len(group_keys)



	print "   * Inserting groups into %s..." % (table)
	for group in groups:
		row = [
			str(group_keys[group[0]]),
			"'" + group[0] + "'",
			"'" + group[1] + "'",
			group[2][1:] # cropped TID
		]
		statement = 'INSERT INTO %s VALUES (%s)' % (table, ','.join(row))
		cursor.execute(statement)

	# cursor.execute('MERGE DELTA OF %s' % (table))