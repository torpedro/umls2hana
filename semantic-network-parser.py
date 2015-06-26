#!/usr/bin/python
import sys
import os
import re
import getpass
from optparse import OptionParser
import pyhdb


"""
CREATE SCHEMA "UMLS";

CREATE ROW TABLE "UMLS"."SEMANTIC_TYPES" (
	"TID" NVARCHAR(4) CS_STRING,
	"NAME" NVARCHAR(128) CS_STRING,
	UNIQUE ("TID")
);

CREATE ROW TABLE "UMLS"."SEMANTIC_TYPE_RELATIONS" (
	"TYPE1" NVARCHAR(4) CS_STRING,
	"REL" NVARCHAR(4) CS_STRING,
	"TYPE2" NVARCHAR(4) CS_STRING,
	UNIQUE ("TYPE1", "REL", "TYPE2")
);
"""



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

	print "   * Read relations from %s..." % (relation_file)
	relations = []
	with open(relation_file, 'r') as f:
		reg = re.compile(r'([^>]+)\|(.+)\|(.+)\|')

		for line in f.readlines():
			match = reg.search(line)
			if match:
				relations.append(match.groups())

	print "   * Insert relations into %s..." % (relation_table)

	for rel in relations:
		values = ["'" + s + "'" for s in rel]
		statement = 'INSERT INTO %s VALUES (%s)' % (relation_table, ','.join(values))
		cursor.execute(statement)





if __name__ == '__main__':
	print ""
	usage = "usage: %prog [options] input_path"
	parser = OptionParser(usage=usage)
	parser.add_option("-s", "--server", dest="server", default="localhost", help="Address of the HANA server")
	parser.add_option("-p", "--port", dest="port", default="30015")
	parser.add_option("-u", "--user", dest="user", default="SYSTEM")
	# parser.add_option("-o", "--out", dest="out")
	(options, args) = parser.parse_args()

	if len(args) < 1:
		parser.error("Not enough arguments given!")


	path = args[0]
	output_schema = 'UMLS'

	####################################
	### Configuration
	server = options.server
	port = int(options.port)
	user = options.user

	type_table = '"UMLS"."SEMANTIC_TYPES"'
	relation_table = '"UMLS"."SEMANTIC_TYPE_RELATIONS"'

	type_file = os.path.join(path, 'SRDEF.html')
	relation_file = os.path.join(path, 'SRSTRE1.html')



	##################################
	##################################
	##################################
	print " * What is the password for your HANA user? (User: %s)" % (user)
	password = getpass.getpass()


	##################################
	##################################
	##################################
	print " * Opening connection to HANA..."
	try:
		connection = pyhdb.connect(
			host=server,
			port=port,
			user=user,
			password=password
		)
		cursor = connection.cursor()

	except pyhdb.exceptions.DatabaseError, e:
		print '[Error] invalid username or password'
		sys.exit(-1)



	readSemanticTypes(cursor, type_file, type_table)
	readSemanticRelations(cursor, relation_file, relation_table)


		
	connection.commit()
	connection.close()
	print " * Done"



