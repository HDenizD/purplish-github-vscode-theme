# Purplish — GitHub VS Code theme

A more purple take on GitHub's VS Code theme.

This is a small customization of the excellent
[**GitHub VS Code theme**](https://github.com/primer/github-vscode-theme) by
GitHub / Primer. **All the design and the heavy lifting belongs to the original
theme** — this fork only swaps out a few colors so it leans more purple.

## What's different

Compared to the original `GitHub Dark Default` theme, this version changes only
a few things — everything else stays exactly like the original:

- 🟣 **Primary buttons are purple instead of green** — the green action buttons
  (Comment, Merge, Checkout, etc.) now use `#8345ff`.
- 🌑 **Darker editor background** — the main editor (right side) is `#0d0d0d`
  instead of `#0d1117`.
- 🌑 **Even darker sidebar** — the Explorer / left sidebar is `#080808`, a touch
  darker than the editor so the panels separate nicely.

That's it. The rest of the palette (syntax highlighting, accents, the other
light/dark variants) is untouched and identical to the upstream theme.

## Credits

Full credit goes to the original theme and its authors:

- **Original theme:** [primer/github-vscode-theme](https://github.com/primer/github-vscode-theme)
- **License:** MIT (see [`LICENSE`](LICENSE))

This fork exists purely to make the theme a bit more purple for personal taste.

## Build it yourself

The theme files in `themes/` are generated from the sources in `src/`:

1. Install the dependencies with `yarn` (or `npm install`).
2. Run `yarn build` (or `npm run build`) to regenerate the themes.
3. Press `F5` in VS Code to open a window with the extension loaded, then pick
   the `GitHub Dark Default` theme to see the purple variant.

The color customizations live in [`src/colors.js`](src/colors.js).
