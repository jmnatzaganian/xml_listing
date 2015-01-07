''' xml_file_listing.py

	Author        : James Mnatzaganian
	Contact       : http://techtorials.me
	Version       : 1.0
	Date Created  : 12/21/2013
	Date Modified : 12/28/2013
	Python Version: 2.7

	Purpose: Module for building XML files from a file path
	
	License:
		The MIT License (MIT)
		
		Copyright (c) 2013 James Mnatzaganian

		Permission is hereby granted, free of charge, to any person obtaining a
		copy of this software and associated documentation files
		(the "Software"), to deal in the Software without restriction,
		including without limitation the rights to use, copy, modify, merge,
		publish, distribute, sublicense, and/or sell copies of the Software,
		and to permit persons to whom the Software is furnished to do so,
		subject to the following conditions:

		The above copyright notice and this permission notice shall be included
		in all copies or substantial portions of the Software.

		THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
		OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
		MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
		IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
		CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
		TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
		SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Native Imports
import os, time, sys

''' XMLFileListing

	Purpose : Generates an XML file listing of the supplied path
	
	Inputs  : tree_start
				Type   : String
				Purpose: Full path to begin creation of the directory listing
			 xml_file
				Type   : String
				Purpose: Full path to where the new XML file should be created
			 quiet
				Type   : Boolean
				Purpose: Flag to suppress printing
			 size
				Type   : Boolean
				Purpose: Flag to capture size time
			 ctime
				Type   : Boolean
				Purpose: Flag to capture created time
			 mtime
				Type   : Boolean
				Purpose: Flag to capture modified time
			 atime
				Type   : Boolean
				Purpose: Flag to capture accessed time
	Requires: os, time, sys, xml
'''
class XMLFileListing():
	def __init__(self, tree_start, xml_file, quiet = False, size = True,
			ctime = True, mtime = True, atime = True):
		# User params
		self.tree_start   = tree_start
		self.xml_file     = xml_file
		self.quiet        = quiet
		self.size         = size
		self.ctime        = ctime
		self.mtime        = mtime
		self.atime        = atime
		
		# Initializations
		self.level_count  = -1         # Current level in XML file
		self.xml_text     = ""         # Full contents of XML file
		self.file_count   = 0          # Total number of flies found
		self.warnings     = []         # Files that stats failed on
		
		# Set proper line termination
		if sys.platform == 'win32':
			self.EOL   = '\r\n'
			self.delim = '\\'
		else:
			self.EOL   = '\n'
			self.delim = '/'

	''' add_whitespace
	
		Purpose : Adds proper indenting and line termination for current level
		
		Inputs  : cur_line
					Type   : String
					Purpose: Text to add to the current line
				 num_lvls
					Type   : Integer
					Purpose: The number of levels deep the current line is
					
		Returns : new_line
					Type   : String
					Purpose: Formatted text to add to the current line
		
		Requires: EOL
	'''
	def add_whitespace(self, cur_line, num_lvls):
		return "".join("\t" for x in range(num_lvls)) + cur_line + self.EOL
	
	''' escape_xml
	
		Purpose : Escapes special characters in XML
		
		Inputs  : text
					Type   : String
					Purpose: String to escape
					
		Returns : new_text
					Type   : String
					Purpose: Escaped string
	'''
	def escape_xml(self, text):
		escape_chars = {'"':"&quot;", "'":"&apos;", "<":"&lt;", ">":"&gt;",
						"&":"&amp;"}
		for char in escape_chars:
			text = text.replace(char, escape_chars[char])
		return text
	
	''' get_file_listing
	
		Purpose : Creates the file listing from a given path
		
		Creates : file_listing
					Type   : List of Strings
					Purpose: To store all files in the path
					
		Requires: os, tree_start, quiet
	'''
	def get_file_listing(self):
		self.file_listing = []
		if self.quiet:
			for root, dirs, files in os.walk(self.tree_start):
					for f in files:
						f = os.path.join(root, f)
						self.file_listing.append(f)
		else:
			for root, dirs, files in os.walk(self.tree_start):
					for f in files:
						f = os.path.join(root, f)
						self.file_listing.append(f)
						print 'Adding file: %s ' % f
	
	''' read_file_listing
	
		Purpose : Reads in the file listing from a file
		
		Creates : file_listing
					Type   : List of Strings
					Purpose: To store all files in the path
					
		Requires: os, tree_start
	'''
	def read_file_listing(self):
		with open(self.tree_start, 'rb') as f:
			self.file_listing = [line.strip() for line in f]
	
	''' end_levels
	
		Purpose : Terminates XML levels
		
		Inputs  : dirs
					Type   : String
					Purpose: Text to add to the current line
					
		Modifies: level_count
					Type   : Integer
					Purpose: Current level of indention in the XML
				  xml_text
					Type   : String
					Purpose: Holds full contents of the XML file being built
		
		Requires: xml_text, level_count, add_whitespace()
	'''
	def end_levels(self, dirs):
		for d in dirs:
			self.xml_text  += self.add_whitespace(
								"</directory>", self.level_count)
			self.level_count -= 1
	
	''' add_levels
	
		Purpose : Adds XML levels
		
		Inputs  : dirs
					Type   : String
					Purpose: Text to add to the current line
					
		Modifies: level_count
					Type   : Integer
					Purpose: Current level of indention in the XML
				  xml_text
					Type   : String
					Purpose: Holds full contents of the XML file being built
					
		Requires: xml_text, level_count, add_whitespace()
	'''
	def add_levels(self, dirs):
		for d in dirs:
			self.level_count += 1
			self.xml_text  += (
				self.add_whitespace("<directory>", self.level_count) +
				self.add_whitespace("<name>%s</name>" %
					self.escape_xml(os.path.basename(d)), self.level_count + 1)
			)

	''' add_file
	
		Purpose : Adds a file and any desired properties to the XML
		
		Inputs  : file_path
					Type   : String
					Purpose: Full path of file to add
					
		Modifies: xml_text
					Type   : String
					Purpose: Holds full contents of the XML file being built
					
		Requires: xml, xml_text, level_count, add_whitespace()
	'''
	def add_file(self, file_path):
		self.file_count += 1
		skip_stats = False
		try:
			file_stats = os.stat(file_path)
		except:
			skip_stats = True
			self.warnings.append(file_path)
		self.xml_text += (
			self.add_whitespace("<file>", self.level_count + 1) +
			self.add_whitespace("<name>%s</name>" %
				self.escape_xml(os.path.basename(file_path)),
				self.level_count + 2)
		)
		if not skip_stats:
			if self.size:
				self.xml_text += self.add_whitespace("<size>%s</size>" % 
					file_stats.st_size, self.level_count + 2)
			if self.ctime:
				self.xml_text += self.add_whitespace(
					"<created_time>%s</created_time>" % 
					time.strftime("%c", time.localtime(file_stats.st_ctime)),
					self.level_count + 2)
			if self.mtime:
				self.xml_text += self.add_whitespace(
					"<modified_time>%s</modified_time>" % 
					time.strftime("%c", time.localtime(file_stats.st_mtime)),
					self.level_count + 2)
			if self.atime:
				self.xml_text += self.add_whitespace(
					"<accessed_time>%s</accessed_time>" % 
					time.strftime("%c", time.localtime(file_stats.st_atime)),
					self.level_count + 2)
					
		self.xml_text += self.add_whitespace("</file>", self.level_count + 1)
	
	''' close_directories
	
		Purpose : Closes any lingering directory tags
		
		Creates : elapsed_time
					Type   : Float
					Purpose: Measure how long it took to build the XML file
		
		Modifies: level_count
					Type   : Integer
					Purpose: Current level of indention in the XML
					
		Requires: level_count, xml_text
	'''
	def close_directories(self):
		while self.level_count != -1:
			self.xml_text += self.add_whitespace("</directory>", 
								self.level_count)
			self.level_count -= 1
	
	''' build_xml
	
		Purpose : Business logic for going from file listing to XML
					
		Requires: os, file_listing, end_levels(), add_levels()
	'''
	def build_xml(self, use_file):
		# Initializations
		if use_file:
			self.read_file_listing()
		else:
			self.get_file_listing()
		prev_dir    = ""
		first_level = True
		start_time  = time.time()

		for f in self.file_listing:
			# Initialize current path
			dir = os.path.dirname(f)

			# Directory structure changed
			if dir != prev_dir:
				# Going deeper into current branch - add new levels
				if prev_dir in dir and \
						dir.rfind(self.delim) > prev_dir.rfind(self.delim):
					new_dirs = [x for x in 
						dir[len(prev_dir):].split(self.delim) if x != ""]
					
					# Update tree structure
					if first_level:
						first_level = False
						self.add_levels([self.delim + self.delim + 
							new_dirs[0]] + new_dirs[1:])
					else:
						self.add_levels(new_dirs)
				
				# End of current branch - end previous levels and add new ones
				else:
					# Find changes in tree structure
					tmp_dir = prev_dir
					while True:
						tmp_dir = os.path.dirname(tmp_dir)
						if len(tmp_dir) < len(dir):
							if tmp_dir in dir and \
									(dir[len(tmp_dir)] == self.delim or
									tmp_dir[0:-1] == dir.split(self.delim)[0]):
								end_dirs = [
									x for x in
									prev_dir[len(tmp_dir):].split(self.delim)
									if x != ""
								]
								new_dirs = [
									x for x in \
										dir[len(tmp_dir):].split(self.delim)
									if x != ""
								]
								break
					
					# Update tree structure
					self.end_levels(end_dirs)
					self.add_levels(new_dirs)
			
			# Update tree structure
			self.add_file(f)
			prev_dir = dir
			
		# Close open directory tags
		self.close_directories()
		
		# Print warnings
		if len(self.warnings) > 0:
			print '\nWARNING: Stats were unable to be obtained for the ' \
			      'following file(s):'
			for warning in self.warnings:
				print warning
		
		# Performance metric
		self.elapsed_time = time.time() - start_time
		
		# Print some statistics
		if not self.quiet:
			print '%s files were found in %d seconds' % (self.file_count,
				self.elapsed_time)
			
	''' write
	
		Purpose : Write the XML string to the file
					
		Requires: sys, xml_text, xml_file
	'''
	def write(self):
		with open(self.xml_file, 'wb') as f:
			if sys.platform == 'win32':
				f.write('<?xml version="1.0" encoding="ISO-8859-1"?>')
			else:
				f.write('<?xml version="1.0" encoding="%s"?>' % \
					sys.getdefaultencoding)
			f.write(self.xml_text)
