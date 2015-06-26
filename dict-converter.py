#!/bin/python
from optparse import OptionParser
from umls2hana.HDBDict import HDBDict
import os
import gc

if __name__ == '__main__':
	usage = "usage: %prog [options] umlspath"
	parser = OptionParser(usage=usage)
	parser.add_option("-o", "--output", dest="output", default="xml-output")
	(options, args) = parser.parse_args()

	output_path = options.output

	if len(args) != 1:
		parser.error("UMLS-Path is missing!")


	umlspath = args[0]

	metapath = os.path.join(umlspath, 'META')
	if not os.path.isdir(metapath):
		parser.error("Given UMLS-Path is invalid!")



	conceptsFilepath = os.path.join(metapath, 'MRCONSO.RRF')
	typesFilepath = os.path.join(metapath, 'MRSTY.RRF')

	if not os.path.exists(conceptsFilepath):
		parser.error('Can\'t find concepts file (META/MRCONSO.RRF) in UMLS-Path!')

	if not os.path.exists(typesFilepath):
		parser.error('Can\'t find types file (META/MRSTY.RRF) in UMLS-Path!')


	# Number of concepts per dictionary
	dictChunkSize = 500000
	chunkId = 1

	with open(conceptsFilepath, 'r') as conceptsFile:
		with open(typesFilepath, 'r') as typeFile:

			done = False
			while not done:
				print " * Reading next chunk (#%d)..." % (chunkId)
				max_concept_id = chunkId * dictChunkSize

				concepts = {}

				#
				#
				# Read Terms
				last_pos = conceptsFile.tell()
				while True:
					last_pos = conceptsFile.tell()
					line = conceptsFile.readline()
					if line == '':
						done = True
						break

					# 0 - Unique identifier for concept
					# 1 - Language of term
					# 2 - Term status
					# 3 - Unique identifier for term
					# 4 - String type
					# 5 - Unique identifier for string
					# 6 - Atom status - preferred (Y) or not (N) for this string within this concept
					# 7-13 - ...
					# 14 - String
					# 15 - Source restriction level
					# 16 - ...
					# 17 - ...
					# 18 - invalid
					concept = line.split('|')
					cui = concept[0]
					if cui == '':
						break

					# Break if we've exceeded the max concept id
					cui_num = int(cui[1:])
					if cui_num > max_concept_id:
						conceptsFile.seek(last_pos)
						break


					string = concept[14]

					if not cui in concepts:
						concepts[cui] = {
							"terms": set(),
							"types": set(),
							"preferred_terms": []
						}

					# ignore all terms that are 2 characters or shorter
					# TODO: use stopword list
					if len(string) > 2:
						concepts[cui]["terms"].add(string)

						if concept[6] == 'Y':
							concepts[cui]["preferred_terms"].append(string)

				#
				#
				# Read Types
				last_pos = typeFile.tell()
				while True:
					last_pos = typeFile.tell()
					line = typeFile.readline()
					if line == '':
						done = True
						break

					# get semantic types for that CUI
					# 0 - Unique identifier of concept
					# 1 - Unique identifier of Semantic Type
					# 2 - Semantic Type tree number
					# 3 - Semantic Type. The valid values are defined in the Semantic Network
					# 4 - Unique identifier for attribute
					# 5 - Content View Flag. Bit field used to flag rows included in Content View.
					typ = line.split('|')
					cui = typ[0]

					# Break if we've exceeded the max concept id
					cui_num = int(cui[1:])
					if cui_num > max_concept_id:
						typeFile.seek(last_pos)
						break


					if not cui in concepts:
						concepts[cui] = {
							"terms": set(),
							"types": set(),
							"preferred_terms": []
						}

					# concepts[cui]["types"].add(typ[3]) # Named types
					concepts[cui]["types"].add(typ[1]) # T-Types


				#
				#
				#
				output_file = os.path.join(output_path, 'umls-%d.xml' % (chunkId))
				print " * Writing to HANA dictionary (%s)..." % (output_file)
				hdbdict = HDBDict()
				for cui in concepts:
					if len(concepts[cui]["types"]) == 0:
						print cui
						break

					for typ in concepts[cui]["types"]:
						# Ignore concepts without terms
						if len(concepts[cui]["terms"]) == 0:
							break


						if len(concepts[cui]["preferred_terms"]) > 0:
							pref_term = concepts[cui]["preferred_terms"][0]
						else:
							pref_term = next(iter(concepts[cui]["terms"]))
							print cui

						hdbdict.addEntity(pref_term, typ)
						for term in concepts[cui]["terms"]:
							hdbdict.addVariant(pref_term, typ, term)

				hdbdict.writeToFile(output_file)
				chunkId += 1



