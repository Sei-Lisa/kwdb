#!/usr/bin/env python

# dictionary.py - This is a LSL2dfg.py output module generating entries in en_sl.dic format.
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


import sys

# Python3 does not have this function, so this replaces it with equivalent behavior.
def cmp(a, b):
  return (a > b) - (a < b)

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  version = "0.0.20230603000"
  str(version) # silence PyFlakes

  keywords = []
  types = []
  constants = []
  functions = []
  events = []

  for element in document:
    if element["cat"] == "keyword":
      keywords.append(element["name"] + "\n")
    elif element["cat"] == "type":
      types.append(element["name"] + "\n")
    elif element["cat"] == "constant":
      if "status" not in element or element["status"] not in ("deprecated", "unimplemented", "godmode"):
        constants.append(element["name"] + "\n")
    elif element["cat"] == "function":
      if "status" not in element or element["status"] not in ("deprecated", "unimplemented", "godmode"):
        functions.append(element["name"] + "\n")
    elif element["cat"] == "event":
      events.append(element["name"] + "\n")

  keywords.sort()
  types.sort()
  constants.sort()
  events.sort()
  try:
    functions.sort(key=lambda x: x.lower())
  except:
    functions.sort(lambda x,y: cmp(x.lower(), y.lower()))

  words = []

  words.extend(types)
  del types
  words.extend(keywords)
  del keywords
  words.extend(functions)
  del functions
  words.extend(events)
  del events
  words.extend(constants)
  del constants

  marker = "<<< %s KEYWORDS >>>" % tag

  if infilename is not None:
    inf = open(infilename, "r")
  else:
    inf = sys.stdin

  try:
    dict = inf.readlines()

  finally:
    if infilename is not None:
      inf.close()

  if outfilename is not None:
    outf = open(outfilename, "w")
  else:
    outf = sys.stdout

  try:
    outf.write(str(len(dict) + len(words) - 2) + "\n")
    for line in dict[1:]:
      if not line.startswith(marker):
        outf.write(line)
      else:
        outf.writelines(words)

  finally:
    if outfilename is not None:
      outf.close()


pass
