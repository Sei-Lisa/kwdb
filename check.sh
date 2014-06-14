#!/bin/bash

function dfg ()
{
  PYTHONPATH=lsl2dfg python lsl2dfg/LSL2dfg.py -d database/kwdb.xml "$@"
}

dfg -ycp
dfg -f rawkeywords -o outputs/rawkeywords.txt # includes dupes
dfg -f rawkeywords -g sl -o outputs/rawkeywords-sl.txt
dfg -f rawkeywords -g os -o outputs/rawkeywords-os.txt
dfg -f rawkeywords -g aa -o outputs/rawkeywords-aa.txt
dfg -f constantvaluecheck -g sl -i inputs/constants-test.lsl.in -o outputs/constants-test-sl.lsl
dfg -f constantvaluecheck -g os -i inputs/constants-test.lsl.in -o outputs/constants-test-os.lsl
dfg -f constantvaluecheck -g aa -i inputs/constants-test.lsl.in -o outputs/constants-test-aa.lsl
dfg -f functioncheck -g sl -i inputs/functioncheck.lsl.in -o outputs/functioncheck-sl.lsl
dfg -f functioncheck -g os -i inputs/functioncheck.lsl.in -o outputs/functioncheck-os.lsl
dfg -f functioncheck -g aa -i inputs/functioncheck.lsl.in -o outputs/functioncheck-aa.lsl
dfg -f constantvalues -g sl -o outputs/constants-sl.txt
dfg -f constantvalues -g os -o outputs/constants-os.txt
dfg -f constantvalues -g aa -o outputs/constants-aa.txt
