import re


def readSemanticTypes(cursor, path, table):
	print " * Semantic Types"

	print "   * Truncating..."
	cursor.execute('TRUNCATE TABLE %s' % (table))

	print "   * Read types from %s..." % (path)
	types = []
	with open(path, 'r') as fh:
		for line in fh:
			typ = line.split('|')
			types.append((typ[1], typ[2]))

	print "   * Insert types into %s..." % (table)
	for tid, name in sorted(types, key=lambda x: x[0]):
		sql = 'INSERT INTO %s VALUES (\'%s\', \'%s\')' % (table, tid, name)
		cursor.execute(sql);



def readSemanticRelations(cursor, path, table):
	print " * Semantic Relations"

	print "   * Truncating..."
	cursor.execute('TRUNCATE TABLE %s' % (table))

	print "   * Read relations from %s..." % (path)
	relations = []
	with open(path, 'r') as f:
		reg = re.compile(r'([^>]+)\|(.+)\|(.+)\|')

		for line in f.readlines():
			match = reg.search(line)
			if match:
				relations.append(match.groups())

	print "   * Insert relations into %s..." % (table)

	for rel in relations:
		values = ["'" + s + "'" for s in rel]
		statement = 'INSERT INTO %s VALUES (%s)' % (table, ','.join(values))
		cursor.execute(statement)


