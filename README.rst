ttf2web
=======

A tool to split/segment a TTF file into multiple WOFF2 files based on Unicode
character ranges, and generate a CSS file that describes that font face as an
aggregate of those WOFF2 files.

Installation
------------

.. code::

    pip install ttf2web

Usage
-----

.. code::

    ttf2web /path/to/font-file.ttf

This will split ``font-file.ttf`` based on a set of pre-defined Unicode ranges,
and create (in the working directory) ``font-file.css`` and a directory named
``assets`` containing the WOFF2 files.

Here's a demo of a more complete example:

.. code::

    $ ls
    Raleway-Regular.ttf  unicode-ranges

    $ cat unicode-ranges
    greek         U+0370-03FF
    greek-ext     U+1F00-1FFF
    latin         U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC
    latin-ext     U+0100-024F,U+0259,U+1E00-1EFF,U+20A0-20CF,U+2C60-2C7F,U+A720-A7FF

    $ ttf2web -v --unicode-ranges unicode-ranges Raleway-Regular.ttf
    Processing greek
      Generated assets/Raleway-Regular.greek.woff2
      Found 1 glyphs for 1 out of 144 unicodes
    Processing greek-ext
      Found no glyphs for any of 256 unicodes
    Processing latin
      Generated assets/Raleway-Regular.latin.woff2
      Found 202 glyphs for 197 out of 264 unicodes
    Processing latin-ext
      Generated assets/Raleway-Regular.latin-ext.woff2
      Found 157 glyphs for 157 out of 897 unicodes
    Generated Raleway-Regular.css

    $ ls
    assets  Raleway-Regular.css  Raleway-Regular.ttf  unicode-ranges

    $ head -n 12 Raleway-Regular.css
    @font-face {
            font-family: "Raleway";
            font-style: normal;
            font-weight: 400;
            src: local("Raleway"), url(assets/Raleway-Regular.greek.woff2) format("woff2");
            unicode-range: U+0370-03FF;
    }
    @font-face {
            font-family: "Raleway";
            font-style: normal;
            font-weight: 400;
            src: local("Raleway"), url(assets/Raleway-Regular.latin.woff2) format("woff2");

LICENSE
-------

MIT
