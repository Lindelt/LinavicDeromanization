#!/usr/bin/env python3
#coding=utf-8

import sys
import io
from itertools import chain

def main ():
    outfile = "./output.txt"
    with open (
        outfile,
        mode='w',
        encoding='utf-8'
    ) as f:
        for arg in sys.argv[1:]:
            s = arg.lower()
            for (t, r) in chain (
                roman_to_translit_mappings(),
                decompose_mappings(),
                digraph_mappings(),
                alt_mappings(),
                mappings(),
                [("-", "")]
            ):
                s = s.replace(t, r)
            f.write(f"{s}\n")
        print(outfile)

def char_range (a = "a", b = "z"):
    for c in range(ord(a), ord(b) + 1):
        yield chr(c)

def chunk (lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

def roman_to_translit_mappings ():
    trg = (
        [ "tth", "nng", "ngq", "ngh"
        , "gq", "gh", "th"
        , "nh", "ng", "nk", "nq"
        , "zq", "zz", "v", "z"
        , "pß", "tß", "cß", "kß", "lß", "ß"
        , "jg", "jj", "jd", "jb"
        ]
    )
    res = (
        [ "ṭṭ", "ŋŋ", "ŋg'", "ŋw'"
        , "g'", "w'", "ṭ"
        , "ŋ", "ŋ", "ŋk", "ŋq"
        , "ẓ", "ź", "w", "ß"
        , "pz", "tz", "cz", "kz", "lz"
        , "xg", "xj", "xd", "xb"
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

if __name__ == '__main__':
    main()
