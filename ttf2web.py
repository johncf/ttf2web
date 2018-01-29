#!/bin/env python3

import os
import sys
from fontTools import ttLib
from subprocess import Popen

def readSubsetFile(subsetfile):
    subsets = []
    with open(subsetfile, 'r') as subsethandle:
        for line in subsethandle:
            subset = line.split()
            if len(subset) == 2:
                subsets.append(subset)
            elif len(subset) > 0:
                raise Exception('A line with ' + len(subset) + ' fields found (expected 2) in the subset file')
    return subsets

def getDefaultSubsets():
    subsetfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'subsets')
    return readSubsetFile(subsetfile)

def main(fontfile, assetdir="assets", subsetfile=None, cssfile=None, fontstyle=None, fontweight=None):
    font = ttLib.TTFont(fontfile)
    fontfamily = font['name'].getDebugName(1)
    subfamily = font['name'].getDebugName(2)
    font.close()
    if fontstyle is None:
        fontstyle = 'italic' if subfamily == 'Italic' else 'normal'
    if fontweight is None:
        fontweight = '700' if subfamily == 'Bold' else '400'
    if subsetfile is None:
        subsets = getDefaultSubsets()
    else:
        subsets = readSubsetFile(subsetfile)
    basename = os.path.splitext(os.path.basename(fontfile))[0]
    if cssfile is None:
        cssfile = basename + '.css'
    with open(cssfile, 'w') as csshandle:
        os.makedirs(assetdir, exist_ok=True)
        print("Generating WebFonts...")
        for charset, unicodes in subsets:
            outfile = os.path.join(assetdir, basename + "." + charset + ".woff2")
            print(outfile)
            p = Popen(['pyftsubset', fontfile,
                       '--unicodes=' + unicodes,
                       '--output-file=' + outfile,
                       '--flavor=woff2'], stdout=sys.stdout, stderr=sys.stderr)
            p.communicate()
            print('/* ' + charset + ' */', file=csshandle)
            print('@font-face {', file=csshandle)
            print('  font-family: "' + fontfamily + '";', file=csshandle)
            print('  font-style: "' + fontstyle + '";', file=csshandle)
            print('  font-weight: "' + fontweight + '";', file=csshandle)
            print('  src: local("' + fontfamily + '"), url(' + outfile + ') format("woff2");', file=csshandle)
            print('  unicode-range: ' + unicodes + ';', file=csshandle)
            print('}\n', file=csshandle)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "font-file.ttf", file=sys.stdout)
        sys.exit(1)
    main(sys.argv[1])
