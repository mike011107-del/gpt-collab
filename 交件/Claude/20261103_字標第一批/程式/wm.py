"""字標工具：從 OFL 字型取字形輪廓，轉成 shapely 幾何做修改，再輸出 SVG。"""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

_fonts = {}

def font(path):
    if path not in _fonts:
        _fonts[path] = TTFont(path)
    return _fonts[path]


class FlatPen(BasePen):
    def __init__(self, gs, steps=12):
        super().__init__(gs)
        self.contours = []
        self.cur = None
        self.steps = steps

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps
            mt = 1 - t
            x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
            y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
            self.cur.append((x, y))

    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps
            mt = 1 - t
            self.cur.append((mt*mt*p0[0] + 2*mt*t*p1[0] + t*t*p2[0], mt*mt*p0[1] + 2*mt*t*p1[1] + t*t*p2[1]))

    def _closePath(self):
        if self.cur and len(self.cur) > 2:
            self.contours.append(self.cur)
        self.cur = None

    _endPath = _closePath


def glyph(path, ch):
    f = font(path)
    gname = f.getBestCmap()[ord(ch)]
    gs = f.getGlyphSet()
    pen = FlatPen(gs)
    gs[gname].draw(pen)
    geom = Polygon()
    for c in pen.contours:
        p = Polygon(c).buffer(0)
        geom = geom.symmetric_difference(p)
    adv = gs[gname].width
    return geom.buffer(0), adv


def to_path(geom, ndig=1):
    """y 軸翻轉後輸出 SVG path（evenodd）。"""
    if geom.is_empty:
        return ''
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    out = []
    def ring(r):
        pts = list(r.coords)
        return 'M' + 'L'.join(f'{x:.{ndig}f},{-y:.{ndig}f}' for x, y in pts[:-1]) + 'Z'
    for p in polys:
        if p.is_empty or p.geom_type != 'Polygon':
            continue
        out.append(ring(p.exterior))
        out += [ring(i) for i in p.interiors]
    return ''.join(out)


def bbox(geom):
    return geom.bounds  # minx, miny, maxx, maxy


def svg(paths, viewbox, fill='#000', bg=None, extra=''):
    x, y, w, h = viewbox
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    ps = ''.join(f'<path d="{d}" fill="{c or fill}" fill-rule="evenodd"/>' for d, c in paths)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}">{b}{ps}{extra}</svg>'
