import cgi
import string

class HDBDict(object):
	"""
		_voc maps categories to entities which have a set of variants assigned
	"""
	def __init__(self):
		self._voc = {}

	def escape(self, text):
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


	def addEntity(self, name, category):
		category = category.upper()
		name = name.strip()

		if not category in self._voc:
			self._voc[category] = {}

		if not name in self._voc[category]:
			self._voc[category][name] = set()

		self._voc[category][name].add(name)


	def addVariant(self, name, category, term):
		category = category.upper().strip()
		name = name.strip()
		term = term.strip()
		try:
			self._voc[category][name].add(term)
		except Exception, e:
			print e

	
	def writeToFile(self, output_file):
		f = open(output_file, 'w')
		f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		f.write('<dictionary xmlns="http://www.sap.com/ta/4.0">\n')

		for category in self._voc:
			f.write('  <entity_category name="' + self.escape(category) + '">\n')

			for name in self._voc[category]:

				try:
					estr = ''
					estr += '    <entity_name standard_form="' + self.escape(name) + '">\n'
					for variant in self._voc[category][name]:
						estr += '      <variant name="' + self.escape(variant) + '"/>\n'
					estr += '    </entity_name>\n'
					f.write(estr)
				except Exception, e:
					print e

			f.write('  </entity_category>\n')
		f.write('</dictionary>\n')
		f.close() 		