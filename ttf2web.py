#!/bin/env python3

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.subset import parse_unicodes, Subsetter

def readSubsetFile(subsetfile):
    subsets = {}
    with open(subsetfile, 'r') as subsethandle:
        for line in subsethandle:
            subname, subrange = line.split()
            unicodes = parse_unicodes(subrange)
            subsets[subname] = (subrange, unicodes)
    return subsets

def getDefaultSubsets():
    subsetfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'subsets')
    return readSubsetFile(subsetfile)

class TTF2Web:
    def __init__(self, fontfile, subsets, assetdir="assets", fontstyle=None, fontweight=None):
        self.fontfile = fontfile
        self.basename = os.path.splitext(os.path.basename(fontfile))[0]
        self.subsets = subsets
        self.assetdir = assetdir

        font = TTFont(fontfile, lazy=True)
        self.fontfamily = font['name'].getDebugName(1)
        subfamily = font['name'].getDebugName(2)
        font.close()

        self.fontstyle = fontstyle
        if fontstyle is None:
            self.fontstyle = 'italic' if subfamily == 'Italic' else 'normal'

        self.fontweight = fontweight
        if fontweight is None:
            self.fontweight = '700' if subfamily == 'Bold' else '400'

    def _writeCssRule(self, handle, url, unicoderange):
        print('@font-face {', file=handle)
        print('\tfont-family: "' + self.fontfamily + '";', file=handle)
        print('\tfont-style: ' + self.fontstyle + ';', file=handle)
        print('\tfont-weight: ' + self.fontweight + ';', file=handle)
        print('\tsrc: local("' + self.fontfamily + '"), ' +
                     'url(' + url + ') format("woff2");', file=handle)
        print('\tunicode-range: ' + unicoderange + ';', file=handle)
        print('}', file=handle)

    def generateCss(self, woff2_list, verbosity=0):
        cssfile = self.basename + '.css'
        with open(cssfile, 'w') as csshandle:
            for woff2_url, subrange in woff2_list:
                self._writeCssRule(csshandle, woff2_url, subrange)
        if verbosity >= 1: print("Generated", cssfile)

    def generateWoff2(self, verbosity=0):
        woff2_list = []
        os.makedirs(self.assetdir, exist_ok=True)
        for subname, (subrange, unicodes) in self.subsets.items():
            if verbosity == 2: print("Processing", subname)
            subs = Subsetter()
            font = TTFont(self.fontfile)
            subs.populate(unicodes=unicodes)
            subs.subset(font)
            cmap = font.getBestCmap()
            glyphcount = len(font.getGlyphOrder()) - 1
            if cmap:
                outfile = os.path.join(self.assetdir,
                                       self.basename + "." + subname + ".woff2")
                font.flavor = 'woff2'
                font.save(outfile)
                woff2_list.append((outfile, subrange))
                if verbosity == 1:
                    print("Generated", outfile)
                elif verbosity == 2:
                    print("  Generated", outfile)
                    print("  Found", glyphcount, "glyphs for",
                          len(cmap), "out of", len(unicodes), "unicodes")
            else:
                if verbosity == 2:
                    print("  Found no glyphs for any of", len(unicodes), "unicodes")
            font.close()
        return woff2_list

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("fontfile",
                        help="ttf file to split into woff2 files")
    parser.add_argument("--unicode-ranges", dest="urfile", default=None,
                        help="the file containing the desired unicode ranges")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print more details")
    args = parser.parse_args()
    if args.urfile:
        subsets = readSubsetFile(args.urfile)
    else:
        subsets = getDefaultSubsets()
    t2w = TTF2Web(args.fontfile, subsets)
    verbosity = 2 if args.verbose else 1
    woff2_list = t2w.generateWoff2(verbosity=verbosity)
    t2w.generateCss(woff2_list, verbosity=verbosity)

if __name__ == '__main__':
    main()
