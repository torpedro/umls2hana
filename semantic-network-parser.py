#!/bin/python
from optparse import OptionParser
import sys
import os
import re
import getpass
import pyhdb

from umls2hana.semanticnetwork import *


if __name__ == '__main__':
	usage = "usage: %prog [options] input_folder"
	parser = OptionParser(usage=usage)
	parser.add_option("-s", "--server", dest="server", default="localhost", help="Address of the HANA server")
	parser.add_option("-p", "--port", dest="port", default="30015")
	parser.add_option("-u", "--user", dest="user", default="SYSTEM")
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

	tables = {
		"types": '"UMLS"."SEMANTIC_TYPES"',
		"relations": '"UMLS"."SEMANTIC_TYPE_RELATIONS"',
		"groups": '"UMLS"."SEMANTIC_GROUPS"'
	}

	src_files = {
		"types": os.path.join(path, 'SRDEF.html'),
		"relations": os.path.join(path, 'SRSTRE1.html'),
		"groups": os.path.join(path, 'SemGroups.txt')
	}

	files = {}

	# Check if files exists
	for key, path in src_files.iteritems():
		if os.path.exists(path):
			files[key] = path
		else:
			files[key] = None

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
		parser.error("invalid username or password")


	##################################
	##################################
	##################################
	print " * Creating the schema and tables..."
	createUMLSSchemaAndTables(connection)

	if files['types']:
		readSemanticTypes(cursor, files['types'], tables['types'])
	else: print " * Types file not found! Skipping types. (%s)" % (src_files['types'])


	if files['relations']:
		readSemanticRelations(cursor, files['relations'], tables['relations'])
	else: print " * Relations file not found! Skipping relations. (%s)" % (src_files['relations'])


	if files['groups']:
		readSemanticGroups(cursor, files['groups'], tables['groups'])
	else: print " * Groups file not found! Skipping groups. (%s)" % (src_files['groups'])
	
	
	connection.commit()
	connection.close()
	print " * Done"



