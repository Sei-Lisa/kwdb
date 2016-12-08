#!/bin/bash

function dfg ()
{
  python lsl2dfg/LSL2dfg.py -u -d database/kwdb.xml "$@"
}

function replace_if_different ()
{
  if cmp -s "$1" "$2"
    # Don't touch output file if it matches the generated file
    then rm -f "$1"
    else mv -f "$1" "$2"
  fi
}

dfg -f dictionary -g sl -i inputs/en_sl.dic.in \
                       -o outputs/en_sl.dic.out \
 && replace_if_different  outputs/en_sl.dic.out \
                          outputs/en_sl.dic

dfg -f kate -g sl      -i inputs/kate2.4_lsl.xml.in \
                      -o outputs/kate2.4_lsl.xml.out \
 && replace_if_different outputs/kate2.4_lsl.xml.out \
                         outputs/kate2.4_lsl.xml

dfg -f geshi -g sl     -i inputs/geshi_lsl2.php.in \
                      -o outputs/geshi_lsl2.php.out \
 && replace_if_different outputs/geshi_lsl2.php.out \
                         outputs/geshi_lsl2.php

dfg -f geshi -g sl     -i inputs/geshi_1.2_lang_lsl2.php.in \
                      -o outputs/geshi_1.2_lang_lsl2.php.out \
 && replace_if_different outputs/geshi_1.2_lang_lsl2.php.out \
                         outputs/geshi_1.2_lang_lsl2.php

dfg -f funcsigshs -g sl -i inputs/FuncSigs.hs.in \
                       -o outputs/FuncSigs.hs.out \
 && replace_if_different  outputs/FuncSigs.hs.out \
                          outputs/FuncSigs.hs

dfg -f constantshs -g sl -i inputs/Constants.hs.in \
                        -o outputs/Constants.hs.out \
 && replace_if_different   outputs/Constants.hs.out \
                           outputs/Constants.hs

dfg -f builtinstxt -g sl -o outputs/builtins.txt.out \
 && replace_if_different    outputs/builtins.txt.out \
                            outputs/builtins.txt
