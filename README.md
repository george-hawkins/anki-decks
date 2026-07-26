NOTES
=====

When creating my cards, I wanted to see the kanji in a more hand-written style (kyokasho / text book).

Using a font like Klee One on its own results in Latin-1 characters looking overly spaced out (as things are essentially monospaced with the Latin-1 characters being far smaller than the Japanese ones).

In a monospace font, like the default _SF Mono_ used in the macOS Terminal app, the Japanese characters are shrunk down to avoid this issue.

I wanted the relationship in size seen in _SF Mono_ but with the Klee One glyphs used for the Japanese characters.

I looked at doing this with the standard macOS Terminal app and with [iTerm2](https://github.com/gnachman/iterm2).

But in the end, it proved far easier with [Ghostty](https://github.com/ghostty-org/ghostty).

Once installed, I created the directory `~/.config/ghostty` and added the file `~/.config/ghostty/config` containing just:

```
font-family = JetBrains Mono
font-size = 24

# Japanese glyphs come from Klee One; everything else stays on JetBrains Mono.
# Deliberately NOT mapped, because Klee One has these at proportional or
# full-width advances and they would break the grid: Latin-1, curly quotes,
# em-dash, arrows, geometric shapes, box drawing (Ghostty draws those itself).
font-codepoint-map = U+3000-U+303F,U+3040-U+309F,U+30A0-U+30FF,U+31F0-U+31FF=Klee One
font-codepoint-map = U+3400-U+4DBF,U+4E00-U+9FFF,U+F900-U+FAFF=Klee One
font-codepoint-map = U+FF00-U+FFEF=Klee One
```

Note: `13` would be a more normal terminal font size, but I wanted things mucy bigger that usual to make the Japanese characters easier to read.


As I don't like the default darkmode or the blinking cursor, I also added:

```
theme = Apple System Colors Light
cursor-style-blink = false
```

You also need [Klee One](https://fonts.google.com/specimen/Klee+One) and [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) installed (though, as I understand it, Ghostty comes with JetBrains Mono so it shouldn't be an issue).
