''' Build_XML_File_Listing.py

	Author        : James Mnatzaganian
	Contact       : http://techtorials.me
	Version       : 1.0
	Date Created  : 12/21/2013
	Date Modified : 12/28/2013
	Python Version: 2.7

	Purpose: Wrapper for XMLFileListing class, allowing a user to generate an
	         XML file listing for the supplied path.

	Usage  : Build_XML_File_Listing.py <options>
	
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

# Native imports
import os, sys, argparse

# Program imports
try:
	from xml_file_listing import XMLFileListing
except:
	print '\nERROR: Failed to import "xml_file_listing.py". Ensure that the ' \
	      'module is in the\n       same path as this program.'
	sys.exit(-1)

'''
	Captures user input to "Yes"/"No" questions. Ensures that the user responds
	correctly.
'''
def get_ui(prompt):
	while True:
		ui = raw_input(prompt)
		if ui.lower() == "n" or ui.lower() == "no":
			return False
		elif ui == "" or ui.lower() == "y" or ui.lower() == "yes":
			return True
		else:
			print '\n"%s" is not a valid response.\nYou must respond ' \
				  'with either "yes" or "no"' % ui

''' main
	
	Purpose: Control the flow of the program
'''
def main():
	# Argument parsing
	usage = '                                                               ' \
	        '                 usage: Build_XML_File_Listing.py <options>'
	parser = argparse.ArgumentParser(usage = argparse.SUPPRESS, 
				description = usage,
				formatter_class = argparse.RawDescriptionHelpFormatter)
	required = parser.add_argument_group('required arguments')
	required.add_argument('-i', action = 'store', dest = 'input', nargs = 1,
						  help = 'path to where the directory listing should '
								 'begin')
	required.add_argument('-o', action = 'store', dest = 'output', nargs = 1,
						  help = 'full output path to destination XML file')
	parser.add_argument('-f', '--file', action = 'store_true', dest = 'file',
						help = 'input is a file containing the paths')
	parser.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet',
						  help = 'suppresses file tree printing')
	parser.add_argument('-s', '--size', action = 'store_true', dest = 'size',
						  help = 'adds the file size')
	parser.add_argument('-c', '--ctime', action = 'store_true', dest = 'ctime',
						  help = 'adds date created time')
	parser.add_argument('-m', '--mtime', action = 'store_true', dest = 'mtime',
						  help = 'adds date modified time')
	parser.add_argument('-a', '--atime', action = 'store_true', dest = 'atime',
						  help = 'adds date accessed time')

	args = parser.parse_args()
	if not args.input:
		print '\nERROR: You must specify an input.'
		sys.exit(-1)
	if not args.output:
		print '\nERROR: You must specify an output.'
		sys.exit(-1)
	if args.file:
		if not os.path.isfile(args.input[0]):
			print '\nERROR: The input file\n       "%s"\n       does not ' \
				  'exist. Please specify a valid path.' % args.input[0]
			sys.exit(-1)
	else:
		if not os.path.isdir(args.input[0]):
			print '\nERROR: The input path\n       "%s"\n       does not ' \
				  'exist. Please specify a valid path.' % args.input[0]
			sys.exit(-1)
	if not os.path.isabs(args.output[0]):
		print '\nERROR: The ouput path\n       "%s"\n       does not ' \
		      'represent a path. Please specify a valid path.' % args.output[0]
		sys.exit(-1) 
	if args.output[0][-4:].lower() != ".xml":
		print '\nERROR: The ouput path\n       "%s"\n       does not point ' \
		      'to an XML file.\n       Please specify a valid path, ending ' \
			  'in ".xml".' % args.output[0]
		sys.exit(-1)
	if os.path.isfile(args.output[0]):
		warning = '\nWARNING: The path\n       "%s"\n       already exists. ' \
		          'Do you wish to overwrite it? (Yes, no) ' % args.output[0]
		if not get_ui(warning):
			print "\nERROR: Unable to delete file. Aborting at user's " \
				  'request.'
			sys.exit(-1)
	
	# Create instance of XMLFileListing
	XML = XMLFileListing(args.input[0], args.output[0], args.quiet, args.size,
						 args.ctime, args.mtime, args.atime)
	
	# Build the XML file
	if not args.quiet:
		print "\nBuilding the XML file. Please be patient."
	XML.build_xml(args.file)
	
	# Write out the XML file
	try:
		XML.write()
	except:
		warning = '\nWARNING: The path\n       "%s"\n       could not be ' \
		          'overwritten. Try closing the file.\n       ' \
		          ' Do you wish to try again? (Yes, no) ' % args.output[0]
		if not get_ui(warning):
			print "\nERROR: Unable to continue. Aborting at user's " \
				  'request.'
			sys.exit(-1)

# Start main()
if __name__ == "__main__":
	main()
