# kwdb #

## LSL2/OSSL/AA Keywords Database and Derived Files Generator ##

### Description ###

This project aims to help synchronizing the various files around that depend on functions and constants added to LSL and similar languages, as additions are frequent and this causes obsolete syntax highlighting files, etc.

This mission is accomplished through a central keyword database in XML format maintained by volunteers; an XML parser using pyXML SAX, and output drivers (Python modules) for the different kinds of files to generate. Output drivers included here are the three files in the viewer source necessary for LSL syntax highlighting, [GeSHi](http://qbnz.com/highlighter/) syntax highlighter PHP code output, [Kate](http://kate-editor.org/) editor syntax highlighting XML output, Haskell code for [LSLForge](https://github.com/KoolLSL/lslforge) (most maintained fork of now archived [LSLForge](https://github.com/elnewfie/lslforge)), [lslint](https://github.com/pclewis/lslint) output, and a few more.

### Quickstart ###

The project is basically self-contained. You only need a working Python installation with default modules. The project attempts to support Python 2 and Python 3 simultaneously, but that aim might not be fully accomplished. In case you see something that doesn't work with your Python version, please report it together with the specific version you're using. The developers are using Python 2.7 at the moment, and occasionally test with Python 3.2.

The main program is in lsl2dfg/ and is called LSL2dfg.py. It can be invoked from either that folder, or from any folder if the -d option is specified to indicate where the database file is.

There are two shell scripts, generate.sh and check.sh, which generate all the outputs currently supported, which are in the outputs/ subfolder. The check.sh script performs a validation of the XML database against the DTD, and provides some output files that help checking it for consistency, including inworld tests.

The inputs/ subfolder contains the input templates needed by some of the generation modules. Not all modules need an input template, though.

### License ###

The license for the project is the GNU Lesser General Public License (LGPL) version 3 or later. Read the full text of the license here:

http://www.gnu.org/licenses/lgpl-3.0.html
