#!/bin/python
from optparse import OptionParser
import sys
import os
import re
import getpass
import pyhdb

from umls2hana.semanticnetwork import *


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



