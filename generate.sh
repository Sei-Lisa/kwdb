#!/bin/bash

function dfg ()
{
  file="$1"
  shift
  test -e "$file" || touch "$file"
  PYTHONPATH=lsl2dfg python lsl2dfg/LSL2dfg.py -u -d database/kwdb.xml "$@" \
   -o "$file".out
  cmp -s <(egrep -v '[Dd]atabase version:|[Oo]utput module version:' "$file".out) \
         <(egrep -v '[Dd]atabase version:|[Oo]utput module version:' "$file") \
    && rm "$file".out || mv -f "$file".out "$file"
}

dfg outputs/en_sl.dic -f dictionary -g sl -i inputs/en_sl.dic.in
dfg outputs/kate2.4_lsl.xml -f kate -g sl -i inputs/kate2.4_lsl.xml.in
dfg outputs/geshi_lsl2.php -f geshi -g sl -i inputs/geshi_lsl2.php.in
dfg outputs/geshi_1.2_lang_lsl2.php -f geshi -g sl -i inputs/geshi_1.2_lang_lsl2.php.in
dfg outputs/FuncSigs.hs -f funcsigshs -g sl -i inputs/FuncSigs.hs.in
dfg outputs/Constants.hs -f constantshs -g sl -i inputs/Constants.hs.in
dfg outputs/builtins.txt -f builtinstxt -g sl
