#!/bin/env python3

import os
import sys
from fontTools import ttLib
from subprocess import Popen

def main(fontfile, assetdir="assets", subsetfile=None, cssfile=None):
    font = ttLib.TTFont(fontfile)
    familyname = font['name'].names[1].toStr()
    stylename = font['name'].names[2].toStr()
    font.close()
    basename = os.path.splitext(os.path.basename(fontfile))[0]
    os.makedirs(assetdir, exist_ok=True)
    if subsetfile is None:
        subsetfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'subsets')
    if cssfile is None:
        cssfile = basename + '.css'
    with open(cssfile, 'w') as csshandle, open(subsetfile) as subsethandle:
        print("Generating WebFonts...")
        for subset in subsethandle:
            subset = subset.strip()
            if not subset:
                continue
            charset, unicodes = subset.split()
            outfile = os.path.join(assetdir, basename + "." + charset + ".woff2")
            print(outfile)
            p = Popen(['pyftsubset', fontfile,
                       '--unicodes=' + unicodes,
                       '--output-file=' + outfile,
                       '--flavor=woff2'], stdout=sys.stdout, stderr=sys.stderr)
            p.communicate()
            print('/* ' + charset + ' */', file=csshandle)
            print('@font-face {', file=csshandle)
            print('  font-family: "' + familyname + '";', file=csshandle)
            print('  font-style: "' + stylename + '";', file=csshandle)
            print('  src: local("' + familyname + '"), url(' + outfile + ') format("woff2");', file=csshandle)
            print('  unicode-range: ' + unicodes + ';', file=csshandle)
            print('}\n', file=csshandle)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "font-file.ttf", file=sys.stdout)
        sys.exit(1)
    main(sys.argv[1])
