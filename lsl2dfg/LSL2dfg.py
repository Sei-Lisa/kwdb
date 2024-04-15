#!/usr/bin/env python

# LSL2 Derived Files Generator - Main program.
#
# (C) Copyright 2013, 2024 Sei Lisa.
# Sei Lisa is the author's username in the Second Life(R) online virtual world.
#
# This file is part of LSL2 Derived Files Generator.
#
#    LSL2 Derived Files Generator is free software: you can redistribute it
#    and/or modify it under the terms of the GNU Lesser General Public License
#    as published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    LSL2 Derived Files Generator is distributed in the hope that it will be
#    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with LSL2 Derived Files Generator. If not, see
#    <http://www.gnu.org/licenses/>.
#
# Second Life is a registered trademark of Linden Research, Inc.


# This program generates the following files:
# - Source code for the viewer's embedded editor syntax highlighting of
#   functions (lscript_library.cpp)
# - Auxiliary file for the viewer's keywords excluding functions
#   (keywords.ini)
# - Auxiliary file for the viewer's embedded editor tooltip help for functions
#   (strings.xml)
# - Dictionary file for the spelling checker (en_sl.dic)
# - GeSHi syntax highlighting file (lsl2.php)
# - Kate Editor syntax highlighting file (lsl.xml)
# - LSLForge Haskell code for functions (FuncSigs.hs)
# - LSLForge Haskell code for constants (Constants.hs)
# - A few more are included for sanity checks etc.
# - It's easy to add other output drivers.
#
# The output drivers are named respectively:
# "viewersrc", "viewerkw", "viewerstr", "dictionary", "geshi", "kate",
# "funcsigshs", "constantshs"
#
# This program takes as input an XML file containing all keywords, types,
# constants, functions and events, with this format:
#
# <keywords version="version">  Top level element - contains a collection of the following tags:
#
#   Grid tags must appear at the start and there can be any number of them:
#
#   <grid id="{ident}" [version="version"]>
#     [Grid description]
#   </grid>
#
#   The rest are all optional and can appear in any order, and except for <defaults>
#   there can be any number of them (there can be only one <defaults>):
#
#   <defaults>
#     [<description lang="{langcodes}"> {text} </description> ...]
#   </defaults>
#
#   <keyword name="{ident}" [status="{normal|unimplemented}"] [grid="{grid}"]>
#     [<description lang="{langcodes}" [other attributes?]> {text} </description> ...]
#   </keyword>
#
#   <type name="{ident}" [grid="{grid}"]>
#     [<description lang="{langcodes}" [other attributes?]> {text} </description> ...]
#   </type>
#
#   <constant name="{ident}" [grid="{grid}"] type="{LSL type}" [value="{value}"] [version="{version}]
#             [status="{normal|deprecated|unimplemented}"]>
#     [<description lang="{langcodes}" [other attributes?]> {text} </description> ...]
#   </constant>
#
#   <function name="{ident}" [grid="{grid}"] [type="{return type}"] [delay="{float value}"]
#             [energy="{float value}"] [version="{version}"]
#             [status="{normal|deprecated|godmode|unimplemented}"]>
#     [<param name="{ident}" type="{LSL type}"/> ...]
#     [<description lang="{langcodes}" [other attributes?]> {text} </description> ...]
#   </function>
#
#   <event name="{ident}" [grid="{grid}"]>
#     [<param name="{ident}" type="{LSL type}"/> ...]
#     [<description lang="{langcodes}" [other attributes?]> {text} </description> ...]
#   </event>
# </keywords>
#
# It loads the XML database into a memory variable with this format:
#
#   possibly empty list of keyword elements, each element being:
#     a dictionary, with the following fixed entries:
#       "cat": string with identifier category ("keyword", "type", "constant", "function", "event")
#       "name": string with the identifier itself
#     and the following optional entries extracted from the attributes of the XML tag:
#       "grid": string with the space-separated grid list; if not present it means all grids
#       "type": return type for functions; value type for constants; not used for the rest
#       "value": value of the constant for constants; not used for the rest
#       "version": a version string representing the server version and date in which the
#                  constant, function or event was added (not applicable to keywords or types);
#                  the string contains a space-separated list of grid:version pairs.
#       "status": it can be:
#                 - the string "normal" (the default if not present)
#                 - the strings "deprecated", "unimplemented" or "godmode" for functions or constants
#       "energy": (only for functions) a float representing the energy of the function, default 10.0
#       "delay": (only for functions) a float representing the delay of the function, default 0.0
#     and the following optional entries derived from the contained tags:
#       "params": (only for functions or events) a nonempty list, each element being:
#         a dictionary, with these entries:
#           "type": the type of the parameter
#           "name": a descriptive identifier for the parameter
#       "desc": a dictionary, with each entry key being:
#         a language code, with the value being a dictionary, with these fixed entries:
#           "text": the textual data contents of the description tag
#         and these optional entries extracted from the attributes of the <description> tag:
#           (none at the moment)
#
# and another memory variable with the contents of the <defaults> section, in this format:
#
#   a dictionary, with each entry key being:
#     a language code, with the default value to use for that language if the corresponding
#       description is not present
#
# Note that where a nonempty list is specified in the above description, the whole element is optional.
# It may be not present, meaning no elements, but if present, it will contain at least one element.
#
# Example: if the XML database contains this:
#
# <keywords>
#   <function name="llTarget" type="integer">
#     <param type="vector" name="position"/>
#     <param type="float" name="range"/>
#     <description lang="en">
# Sets positions within range of position as a target and return an ID for the target
#     </description>
#   </function>
#
#   <keyword name="event"/>
# </keywords>
#
# then this program loads it into the following Python structure:
#
# [{"cat":"function",
#   "name":"llTarget",
#   "type":"integer",
#   "params":[{"name":"position", "type":"vector"},
#             {"name":"range", "type":"float"}
#            ],
#   "desc":{"en":{"text":"Sets positions within range of position as a target and return an ID for the target"}}
#  },
#  {"cat":"keyword",
#   "name":"event"
#  }
# ]
#
# After loading the XML file into these structures, the program passes them to
# the output module.
#
# This program uses the output driver modules in the lsloutput/ subdirectory.
# They are dynamically imported with __import__ depending on the format
# parameter selected in the command line. That parameter must match
# a Python module name in the lsloutput/ subdirectory, otherwise an
# ImportError exception will be raised.
#
# IMPORTANT: The viewerkw.py module requires the descriptions of all
# elements except functions not to contain colons (:), because the
# keywords.ini file uses the colon as line separator, as per these lines of
# llui/llkeywords.cpp:
#
#      // Replace : with \n for multi-line tool tips.
#      LLStringUtil::replaceChar( tool_tip, ':', '\n' );
#
# (The keywords.ini file does not have descriptions of functions, therefore function
# descriptions can contain colons.)


import sys #, os
import getopt
from xml import sax

version = "0.0.20240415000"
defaultlang = "en"
defaulttag = "LSL"

class ParameterException(Exception):
  pass

class LSLXMLException(sax.SAXParseException):
  def __init__(self, text, locator):
    super(LSLXMLException, self).__init__(text, self, locator)


class LSLXMLDefaultHandler(sax.handler.EntityResolver, sax.handler.DTDHandler,
                           sax.handler.ContentHandler, sax.handler.ErrorHandler):
  pass

class LSLDefinitionLoader(LSLXMLDefaultHandler):

  def __init__(self, grids, unique):
    self.grids = grids
    self.unique = unique
    self.names = set()
    self.document = []
    self.defaults = {}
    self.in_keywords = False
    self.has_keywords = False
    self.in_ident = False
    self.has_nongrid = False
    self.in_grid = False
    self.in_defaults = False
    self.has_defaults = False
    self.in_param = False
    self.in_desc = False
    self.version = "0"
    self.checked_grids = False
    self.griddata = {}

  def setDocumentLocator(self, locator):
    self.locator = locator

  def startElement(self, tag, attrs):

    self.lasttag = tag

    if tag == "keywords":
      if self.in_keywords:
        raise LSLXMLException("Nested <keywords> tags not allowed", self.locator)
      if self.has_keywords:
        raise LSLXMLException("Just one <keywords> root tag allowed", self.locator)
      self.in_keywords = True
      self.has_keywords = True
      self.version = attrs.get("version")

    elif tag == "grid":
      if self.has_nongrid:
        raise LSLXMLException("<grid> tag must appear before any other tags", self.locator)
      self.in_grid = True
      self.content = ""
      self.data = {"id": attrs.get("id")}
      for attr in ("version",):
        if attr in attrs:
          self.data[attr] = attrs.get(attr)

    elif tag in ("defaults", "keyword", "type", "constant", "function", "event"):
      if not self.in_keywords:
        raise LSLXMLException("<keywords> root tag not opened", self.locator)

      if self.in_ident or self.in_defaults or self.in_grid:
        raise LSLXMLException("Nested identifier/defaults tags not allowed. Found nested tag; <%s>" % tag, self.locator)

      if not self.checked_grids:
        if self.grids is not None:
          for grid in self.grids:
            if grid[0:1] == '-':
              grid = grid[1:]
            if grid not in self.griddata:
              raise ParameterException("One of the specified grids is not in the database: " + grid)
        self.checked_grids = True

      self.has_nongrid = True

      if tag == "defaults":
        if self.has_defaults:
          raise LSLXMLException("Only one defaults tag is allowed", self.locator)
        self.in_defaults = True
        self.has_defaults = True

      else:
        # No duplicate check - at most it should be unique per grid, not in the file;
        # but also, overloaded functions are supported by some grids, so it should
        # be actually unique per grid and param type list. No such detection is made.
        #
        #if attrname in self.names:
        #  raise LSLXMLException("Duplicate identifier name: " + attrname, self.locator)
        #self.names.add(attrname)

        self.in_ident = True
        self.params = None
        self.data = \
          { "cat": tag
          , "name": attrs.get("name")
          }
        for attr in ("grid", "type", "value", "status", "energy", "delay", "version"):
          if attr in attrs:
            # Accept backslash-escaped strings
            self.data[attr] = attrs.get(attr).encode('latin1', 'backslashreplace').decode('unicode_escape')

    elif tag == "description":
      if self.in_ident or self.in_defaults:
        if self.in_desc:
          if self.in_ident:
            raise LSLXMLException("Nested <description> tags not allowed, in identifier '%s'" % self.data["name"], self.locator)
          else:
            raise LSLXMLException("Nested <description> tags not allowed inside <defaults>", self.locator)
        if self.in_param:
          raise LSLXMLException("<description> tag not allowed inside <param> tag, in identifier '%s'" % self.data["name"], self.locator)
        if self.in_grid:
          raise LSLXMLException("<description> tag not allowed inside <grid> tag", self.locator)
        self.in_desc = True
        self.content = ""
        self.descattrs = {}
        for attr in ("lang",):
          if attr in attrs:
            self.descattrs[attr] = attrs.get(attr)
      else:
        raise LSLXMLException("<description> not inside an identifier definition or defaults tag", self.locator)

    elif tag == "param":
      if self.in_ident:

        if self.in_param:
          raise LSLXMLException("Nested <param> tags not allowed, in identifier '%s'" % self.data["name"], self.locator)
        if self.in_desc:
          raise LSLXMLException("<param> tag not allowed inside <description> tag, in identifier '%s'" % self.data["name"], self.locator)

        self.in_param = True

        if self.params is None:
          self.params = []
        param = {"type": attrs.get("type"), "name": attrs.get("name")}
        for test in self.params:
          if test["name"] == param["name"]:
            raise LSLXMLException("Duplicate parameter: '%s' in identifier '%s'" % (param["name"], self.data["name"]), self.locator)
        self.params.append(param)
      else:
        raise LSLXMLException("<param> tag not inside an identifier definition tag", self.locator)

    else:
      raise LSLXMLException("Unknown tag: " + tag, self.locator)

  def characters(self, ch):

    if self.in_desc or self.in_grid:
      self.content = self.content + ch
    elif ch.strip(" \r\n\t") != "":
      raise LSLXMLException("Unexpected text '%s' inside <%s> tag" % (ch, self.lasttag), self.locator)

  def endElement(self, tag):
    if tag == "grid":
      if not self.in_grid:
        raise LSLXMLException("Closing <grid> without opening it", self.locator)
      self.in_grid = False
      gridid = self.data['id']
      self.griddata[gridid] = {}
      if self.content != "":
        self.griddata[gridid]["name"] = self.content
      if "version" in self.data:
        self.griddata[gridid]["version"] = self.data["version"]

    elif tag in ("keyword", "type", "constant", "function", "event"):
      if not self.in_ident:
        raise LSLXMLException("Closing <%s> without opening it" % tag, self.locator)
      self.in_ident = False
      if self.params is not None:
        self.data["params"] = self.params

      # Filter by grids list
      include = False
      if self.grids is None:
        include = True
      else:
        kwgrids = None
        if "grid" in self.data:
          kwgrids = self.data["grid"].split()

        for grid in self.grids:
          if grid[0] == "-":
            # Exclusion pattern
            if kwgrids is None or grid[1:] in kwgrids:
              include = False
          else:
            # Inclusion pattern
            if kwgrids is None or grid in kwgrids:
              include = True

      if include:
        if not self.unique or self.data["name"] not in self.names:
          if self.unique: # otherwise don't bother, it's a waste of memory
            self.names.add(self.data["name"])
          self.document.append(self.data)

    elif tag == "defaults":
      if not self.in_defaults:
        raise LSLXMLException("Closing <defaults> without opening it", self.locator)
      self.in_defaults = False

    elif tag == "description":
      if not self.in_desc:
        raise LSLXMLException("Closing <description> without opening it", self.locator)
      self.in_desc = False

      # Strip spaces and tabs
      self.content = self.content.strip(" \t")
      # Strip exactly one LF if present at first position
      if self.content[:1] == "\n":
        self.content = self.content[1:]
      # Strip exactly one LF if present at last position
      if self.content[-1:] == "\n":
        self.content = self.content[:-1]

      if self.content != "": # do not add empty descriptions

        self.descattrs["text"] = self.content
        langs = [defaultlang]
        if "lang" in self.descattrs:
          langs = self.descattrs["lang"].split()
          del self.descattrs["lang"]

        if self.in_defaults:
          for lang in langs:
            if lang in self.defaults:
              raise LSLXMLException("Duplicate language '%s' in descriptions within <defaults>" % lang, self.locator)
            self.defaults[lang] = self.content

        else:
          if "desc" not in self.data:
            self.data["desc"] = {}

          for lang in langs:
            if lang in self.data["desc"]:
              raise LSLXMLException("Duplicate language '%s' in descriptions of element '%s'" % (lang, self.data["name"]), self.locator)
            self.data["desc"][lang] = self.descattrs

    elif tag == "param":
      if not self.in_param:
        raise LSLXMLException("Closing <param> without opening it", self.locator)
      self.in_param = False


def loadXML(filename, grids, unique):
  """Load the XML LSL definitions file into memory"""

  parser = sax.make_parser()
  parser.setFeature(sax.handler.feature_namespaces, 0)
  dochandler = LSLDefinitionLoader(grids, unique)
  parser.setContentHandler(dochandler)
  parser.parse(filename)

  # Ensure "default" always exists
  defaults = dochandler.defaults
  if "default" not in defaults:
    if defaultlang in defaults:
      # Use default if it exists
      defaults["default"] = defaults[defaultlang]
    else:
      defaults["default"] = ""

  return (dochandler.document, defaults, dochandler.version, dochandler.griddata)


def showusage():
  sys.stderr.write("Usage: %s [-h|--help] [-v|--version] [-p|--parse-only] [-c|--check|--validate] [-y|--python-exceptions] [-u|--unique] [-d|--database=...] [-f|--format=...] [-g|--grids=...] [-i|-input=...] [-o|--output=...] [-l|--lang=...] [-t|--tag=...]\n" % sys.argv[0])


def showhelp():
  showusage()
  sys.stderr.write("""
Parameters:
  -c, --check, --validate
                Validate the XML file against the DTD.
  -d, --database=xxx
                Database file to use.
  -f, --format=xxx
                Output format (a module name from the lsloutputs subdir, without the path or the .py extension).
  -g, --grids=xxx,yyy,...
                Grids to include or exclude in the output. If the grid is prefixed with a dash (-), exclude it. For example, --grids=sl,-os will include all identifiers that (implicitly or explicitly) have 'sl' as grid, then exclude all identifiers that have 'os' as grid. Default is to include all from all grids, which is rarely useful actually.
  -h, --help
                Print this help text.
  -i, --input=xxx
                Input file name. If omitted, stdin will be used.
  -l, --lang=xxx
                Language to use for descriptions, if the output module supports it. Default is %(lang)s.
  -o, --output=xxx
                Output file name. If omitted, stdout will be used.
  -p, --parse-only
                Do not invoke the output module, stop after parsing the XML file.
  -t, --tag=xxx
                Most output modules expect the input file to be a template having a marker like: <<< xxx KEYWORDS >>>, which will be replaced with the actual output from the module. This parameters allows to specify the xxx tag. Default tag is %(tag)s, meaning the default line is <<< %(tag)s KEYWORDS >>>.
  -u, --unique
                Filter out duplicate identifiers. Some identifiers have multiple instances (different definitions for different grids, or overloaded functions, for example). With this flag, only the first instance of each identifier will be used. Without it, all instances of the identifiers selected with --grid will be included.
  -v, --version
                Print the version. If used with --database, print also the database version.
  -y, --python-exceptions
                Show Python stack trace in case of exception. Without it, just the error message is printed.
""" % {'lang': defaultlang, 'tag': defaulttag})


# Exceptions during the getopt phase will be reported Python style

try:
  opts, args = getopt.getopt(sys.argv[1:], 'hvypcud:f:i:o:l:t:g:',
    ("help", "version", "python-exceptions", "parse-only", "check", "validate", "unique", "database=", "format=", "input=", "output=", "lang=", "tag=", "grids="))
except getopt.GetoptError:
  showusage()
  raise

arghelp = False
argversion = False
argvalidatedtd = False
argparseonly = False
argpyexcept = False
argunique = False
argdatabase = None
argformat = None
arginput = None
argoutput = None
arglang = None
argtag = None
arggrids = None

for opt, arg in opts:
  if opt in ('-y', '--python-exceptions'):
    argpyexcept = True
  elif opt in ('-h', '--help'):
    arghelp = True
  elif opt in ('-v', '--version'):
    argversion = True
  elif opt in ('-p', '--parse-only'):
    argparseonly = True
  elif opt in ('-c', '--check', '--validate'):
    argvalidatedtd = True
  elif opt in ('-u', '--unique'):
    argunique = True
  elif opt in ('-d', '--database'):
    argdatabase = arg
  elif opt in ('-f', '--format'):
    argformat = arg
  elif opt in ('-i', '--input'):
    arginput = arg
  elif opt in ('-o', '--output'):
    argoutput = arg
  elif opt in ('-l', '--lang'):
    arglang = arg
  elif opt in ('-t', '--tag'):
    argtag = arg
  elif opt in ('-g', '--grids'):
    arggrids = arg

# Now we have an usable pyexcept setting.

try:
  if arghelp:
    showhelp()

  if arggrids is not None:
    arggrids = arggrids.split(',')

  if argversion:
    print("LSL2 Derived Files Generator version: " + version)
    if argdatabase is not None:

      document = loadXML(argdatabase, [], True)
      print("Database version: " + document[2])
      if document[3]:
        print("Based on the following grid versions:")
        for grid in document[3]:
          if arggrids is None or grid in arggrids:
            data = document[3][grid]
            gridname = grid
            if 'name' in data:
              gridname += " (" + data['name'] + ")"
            if 'version' in data:
              ver = data['version']
            else:
              ver = '(unspecified)'
            print("\t%s: %s" % (gridname, ver))

  if not arghelp and not argversion:
    if argdatabase is None:
      showusage()
      raise ParameterException("No --database specified.")

    if argvalidatedtd:
      try:
        from lxml import etree
      except ImportError:
        print("lxml is necessary for DTD validation, but it is not installed or not found.")
        raise

      parser = etree.XMLParser(dtd_validation = True)
      etree.parse(argdatabase, parser)

    document = loadXML(argdatabase, arggrids, argunique)

    if not argparseonly:
      if argformat is None:
        showusage()
        raise ParameterException("Neither --format nor --parse-only was specified.")

      if arglang is None:
        arglang = defaultlang

      if argtag is None:
        argtag = defaulttag

      # Add the path to the script
      #sys.path.append(os.path.dirname(sys.argv[0]))

      # Will raise an ImportError or AttributeError exception if the output module is not found
      lsloutput = getattr(__import__("lsloutputs." + argformat), argformat)
      lsloutput.output(document[0], document[1], document[2], arginput, argoutput, arglang, argtag)

except Exception:
  if not argpyexcept:
    e = sys.exc_info()[:2]
    sys.stderr.write("EXCEPTION %s: %s\n" % (e[0].__name__, str(e[1])))
    sys.exit(2)
  else:
    raise

pass
