"""Generate preview mockups for each theme from its real color values.

Renders a small VS Code-like window (activity bar, sidebar, editor with
syntax-highlighted code, status bar) using the colors from themes/*.json, so the
previews are colour-accurate. Output goes to images/preview-<key>.png.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample for crisp text/edges
W, H = 920 * S, 560 * S
AB = 48 * S            # activity bar width
SBW = 220 * S          # sidebar width
TITLE = 34 * S         # title bar height
STATUS = 26 * S        # status bar height
SB_X = AB
ED_X = AB + SBW

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
mono = lambda s: ImageFont.truetype(MONO, s * S)
sans = lambda s: ImageFont.truetype(SANS, s * S)


def hex_to_rgba(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 6:
        h += "ff"
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))


def over(base, top):
    """Alpha-composite top (rgba) over base (rgb)."""
    br, bg, bb = base[:3]
    tr, tg, tb, ta = top
    a = ta / 255
    return (round(tr * a + br * (1 - a)), round(tg * a + bg * (1 - a)), round(tb * a + bb * (1 - a)))


def token(tokens, target):
    """Foreground for the first tokenColor rule whose scope matches target."""
    for pref in (True, False):  # first exact, then substring
        for tc in tokens:
            scopes = tc.get("scope", [])
            if isinstance(scopes, str):
                scopes = [s.strip() for s in scopes.split(",")]
            for sc in scopes:
                if (sc == target) if pref else (target in sc):
                    fg = tc.get("settings", {}).get("foreground")
                    if fg:
                        return hex_to_rgba(fg)
    return None


def build(theme_path, out_path):
    data = json.load(open(theme_path))
    c = data["colors"]
    tok = data["tokenColors"]

    def col(key, fallback="#808080"):
        return hex_to_rgba(c.get(key, fallback))

    fg = col("foreground", "#cccccc")
    ed_bg = col("editor.background", "#1e1e1e")[:3]
    sb_bg = col("sideBar.background", "#252526")[:3]
    ab_bg = col("activityBar.background", "#333333")[:3]
    title_bg = col("titleBar.activeBackground", "#3c3c3c")[:3]
    status_bg = col("statusBar.background", "#007acc")[:3]

    syn = {
        "fg": fg,
        "comment": token(tok, "comment") or (fg[0], fg[1], fg[2], 160),
        "keyword": token(tok, "keyword") or fg,
        "string": token(tok, "string") or fg,
        "func": token(tok, "entity.name.function") or fg,
        "var": token(tok, "variable") or fg,
    }

    img = Image.new("RGB", (W, H), ed_bg)
    d = ImageDraw.Draw(img, "RGBA")

    # --- regions ---
    d.rectangle([0, 0, W, TITLE], fill=title_bg)                       # title bar
    d.rectangle([0, TITLE, AB, H - STATUS], fill=ab_bg)               # activity bar
    d.rectangle([SB_X, TITLE, ED_X, H - STATUS], fill=sb_bg)          # sidebar
    d.rectangle([0, H - STATUS, W, H], fill=status_bg)               # status bar

    # --- title bar text ---
    d.text((ED_X + 16 * S, TITLE / 2), data["name"], font=sans(12),
           fill=col("titleBar.activeForeground", "#cccccc"), anchor="lm")
    # window dots
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        d.ellipse([14 * S + i * 18 * S, TITLE / 2 - 6 * S, 14 * S + i * 18 * S + 12 * S, TITLE / 2 + 6 * S],
                  fill=hex_to_rgba(dot))

    # --- activity bar icons ---
    ab_fg = col("activityBar.foreground", "#ffffff")
    ab_in = col("activityBar.inactiveForeground", "#888888")
    for i in range(5):
        y = TITLE + 22 * S + i * 40 * S
        active = i == 2
        d.rounded_rectangle([AB / 2 - 11 * S, y - 11 * S, AB / 2 + 11 * S, y + 11 * S],
                            radius=5 * S, outline=ab_fg if active else ab_in, width=2 * S)
        if active:
            d.rectangle([0, y - 14 * S, 2 * S, y + 14 * S], fill=col("activityBar.activeBorder", "#ffffff"))
    # SCM badge on the 4th icon
    by = TITLE + 22 * S + 3 * 40 * S
    bx = AB / 2 + 8 * S
    d.ellipse([bx, by - 16 * S, bx + 16 * S, by], fill=col("activityBarBadge.background", "#007acc"))
    d.text((bx + 8 * S, by - 8 * S), "3", font=sans(8), fill=col("activityBarBadge.foreground", "#ffffff"), anchor="mm")

    # --- sidebar ---
    pad = SB_X + 16 * S
    d.text((pad, TITLE + 14 * S), "EXPLORER", font=sans(9), fill=col("descriptionForeground", "#999999"), anchor="lm")
    files = [
        ("▾ src", fg, None, 0),
        ("colors.js", col("gitDecoration.modifiedResourceForeground", "#e2c08d"), "M", 1),
        ("theme.js", fg, None, 1),
        ("index.js", fg, None, 1),
        ("README.md", col("gitDecoration.untrackedResourceForeground", "#73c991"), "U", 0),
    ]
    fy = TITLE + 40 * S
    sel_bg = over(sb_bg, col("list.activeSelectionBackground", "#37373d"))
    for i, (label, color, badge, indent) in enumerate(files):
        rowy = fy + i * 26 * S
        if i == 1:  # selected row
            d.rectangle([SB_X, rowy - 4 * S, ED_X, rowy + 22 * S], fill=sel_bg)
        d.text((pad + indent * 14 * S, rowy + 9 * S), label, font=sans(11), fill=color, anchor="lm")
        if badge:
            d.text((ED_X - 18 * S, rowy + 9 * S), badge, font=sans(10), fill=color, anchor="mm")

    # --- purple primary button (like the SCM commit button) ---
    btn_y = H - STATUS - 52 * S
    d.rounded_rectangle([SB_X + 14 * S, btn_y, ED_X - 14 * S, btn_y + 30 * S], radius=6 * S,
                        fill=col("button.background", "#8345ff"))
    d.text(((SB_X + ED_X) / 2, btn_y + 15 * S), "✓ Commit", font=sans(11),
           fill=col("button.foreground", "#ffffff"), anchor="mm")

    # --- editor: line highlight + code ---
    code = [
        [("// Purplish — a more purple GitHub theme", "comment")],
        [("import", "keyword"), (" { ", "fg"), ("theme", "var"), (" } ", "fg"), ("from", "keyword"),
         (" ", "fg"), ('"purplish"', "string"), (";", "fg")],
        [],
        [("export function", "keyword"), (" ", "fg"), ("greet", "func"), ("(", "fg"), ("name", "var"), (") {", "fg")],
        [("  const", "keyword"), (" ", "fg"), ("msg", "var"), (" = ", "fg"), ('`Hello, ${name}`', "string"), (";", "fg")],
        [("  return", "keyword"), (" ", "fg"), ("greet", "func"), ("(", "fg"), ("name", "var"), (");", "fg")],
        [("}", "fg")],
    ]
    cf = mono(13)
    gut_x = ED_X + 40 * S
    code_x = ED_X + 58 * S
    top = TITLE + 18 * S
    lh = 28 * S
    active_line = 4  # 0-based -> line 5

    # active line highlight across editor
    ay = top + active_line * lh
    d.rectangle([ED_X, ay - 4 * S, W, ay + lh - 4 * S], fill=col("editor.lineHighlightBackground", "#ffffff10"))

    for i, segs in enumerate(code):
        ly = top + i * lh
        d.text((gut_x, ly + 9 * S), str(i + 1), font=mono(12),
               fill=col("editorLineNumber.foreground", "#858585"), anchor="rm")
        x = code_x
        # selection highlight behind "greet" on the return line
        for text, key in segs:
            if i == 5 and text == "greet":
                wsel = cf.getlength(text)
                d.rectangle([x, ly - 2 * S, x + wsel, ly + 20 * S],
                            fill=col("editor.selectionBackground", "#264f78"))
            d.text((x, ly + 9 * S), text, font=cf, fill=syn.get(key, fg), anchor="lm")
            x += cf.getlength(text)
        # cursor at end of active line
        if i == active_line:
            d.rectangle([x + 1 * S, ly - 2 * S, x + 2 * S, ly + 20 * S], fill=col("editorCursor.foreground", "#ffffff"))

    # --- status bar text ---
    st_fg = col("statusBar.foreground", "#ffffff")
    d.text((12 * S, H - STATUS / 2), "⎇ main*", font=sans(10), fill=st_fg, anchor="lm")
    d.text((W - 12 * S, H - STATUS / 2), "Spaces: 2   UTF-8   TypeScript", font=sans(10), fill=st_fg, anchor="rm")

    img.resize((W // S, H // S), Image.LANCZOS).save(out_path)
    print("wrote", out_path)


if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    for key, src in [
        ("light", "themes/light-default.json"),
        ("dark", "themes/dark-default.json"),
        ("dark-purple", "themes/dark-purple.json"),
    ]:
        build(src, f"images/preview-{key}.png")
