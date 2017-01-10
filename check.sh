#!/bin/bash

function dfg ()
{
  file="$1"
  shift
  test -e "$file" || touch "$file"
  PYTHONPATH=lsl2dfg python lsl2dfg/LSL2dfg.py -d database/kwdb.xml "$@" \
   -o "$file".out
  cmp -s <(egrep -v '[Dd]atabase version:|[Oo]utput module version:' "$file".out) \
         <(egrep -v '[Dd]atabase version:|[Oo]utput module version:' "$file") \
    && rm "$file".out || mv -f "$file".out "$file"
}

md5sum database/kwdb.xml > database/kwdb.xml.md5

PYTHONPATH=lsl2dfg python lsl2dfg/LSL2dfg.py -d database/kwdb.xml -ycp
dfg outputs/rawkeywords.txt -f rawkeywords # includes dupes
dfg outputs/rawkeywords-sl.txt -f rawkeywords -g sl
dfg outputs/rawkeywords-os.txt -f rawkeywords -g os
dfg outputs/rawkeywords-aa.txt -f rawkeywords -g aa
dfg outputs/constant-test-sl.lsl -f constantvaluecheck -g sl -i inputs/constants-test.lsl.in
dfg outputs/constant-test-os.lsl -f constantvaluecheck -g os -i inputs/constants-test.lsl.in
dfg outputs/constant-test-aa.lsl -f constantvaluecheck -g aa -i inputs/constants-test.lsl.in
dfg outputs/functioncheck-sl.lsl -f functioncheck -g sl -i inputs/functioncheck.lsl.in
dfg outputs/functioncheck-os.lsl -f functioncheck -g os -i inputs/functioncheck.lsl.in
dfg outputs/functioncheck-aa.lsl -f functioncheck -g aa -i inputs/functioncheck.lsl.in
dfg outputs/constants-sl.txt -f constantvalues -g sl
dfg outputs/constants-os.txt -f constantvalues -g os
dfg outputs/constants-aa.txt -f constantvalues -g aa
