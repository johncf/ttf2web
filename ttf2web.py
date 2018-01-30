#!/bin/env python3

import os
from fontTools.ttLib import TTFont
from fontTools.subset import parse_unicodes, Subsetter

def _intoURDict(uranges):
    urdict = {}
    for urname, urange in uranges:
        unicodes = parse_unicodes(urange)
        urdict[urname] = (urange, unicodes)
    return urdict

def readURFile(urfile):
    with open(urfile, 'r') as urhandle:
        return [line.split() for line in urhandle]

def getDefaultRanges():
    uranges = [['cyrillic',     'U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'],
               ['cyrillic-ext', 'U+0460-052F,U+1C80-1C88,U+20B4,U+2DE0-2DFF,' +
                                'U+A640-A69F,U+FE2E-FE2F'],
               ['devanagari',   'U+0900-097F,U+1CD0-1CF6,U+1CF8-1CF9,U+200B-200D,' +
                                'U+20A8,U+20B9,U+25CC,U+A830-A839,U+A8E0-A8FB'],
               ['greek',        'U+0370-03FF'],
               ['greek-ext',    'U+1F00-1FFF'],
               ['latin',        'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,' +
                                'U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2212,U+2215'],
               ['latin-ext',    'U+0100-024F,U+0259,U+1E00-1EFF,U+20A0-20CF,U+2C60-2C7F,' +
                                'U+A720-A7FF'],
               ['vietnamese',   'U+0102-0103,U+0110-0111,U+1EA0-1EF9,U+20AB']]
    return uranges

class TTF2Web:
    def __init__(self, fontfile, uranges, assetdir="assets", fontstyle=None, fontweight=None):
        """
        Parameters
        ----------
        fontfile : str
            Path to a ttf file.
        uranges : [[str]]
            Array of pairs -- name of the unicode range and the range itself.
            These will be used to suffix the names of generated woff2 files.
            E.g. [['greek', 'U+0370-03FF,U+1F00-1FFF'], ['thumbs', 'U+01F44D']]
                 If   fontfile='/path/to/fontfile.ttf' and assetdir='assets'
                 then 'assets/fontfile.greek.woff2' and
                      'assets/fontfile.thumbs.woff2'
                 will be generated when the generateWoff2 method is called.
        assetdir : str
            Path to which woff2 files should be generated.
        fontstyle : str
            The CSS3 font-style property. If not specified, an appropriate one
            will be generated based on the subfamily property[1].
        fontweight : str
            The CSS3 font-weight property. If not specified, an appropriate one
            will be generated based on the subfamily property[1].

        [1]: https://www.microsoft.com/typography/otspec/name.htm#nameIDs
        """
        self.fontfile = fontfile
        self.basename = os.path.splitext(os.path.basename(fontfile))[0]
        self.urdict = _intoURDict(uranges)
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
        for subname, (subrange, unicodes) in self.urdict.items():
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
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print more details")
    parser.add_argument("--unicode-ranges", dest="urfile", default=None,
                        help="the file specifying the desired unicode ranges. " +
                             "Each line of the file should contain 2 fields " +
                             "separated by one or more spaces. The first field " +
                             "should be a name given to the unicode range " +
                             "specified in the second field.")
    args = parser.parse_args()
    if args.urfile:
        uranges = readURFile(args.urfile)
    else:
        uranges = getDefaultRanges()
    t2w = TTF2Web(args.fontfile, uranges)
    verbosity = 2 if args.verbose else 1
    woff2_list = t2w.generateWoff2(verbosity=verbosity)
    t2w.generateCss(woff2_list, verbosity=verbosity)

if __name__ == '__main__':
    main()
