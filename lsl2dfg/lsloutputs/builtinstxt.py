#!/usr/bin/env python

# builtinstxt.py - This is a LSL2dfg.py output module that outputs all the
# functions, events and constants in the database with their signatures,
# types and values.
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

  def print_function_or_event(element):
    if element["cat"] in ("function", "event"):

      if element["cat"] == "event":
        func = "event "
      elif "type" in element:
        func = element["type"] + " "
      else:
        func = "void "
      func = func + element["name"] + "( "
      first = True
      if "params" in element:
        for param in element["params"]:
          if first:
            first = False
          else:
            func = func + ", "
          func = func + param["type"] + " " + param["name"]
      func = func + " )\n"

      outf.write(func.encode('utf8'))


  if outfilename is not None:
    outf = open(outfilename, "wb")
  else:
    outf = sys.stdout

  functions = []
  events = []
  constants = []
  for element in document:
    if element["cat"] == "function":
      functions.append(element)
    elif element["cat"] == "event":
      events.append(element)
    elif element["cat"] == "constant":
      constants.append(element)

  try:
    functions.sort(key=lambda x: x["name"])
    events.sort(key=lambda x: x["name"])
    constants.sort(key=lambda x: x["name"])
  except:
    functions.sort(lambda x,y: cmp(x["name"],y["name"]))
    events.sort(lambda x,y: cmp(x["name"],y["name"]))
    constants.sort(lambda x,y: cmp(x["name"],y["name"]))

  try:

    outf.write(("// Generated by LSL2 Derived Files Generator. Database version: %s; output module version: %s\n"
      % (databaseversion, version)).encode('utf8'))

    for element in functions:
      print_function_or_event(element)

    for element in constants:
      val = element['value']
      if element['type'] in ('string', 'key'):
        val = '"' + val.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"') + '"'

      outf.write(('const %s %s = %s\n' % (element['type'], element['name'], val)).encode('utf8'))

    for element in events:
      print_function_or_event(element)

  finally:
    if outfilename is not None:
      outf.close()

pass
