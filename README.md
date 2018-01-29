# ttf2web

A python script to export a TTF font for the web.

## Usage:

```txt
$ ls
Raleway-Regular.ttf

$ ttf2web.py -v Raleway-Regular.ttf
Processing cyrillic
  Found no glyphs for any of 101 unicodes
Processing cyrillic-ext
  Found no glyphs for any of 348 unicodes
Processing devanagari
  Found no glyphs for any of 213 unicodes
Processing greek
  Generated assets/Raleway-Regular.greek.woff2
  Found 1 glyphs for 1 out of 144 unicodes
Processing greek-ext
  Found no glyphs for any of 256 unicodes
Processing latin
  Generated assets/Raleway-Regular.latin.woff2
  Found 223 glyphs for 218 out of 381 unicodes
Processing latin-ext
  Generated assets/Raleway-Regular.latin-ext.woff2
  Found 156 glyphs for 156 out of 896 unicodes
Processing vietnamese
  Generated assets/Raleway-Regular.vietnamese.woff2
  Found 10 glyphs for 10 out of 95 unicodes
Generated Raleway-Regular.css

$ ls
assets  Raleway-Regular.css  Raleway-Regular.ttf

$ head -n 16 Raleway-Regular.css
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
  unicode-range: U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2212,U+2215;
}
@font-face {
  font-family: "Raleway";
```

The unicode ranges are defined in [`subsets`](./subsets), which you may edit as needed.

## LICENSE

MIT
