# ttf2web

A python script to export a TTF font for the web.

## Usage:

```txt
$ ls
NotoSansMono-Regular.ttf

$ ttf2web.py NotoSansMono-Regular.ttf
Generating WebFonts...
assets/NotoSansMono-Regular.cyrillic.woff2
assets/NotoSansMono-Regular.cyrillic-ext.woff2
assets/NotoSansMono-Regular.devanagari.woff2
assets/NotoSansMono-Regular.greek.woff2
assets/NotoSansMono-Regular.greek-ext.woff2
assets/NotoSansMono-Regular.latin.woff2
assets/NotoSansMono-Regular.latin-ext.woff2
assets/NotoSansMono-Regular.vietnamese.woff2

$ ls
assets  NotoSansMono-Regular.css  NotoSansMono-Regular.ttf

$ cat NotoSansMono-Regular.css
/* cyrillic */
@font-face {
  font-family: "Noto Sans Mono";
  font-style: "Regular";
  src: local("Noto Sans Mono"), url(assets/NotoSansMono-Regular.cyrillic.woff2) format("woff2");
  unicode-range: U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116;
}

/* cyrillic-ext */
@font-face {
  font-family: "Noto Sans Mono";
  font-style: "Regular";
  src: local("Noto Sans Mono"), url(assets/NotoSansMono-Regular.cyrillic-ext.woff2) format("woff2");
  unicode-range: U+0460-052F,U+1C80-1C88,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F;
}

...[truncated]
```

The unicode ranges are defined in [`subsets`](./subsets), which you may edit as needed.

## LICENSE

MIT
