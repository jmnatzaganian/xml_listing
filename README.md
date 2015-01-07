# xml_listing
## Intro
This is a basic Python program designed to traverse a path and generate a
properly indented XML file listing. More details may be found
[here](http://techtorials.me/xml-file-listing).
## Prerequisites
- [Python 2.7.8](https://www.python.org/download/releases/2.7.8/)

## Usage
Call "Build_XML_File_Listing" with the desired parameters.
### Supported Parameters
#### Required Parameters
These parameters denote options that are required for the program to perform
something useful. The below parameters are the parameters that are needed for
the various program paths.
##### Required Parameters 1
- "-h": Prints the message

##### Required Parameters 2
- "-i": Full path to the input directory or input file if the "-f" option is
used.
- "-o": Full path to an XML file where the output should be created.

#### Optional Parameters
These parameters are parameters that can be added to the required parameters
to add additional functionality.

- "-f": Denotes that the input is a file containing a list of directories. Each
directory should be on its own line.
- "-q": Suppresses the printing of the file paths
- "-s": Adds the file size, in bytes, to the XML
- "-c": Adds the date created time to the XML
- "-m": Adds the date modified time to the XML
- "-a": Adds the date accessed time to the XML

### Example
#### Example 1
The below command would create an XML file called "test.xml" in the "C"
directory. The XML file would be a full listing of the "C:\Windows\Help"
directory. Additionally, the XML would contain the following information about
each file: file size, creation time, modification time, access time.

python Build_XML_File_Listing.py -i "C:\Windows\Help" -o "C:\test.xml" -s -c
-m -a
#### Example 2
We have a file "paths.txt" and it is located at "C:\paths.txt". Inside this
file we the following:

C:\Python27

To build an XML of the directories in that file with the same options as the
first example, we would do the following:

python Build_XML_File_Listing.py -f -i "paths.txt" -o "C:\test.xml" -s -c -m -a
## Notes
To view the outputted XML an XML viewer is recommended. The free XML viewer,
[XMLViewer](http://www.mindfusion.eu/product1.html) was tested to work with
this output.
## Author
The original author of this code was James Mnatzaganian. For contact info, as
well as other details, see his corresponding [website](http://techtorials.me).
## Legal
This code is licensed under the [MIT license](http://opensource.org/licenses/mit-license.php).