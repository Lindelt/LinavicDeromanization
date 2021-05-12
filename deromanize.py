#!/usr/bin/env python3
#coding=utf-8

import argparse
import sys
from itertools import chain

def main (text: list[str], ostream=sys.stdout):
    for entry in text:
        s = entry.lower()
        for (t, r) in chain (
            roman_to_translit_mappings(),
            decompose_mappings(),
            digraph_mappings(),
            alt_mappings(),
            mappings(),
            [("-", "")]
        ): s = s.replace(t, r)
        print(s, file=ostream)

def char_range (a = "a", b = "z"):
    for c in range(ord(a), ord(b) + 1):
        yield chr(c)

def chunk (lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

def roman_to_translit_mappings ():
    trg = (
        [ "ngq", "ngh", "nhg"
        , "gq", "gh", "th"
        , "ng", "nk", "nq"
        , "zq", "zz"
        , "pz", "tz", "cz", "kz", "lz", "z"
        , "jg", "jj", "jd", "jb"
        , "vg", "vj", "vd", "vb", "v"
        ]
    )
    res = (
        [ "ŋŋ'", "ŋw'", "ŋg"
        , "ŋ'", "w'", "ṭ"
        , "ŋ", "ŋk", "ŋq"
        , "ẓ", "ź"
        , "pz", "tz", "cz", "kz", "lz", "s"
        , "xg", "xj", "xd", "xb"
        , "fg", "fj", "fd", "fb", "w"
        ]
    )
    return zip(trg, res)

def decompose_mappings ():
    trg = "áéíóúàèìòù"
    res = chunk("a~e~i~o~u~a`e`i`o`u`", 2)
    return zip(trg, res)

def digraph_mappings ():
    trg = chunk("t!h!n!z!z~2!3!", 2)
    res = "ṭḥŋẓź↊↋"
    return zip(trg, res)

def alt_mappings ():
    trg = "uí̀"
    res = "wy~`"
    return zip(trg, res)

def mappings ():
    trg = "kctpqhxṭfḥsgjdbŋnmwylraeozẓź(),.#'~`/^0123456789↊↋"
    res = chain (
        char_range("\ue000", "\ue01b"),
        char_range("\ue020", "\ue029"),
        char_range("\ue030", "\ue03b")
    )
    return zip(trg, res)

def argparse_setup ():
    parser = argparse.ArgumentParser (
        description="Program which maps latin script Linavic text "
                    "to PUA unicode"
    )
    parser.add_argument (
        '-f', '--file', help="output the results to the given file"
    )
    parser.add_argument (
        'text', nargs='+', help="text to be translated, one line per item"
    )
    return parser

if __name__ == '__main__':
    args = argparse_setup().parse_args()
    if args.file is None:
        main(args.text)
    else:
        with open(args.file, mode='w', encoding='utf-8') as file:
            main(args.text, file)
