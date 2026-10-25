# Logo spaice „Kurzor“: slovo z písma Archivo (váha 700, šířka 118), písmeno i nahrazuje oranžový kurzor.
# Spuštění (potřebuje fontTools a brotli):  python tools/logo.py
# Výstup: SVG loga a značky a favicon.svg do assets/logo/, tools/logo.json s cestami pro tools/web.py.
# PNG a ICO z nich: viz README.
import json, os
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, 'assets', 'fonts', 'archivo-latin.woff2')
OUT = os.path.join(ROOT, 'assets', 'logo')
INK, PAPER, ACCENT = '#111210', '#f2f0e9', '#c66a3d'
BASE = 800            # účaří v souřadnicích SVG
TRACK = -55           # proklad jako v CSS (-0.055em)
BAR_W = 100           # šířka kurzoru (2/3 tahu písmen)
BAR_TOP, BAR_BOT = 724, -186   # od výšky ascenderu po spodek nožičky p
PAD = 12              # rezerva po stranách


def font(wght, wdth=118):
    f = instancer.instantiateVariableFont(TTFont(FONT), {'wght': wght, 'wdth': wdth})
    return f.getGlyphSet(), f.getBestCmap(), f['hmtx']


def draw(gs, name, dx):
    pen = SVGPathPen(gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
    gs[name].draw(TransformPen(pen, (1, 0, 0, -1, dx, BASE)))
    return pen.getCommands()


def bounds(gs, name):
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    return bp.bounds


def word(left, right, wght=700, bar_w=BAR_W):
    """Písmena vlevo od kurzoru, kurzor (mezery z obou stran vyrovnané) a písmena vpravo."""
    gs, cmap, hmtx = font(wght)
    paths, x = [], 0
    for ch in left:
        n = cmap[ord(ch)]
        paths.append(draw(gs, n, x))
        last_right = x + bounds(gs, n)[2]
        x += hmtx[n][0] + TRACK
    # mezera za kurzorem je stejná jako před ním; vychází z mezery, kterou by zabralo ı
    ni = cmap[ord('ı')]
    x_after = x + hmtx[ni][0] + TRACK
    if right:
        first_left = x_after + bounds(gs, cmap[ord(right[0])])[0]
        gap = (first_left - last_right - bar_w) / 2
    else:
        gap = 61
        first_left = last_right + gap * 2 + bar_w
    bar = (last_right + gap, BASE - BAR_TOP, bar_w, BAR_TOP - BAR_BOT)
    x = x_after
    right_edge = bar[0] + bar_w
    for ch in right:
        n = cmap[ord(ch)]
        paths.append(draw(gs, n, x))
        right_edge = x + bounds(gs, n)[2]
        x += hmtx[n][0] + TRACK
    left_edge = bounds(gs, cmap[ord(left[0])])[0]
    # malá rezerva po stranách, aby vyhlazení krajních písmen nezmizelo na okraji
    box = (left_edge - PAD, BASE - BAR_TOP, right_edge - left_edge + 2 * PAD, BAR_TOP - BAR_BOT)
    return ' '.join(paths), bar, box


def n(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def svg_logo(d, bar, box, color, title='spaice'):
    vb = ' '.join(n(v) for v in box)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'<path d="{d}" fill="{color}"/><rect x="{n(bar[0])}" y="{n(bar[1])}" width="{n(bar[2])}" height="{n(bar[3])}" fill="{ACCENT}"/></svg>\n')


def svg_mark(d, bar, box, size=1024, fill=0.56, radius=0.225, bg=INK, fg=PAPER):
    """Značka: s a kurzor uprostřed čtverce."""
    s = size * fill / box[3]
    w, h = box[2] * s, box[3] * s
    tx = (size - w) / 2 - box[0] * s
    ty = (size - h) / 2 - box[1] * s
    rx = f' rx="{n(size * radius)}"' if radius else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
            f'<rect width="{size}" height="{size}"{rx} fill="{bg}"/>'
            f'<g transform="translate({n(tx)} {n(ty)}) scale({round(s, 5)})">'
            f'<path d="{d}" fill="{fg}"/><rect x="{n(bar[0])}" y="{n(bar[1])}" width="{n(bar[2])}" height="{n(bar[3])}" fill="{ACCENT}"/></g></svg>\n')


def write(name, text, folder=OUT):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
        f.write(text)
    print('ok', name)


d, bar, box = word('spa', 'ce')
write('spaice-logo-na-tmave.svg', svg_logo(d, bar, box, PAPER))
write('spaice-logo-na-svetle.svg', svg_logo(d, bar, box, INK))

md, mbar, mbox = word('s', '')
write('spaice-znacka.svg', svg_mark(md, mbar, mbox))
write('spaice-znacka-ctverec.svg', svg_mark(md, mbar, mbox, radius=0))
# Favicon: v 16 px by tenký kurzor zmizel, proto těžší s a širší kurzor
fd, fbar, fbox = word('s', '', wght=820, bar_w=150)
write('favicon.svg', svg_mark(fd, fbar, fbox, fill=0.62, radius=0.2))

write('logo.json', folder=os.path.join(ROOT, 'tools'), text=json.dumps({'d': d, 'bar': [round(v, 1) for v in bar], 'box': [round(v, 1) for v in box]}))
