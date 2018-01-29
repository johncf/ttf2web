#!/bin/env python3

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.subset import parse_unicodes, Subsetter

def readSubsetFile(subsetfile):
    subsets = []
    with open(subsetfile, 'r') as subsethandle:
        for line in subsethandle:
            subname, subrange = line.split()
            unicodes = parse_unicodes(subrange)
            subsets.append((subname, subrange, unicodes))
    return subsets

def getDefaultSubsets():
    subsetfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'subsets')
    return readSubsetFile(subsetfile)

def writeCssFont(handle, fontfamily, url, unicoderange, fontstyle='normal', fontweight='400'):
    print('@font-face {', file=handle)
    print('  font-family: "' + fontfamily + '";', file=handle)
    print('  font-style: ' + fontstyle + ';', file=handle)
    print('  font-weight: ' + fontweight + ';', file=handle)
    print('  src: local("' + fontfamily + '"), url(' + url + ') format("woff2");', file=handle)
    print('  unicode-range: ' + unicoderange + ';', file=handle)
    print('}', file=handle)

def main(fontfile, assetdir="assets", subsetfile=None, cssfile=None, fontstyle=None, fontweight=None, verbose=False):
    font = TTFont(fontfile, lazy=True)
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
        for subname, subrange, unicodes in subsets:
            outfile = os.path.join(assetdir, basename + "." + subname + ".woff2")
            if verbose: print("Processing", subname)
            subs = Subsetter()
            font = TTFont(fontfile)
            subs.populate(unicodes=unicodes)
            subs.subset(font)
            cmap = font.getBestCmap()
            glyphcount = len(font.getGlyphOrder()) - 1
            if cmap:
                font.flavor = 'woff2'
                font.save(outfile)
                writeCssFont(csshandle, fontfamily, outfile, subrange, fontstyle, fontweight)
                print(("  " if verbose else "") + "Generated", outfile)
                if verbose:
                    print("  Found", glyphcount, "glyphs for",
                          len(cmap), "out of", len(unicodes), "unicodes")
            else:
                if verbose:
                    print("  Found no glyphs for any of", len(unicodes), "unicodes")
            font.close()
        print("Generated", cssfile)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "font-file.ttf", file=sys.stdout)
        sys.exit(1)
    main(sys.argv[1])
