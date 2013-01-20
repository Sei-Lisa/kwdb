#!/bin/bash

function dfg ()
{
  PYTHONPATH=lsl2dfg python lsl2dfg/LSL2dfg.py -d database/kwdb.xml "$@"
}

dfg -ycp
dfg -f rawkeywords -o outputs/rawkeywords.txt
dfg -f constantvaluecheck -g sl -i inputs/constants-test.lsl.in -o outputs/constants-test-sl.lsl
dfg -f constantvaluecheck -g os -i inputs/constants-test.lsl.in -o outputs/constants-test-os.lsl
dfg -f constantvaluecheck -g aa -i inputs/constants-test.lsl.in -o outputs/constants-test-aa.lsl
dfg -f constantvalues -g sl -o outputs/constants-sl.txt
dfg -f constantvalues -g os -o outputs/constants-os.txt
dfg -f constantvalues -g aa -o outputs/constants-aa.txt
