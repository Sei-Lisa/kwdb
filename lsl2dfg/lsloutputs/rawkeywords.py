#!/usr/bin/env python

# rawkeywords.py - This is a LSL2dfg.py output module for vanilla output of the keywords, one per line.
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


# rawkeywords output module uses the input file name in a different way.
# It is an optional argument consisting of a string of letters:
#    k to output the language keywords
#    t to output the types
#    c to output the constants
#    f to output the functions
#    e to output the events
# They are output in the order given, if one is given, otherwise in the XML file's order.

import sys

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  if outfilename is not None:
    outf = open(outfilename, "w")
  else:
    outf = sys.stdout

  try:
    if infilename is not None:
      # Output the desired sections
      for letter in infilename:
        for entry in document:
          if entry["cat"][0] == letter:
            outf.write(entry["name"] + "\n")

    else:
      # Output all in the XML file's order
      for entry in document:
        outf.write(entry["name"] + "\n")

  finally:
    if outfilename is not None:
      outf.close()


pass
