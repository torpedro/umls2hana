import cgi
import string
import pyhdb
import sqlhelper

class HDBDict(object):
	"""
		__voc maps categories to entities which have a set of variants assigned
		__synonyms
	"""
	def __init__(self):
		self.__voc = {}
		self.__synonyms = set()


	@staticmethod
	def escape(text):
		# remove all non printable characters
		# we had a case where there were ASCII control characters in the UMLS files
		# these will be removed
		text = filter(string.printable.__contains__, text) 

		# Escape the HTML special characters
		text = cgi.escape(text)
		text = text.replace('"', "'")
		text = text.replace('?', "\\?") # reserved wild card character
		text = text.replace('*', '\\*') # reserved wild card character
		return text


	def __addSynonym(self, pref_term, variant):
		tup = (HDBDict.escape(pref_term), HDBDict.escape(variant))
		self.__synonyms.add(tup)


	def addEntity(self, pref_term, category):
		category = category.upper()
		pref_term = pref_term.strip()

		if not category in self.__voc:
			self.__voc[category] = {}

		if not pref_term in self.__voc[category]:
			self.__voc[category][pref_term] = set()

		self.__voc[category][pref_term].add(pref_term)

		self.__addSynonym(pref_term, pref_term)


	def addVariant(self, pref_term, category, variant):
		category = category.upper().strip()
		pref_term = pref_term.strip()
		variant = variant.strip()
		try:
			self.__voc[category][pref_term].add(variant)
			self.__addSynonym(pref_term, variant)
		except Exception, e:
			print e

	
	def writeToFile(self, output_file):
		f = open(output_file, 'w')
		f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f.write('<dictionary xmlns="http://www.sap.com/ta/4.0">\n')

		for category in self.__voc:
			f.write('  <entity_category name="' + HDBDict.escape(category) + '">\n')

			for name in self.__voc[category]:

				try:
					estr = ''
					estr += '    <entity_name standard_form="' + HDBDict.escape(name) + '">\n'
					for variant in self.__voc[category][name]:
						estr += '      <variant name="' + HDBDict.escape(variant) + '"/>\n'
					estr += '    </entity_name>\n'
					f.write(estr)
				except Exception, e:
					print e

			f.write('  </entity_category>\n')
		f.write('</dictionary>\n')
		f.close() 		


	
	def writeSynonymsToFile(self, output_file):
		f = open(output_file, 'w')

		for pref_term, variant in self.__synonyms:
			pref_term = pref_term.replace("'", "''")
			variant = variant.replace("'", "''")
			line = '"%s";"%s"\n' % (pref_term, variant)
			f.write(line)

		f.close() 		



	def insertSynonymsIntoTable(self, connection, tablename):
		cursor = connection.cursor()

		i = 0
		for pref_term, variant in self.__synonyms:
			pref_term = pref_term.replace("'", "''")
			variant = variant.replace("'", "''")
			sql = "INSERT INTO %s VALUES('%s', '%s')" % (tablename, pref_term, variant)
			try:
				cursor.execute(sql)
			except pyhdb.exceptions.DatabaseError, e:
				s = str(e)
				if "too large for column" in s:
					print "Too Large"
				else:
					raise e

			i += 1
			if i % 1000 == 0:
				print "   * Committing chunk"
				connection.commit()
				sqlhelper.mergeDelta(connection, tablename)

		connection.commit()