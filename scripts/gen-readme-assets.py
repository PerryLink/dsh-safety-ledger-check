#!/usr/bin/env python3
"""Generate README visuals for dsh-safety-ledger-check (docs/assets/).

Outputs (overwritten in place, safe to re-run):

  dsh-safety-ledger-check-hero-{zh,en}-{light,dark}.webp   1440x576, Pillow
      Left column: kicker / title / two value lines / subtitle / meta / footer.
      Right column: one real ledger row from samples/quickstart (Li Qiang,
      16 pre-job hours) with the failing cell flagged, the SL-001 finding card
      that points at row 1 + field trainingHours + Order No. 3 Article 13, and
      the report strip (issues[] 1, skipped[] 0, verdict stays human).

  dsh-safety-ledger-check-flow-v5-{light,dark}.svg         1100x660, hand-written
      Clause alignment, not a five-box pipeline: the ledger's columns on the
      left, the ten implemented criteria in the middle (colour-coded by check
      kind: number / presence / date gap / contains-any), the cited clause on
      the right, grouped into three evidence bands whose ceiling is the
      severity cap (direct <= error, derived-from-principle <= warn,
      institutional-configuration <= info). The bottom band projects issues[]
      and skipped[]; the dashed boundary strip records what the figure does not
      claim: SL-009 not implemented, 1 of 10 ledgers covered, read-only.

The older single-skin assets (flow.svg, flow-{light,dark}.svg, hero.png,
demo.gif, quickstart.*) are deliberately left untouched: they still serve
external deep links. README files reference only the six new files above.
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

# ---------------------------------------------------------------------------
# Palette: family accent + GitHub page backgrounds.
# ---------------------------------------------------------------------------
FAMILY = "#4B67B4"

LIGHT = {
    "bg1": "#f9f6fd",
    "bg2": "#e4eaf8",
    "surface": "#ffffff",
    "surface2": "#f6f3fc",
    "surface3": "#efecf8",
    "border": "#e3dff0",
    "border_strong": "#d2cbe8",
    "text": "#171a2b",
    "sub": "#4d5261",
    "muted": "#6f7487",
    "accent": "#4B67B4",
    "accent_soft": "#cfcdf0",
    "accent_tint": "#ecebfa",
    "error": "#b3261e",
    "error_soft": "#e6b4ae",
    "error_tint": "#fbeae8",
    "warn": "#8f6100",
    "warn_soft": "#e3c48a",
    "warn_tint": "#fbf0da",
    "info": "#4B67B4",
    "info_soft": "#c3c9ea",
    "info_tint": "#ecebfa",
    "ok": "#16794a",
    "ok_tint": "#e5f3eb",
    "kind_number": "#4B67B4",
    "kind_presence": "#2F7F74",
    "kind_date": "#A2691B",
    "kind_contains": "#7457A8",
    "doc60": "#7457A8",
    "shadow": (36, 24, 72, 26),
    "glow": (75, 103, 180, 22),
}

DARK = {
    "bg1": "#131a2a",
    "bg2": "#0c1016",
    "surface": "#1b2335",
    "surface2": "#202a3e",
    "surface3": "#243049",
    "border": "#2c3650",
    "border_strong": "#3a4664",
    "text": "#eef2fb",
    "sub": "#b9c3d8",
    "muted": "#8c97ae",
    "accent": "#8496f5",
    "accent_soft": "#3c4870",
    "accent_tint": "#232b4a",
    "error": "#ff8f86",
    "error_soft": "#6a3634",
    "error_tint": "#3a2024",
    "warn": "#f0bb63",
    "warn_soft": "#6b5430",
    "warn_tint": "#3a2f1c",
    "info": "#8496f5",
    "info_soft": "#39456b",
    "info_tint": "#232b4a",
    "ok": "#5ddba0",
    "ok_tint": "#173a2c",
    "kind_number": "#8496f5",
    "kind_presence": "#58c3b4",
    "kind_date": "#e0a34a",
    "kind_contains": "#b99cf0",
    "doc60": "#b99cf0",
    "shadow": (0, 0, 0, 96),
    "glow": (132, 150, 245, 20),
}

FONT_FILES = {
    "cjk": (r"C:\Windows\Fonts\msyh.ttc", 0),
    "cjk_bold": (r"C:\Windows\Fonts\msyhbd.ttc", 0),
    "mono": (r"C:\Windows\Fonts\consola.ttf", 0),
    "mono_bold": (r"C:\Windows\Fonts\consolab.ttf", 0),
}
for _name, (_path, _index) in FONT_FILES.items():
    if not os.path.exists(_path):
        sys.exit(f"FATAL: missing font for {_name}: {_path}")

_FONTS: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(kind: str, size: float) -> ImageFont.FreeTypeFont:
    size = int(round(size))
    key = (kind, size)
    if key not in _FONTS:
        path, index = FONT_FILES[kind]
        _FONTS[key] = ImageFont.truetype(path, size, index=index)
    return _FONTS[key]


_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def tw(text: str, kind: str, size: int) -> float:
    return _MEASURE.textlength(text, font=font(kind, size))


def need(cond: bool, message: str) -> None:
    if not cond:
        sys.exit(f"FATAL: {message}")


def fit(text: str, kind: str, max_w: float, high: int, low: int, where: str) -> int:
    for size in range(high, low - 1, -1):
        if tw(text, kind, size) <= max_w:
            return size
    sys.exit(f"FATAL: {where} does not fit {max_w}px even at {low}px: {text!r}")


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)
    c1, c2 = hx(top), hx(bottom)
    for y in range(h):
        t = y / (h - 1)
        t = t * t * (3 - 2 * t)  # smoothstep, so the band does not look linear
        colour = tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))
        draw.line([(0, y), (w, y)], fill=colour + (255,))
    return img


def glow(img: Image.Image, cx: int, cy: int, radius: int, colour: str, alpha: int) -> None:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=hx(colour) + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.5))
    img.alpha_composite(layer)


def card(img: Image.Image, box: tuple[int, int, int, int], radius: int, p: dict,
         elevated: bool = True) -> None:
    x0, y0, x1, y1 = box
    if elevated:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.rounded_rectangle([x0 + 2, y0 + 9, x1 + 2, y1 + 9], radius, fill=p["shadow"])
        layer = layer.filter(ImageFilter.GaussianBlur(11))
        img.alpha_composite(layer)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, radius, fill=p["surface"], outline=p["border"], width=1)


def pill(img: Image.Image, x: int, y: int, text: str, kind: str, size: int,
         fg: str, bg: str, border: str | None, pad: int = 12, height: int = 24) -> int:
    w = int(tw(text, kind, size)) + pad * 2
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, x + w, y + height], radius=height / 2, fill=bg,
                           outline=border, width=1)
    draw.text((x + pad, y + height / 2), text, font=font(kind, size), fill=fg, anchor="lm")
    return w


# ---------------------------------------------------------------------------
# Hero copy. Every value below comes from this repository:
#   samples/quickstart/input/SL-001-unsafe.yaml   (Li Qiang, 16 hours, ...)
#   samples/quickstart/expected/result.json       (1 issue, 0 skipped)
#   src/view.ts                                   (finding line shape)
#   rules/safety-ledger-check.yaml                (clause, excerpt, pack 2026.1)
# No other numbers or quotations are invented.
# ---------------------------------------------------------------------------
HERO = {
    "zh": {
        "kicker": "DeepSeek Harness 插件 · 核查器",
        "title": "dsh-safety-ledger-check",
        "value": ("逐行对到条款上", "差异落到行号与字段"),
        "sub": ("核对学时、档案四要素、特种作业证书与实习期；",
                "只列材料内的字面差异，不判合规、不认定责任。"),
        "meta": "规则包 2026.1 · 10 条：7 error / 2 warn / 1 info · SL-009 未实现",
        "foot": "Apache-2.0 · PerryLink DSH plugin family",
        "ledger_title": "台账 · 一人一行",
        "ledger_chip": "rows[] · JSON/YAML",
        "ledger_sub": "安全教育与资格台账 · 一人一条培训记录或证书",
        "ledger_cols": ("姓名", "学时", "证书编号", "有效期至"),
        "ledger_vals": ("李强", "16", "京A0120260001", "2029-01-10"),
        "ledger_caption": "只读原件 · 证书只核编号与有效期，不验真伪",
        "rule": "SL-001",
        "sev": "error",
        "loc": "第1行 · 字段 trainingHours",
        "found": "第 1 行「trainingHours」为 16，小于配置下限 24",
        "clause": "《生产经营单位安全培训规定》· 第十三条",
        "quote": "「生产经营单位新上岗的从业人员，岗前安全培训时间不得少于24学时。」",
        "fix": "建议核对：核对岗前培训学时；本条只比较数值，不判断培训内容是否覆盖大纲",
        "summary": "issues[] 1 条 · skipped[] 0 条",
        "summary_sub": "error 1 · warn 0 · info 0 · 规则集 2026.1",
        "verdict": "结论留给审核人",
    },
    "en": {
        "kicker": "DeepSeek Harness plugin · checker",
        "title": "dsh-safety-ledger-check",
        "value": ("Rows checked against clauses", "gaps pinned to row and field"),
        "sub": ("Hours, the four record elements, certificates, the internship;",
                "literal gaps only — no verdict, no liability."),
        "meta": "ruleset 2026.1 · 10 checks: 7 error / 2 warn / 1 info · SL-009 not implemented",
        "foot": "Apache-2.0 · PerryLink DSH plugin family",
        "ledger_title": "Ledger · one row per person",
        "ledger_chip": "rows[] · JSON/YAML",
        "ledger_sub": "Safety education & qualification ledger · one record per row",
        "ledger_cols": ("Name", "Hours", "Cert no.", "Valid to"),
        "ledger_vals": ("Li Qiang", "16", "京A0120260001", "2029-01-10"),
        "ledger_caption": "Read-only · certificates: number and validity only, never authenticity",
        "rule": "SL-001",
        "sev": "error",
        "loc": "row 1 · field trainingHours",
        "found": "Row 1 sets trainingHours to 16 — below the minimum 24",
        "clause": "The Provisions on Safety Training for Production and Business Units · Order No. 3, Article 13",
        "quote": "「生产经营单位新上岗的从业人员，岗前安全培训时间不得少于24学时。」",
        "fix": "Next: check the pre-job training hours — this rule compares numbers only",
        "summary": "issues[] 1 · skipped[] 0",
        "summary_sub": "error 1 · warn 0 · info 0 · ruleset 2026.1",
        "verdict": "verdict stays human",
    },
}


def hero(lang: str, skin: str) -> None:
    p = LIGHT if skin == "light" else DARK
    h = HERO[lang]
    w, height = 1440, 576
    img = gradient(w, height, p["bg1"], p["bg2"])
    glow(img, 1270, 30, 300, p["accent"], 24 if skin == "light" else 30)
    glow(img, 700, 590, 260, p["accent"], 16 if skin == "light" else 22)
    d = ImageDraw.Draw(img)

    # ---- left column ------------------------------------------------------
    m, col = 64, 624
    ks = 15
    kw = int(tw(h["kicker"], "cjk_bold", ks))
    d.rounded_rectangle([m, 52, m + kw + 36, 88], radius=18, fill=p["accent_tint"],
                        outline=p["accent_soft"], width=1)
    d.text((m + 18, 70), h["kicker"], font=font("cjk_bold", ks), fill=p["accent"], anchor="lm")

    ts = fit(h["title"], "mono_bold", col, 56, 46, "hero title")
    need(ts >= 48, f"hero title must stay >= 48px, got {ts}")
    d.text((m - 2, 158), h["title"], font=font("mono_bold", ts), fill=p["text"], anchor="ls")

    v1, v2 = h["value"]
    vs = min(fit(v1, "cjk_bold", col, 42, 30, "hero value line 1"),
             fit(v2, "cjk_bold", col, 42, 30, "hero value line 2"))
    need(vs >= 32, f"hero value lines too small: {vs}")
    d.text((m, 240), v1, font=font("cjk_bold", vs), fill=p["text"], anchor="ls")
    d.text((m, 296), v2, font=font("cjk_bold", vs), fill=p["text"], anchor="ls")

    s1, s2 = h["sub"]
    ss = min(fit(s1, "cjk", col, 21, 17, "hero sub line 1"),
             fit(s2, "cjk", col, 21, 17, "hero sub line 2"))
    need(ss >= 18, f"hero sub too small: {ss}")
    d.text((m, 344), s1, font=font("cjk", ss), fill=p["sub"], anchor="ls")
    d.text((m, 372), s2, font=font("cjk", ss), fill=p["sub"], anchor="ls")

    ms = fit(h["meta"], "cjk", col, 17, 14, "hero meta")
    need(ms >= 15, f"hero meta too small: {ms}")
    d.text((m, 410), h["meta"], font=font("cjk", ms), fill=p["muted"], anchor="ls")

    d.line([(m, 440), (m + 300, 440)], fill=p["border"], width=1)
    d.text((m, 472), h["foot"], font=font("cjk", 15), fill=p["muted"], anchor="ls")

    # ---- right column: one flagged ledger row -----------------------------
    x0, x1 = 724, 1396
    card(img, (x0, 48, x1, 228), 20, p)
    d = ImageDraw.Draw(img)
    d.text((748, 80), h["ledger_title"], font=font("cjk_bold", 17), fill=p["text"], anchor="ls")
    chip_w = int(tw(h["ledger_chip"], "mono", 12)) + 24
    d.rounded_rectangle([x1 - 24 - chip_w, 62, x1 - 24, 86], radius=12,
                        fill=p["surface2"], outline=p["border"], width=1)
    d.text((x1 - 24 - chip_w + 12, 74), h["ledger_chip"], font=font("mono", 12),
           fill=p["muted"], anchor="lm")
    d.text((748, 108), h["ledger_sub"], font=font("cjk", 13), fill=p["muted"], anchor="ls")

    d.rounded_rectangle([748, 118, 1372, 146], radius=9, fill=p["surface2"])
    cols = ((764, "ls"), (952, "ls"), (1070, "ls"), (1230, "ls"))
    for (cx, _), header in zip(cols, h["ledger_cols"]):
        d.text((cx, 138), header, font=font("cjk_bold", 12.5), fill=p["muted"], anchor="ls")

    # The failing cell is the one SL-001 reads: 学时 / trainingHours.
    d.rounded_rectangle([946, 150, 1012, 184], radius=8, fill=p["error_tint"],
                        outline=p["error_soft"], width=1)
    vals = h["ledger_vals"]
    d.text((764, 174), vals[0], font=font("cjk", 15), fill=p["text"], anchor="ls")
    d.text((962, 174), vals[1], font=font("mono_bold", 17), fill=p["error"], anchor="ls")
    d.text((1070, 174), vals[2], font=font("cjk", 13), fill=p["sub"], anchor="ls")
    d.text((1230, 174), vals[3], font=font("mono", 13), fill=p["sub"], anchor="ls")
    d.text((748, 208), h["ledger_caption"], font=font("cjk", 13), fill=p["muted"], anchor="ls")

    # ---- right column: the finding card ----------------------------------
    card(img, (724, 244, 1396, 424), 20, p)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([740, 258, 744, 410], radius=2, fill=p["error"])
    rw = pill(img, 760, 256, h["rule"], "mono_bold", 12, p["error"], p["error_tint"],
              p["error_soft"], pad=10, height=24)
    d = ImageDraw.Draw(img)
    d.ellipse([760 + rw + 12, 264, 760 + rw + 18, 270], fill=p["error"])
    d.text((760 + rw + 24, 274), h["sev"], font=font("mono_bold", 12), fill=p["error"], anchor="ls")
    d.text((1372, 274), h["loc"], font=font("cjk", 13), fill=p["muted"], anchor="rs")

    fs = fit(h["found"], "cjk", 612, 16, 14, "hero finding")
    d.text((760, 316), h["found"], font=font("cjk", fs), fill=p["text"], anchor="ls")
    cs = fit(h["clause"], "cjk", 612, 14, 11, "hero clause")
    d.text((760, 344), h["clause"], font=font("cjk", cs), fill=p["sub"], anchor="ls")
    d.rounded_rectangle([752, 354, 1372, 386], radius=8, fill=p["surface2"])
    qs = fit(h["quote"], "cjk", 600, 13, 11, "hero quote")
    d.text((766, 374), h["quote"], font=font("cjk", qs), fill=p["sub"], anchor="ls")
    d.text((760, 406), h["fix"], font=font("cjk", 13), fill=p["accent"], anchor="ls")

    # ---- right column: report strip --------------------------------------
    card(img, (724, 440, 1396, 504), 18, p)
    d = ImageDraw.Draw(img)
    d.text((748, 470), h["summary"], font=font("cjk_bold", 16), fill=p["text"], anchor="ls")
    d.text((748, 492), h["summary_sub"], font=font("cjk", 12.5), fill=p["muted"], anchor="ls")
    d.text((1372, 474), h["verdict"], font=font("cjk_bold", 14), fill=p["ok"], anchor="rs")

    name = f"dsh-safety-ledger-check-hero-{lang}-{skin}.webp"
    img.convert("RGB").save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name}")


# ---------------------------------------------------------------------------
# Flow: clause alignment (1100x660 SVG).
# ---------------------------------------------------------------------------
CJK_FONT = "'Microsoft YaHei','PingFang SC','Noto Sans CJK SC','Source Han Sans SC',sans-serif"
MONO_FONT = "'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace"

# rule id, ledger column, criterion, cited clause, actual severity, check kind
ROWS = [
    ("SL-001", "学时 trainingHours", "≥ 24 学时", "令第3号 · 第十三条", "error", "number"),
    ("SL-002", "管理岗学时 managerHours", "≥ 32 学时", "令第3号 · 第九条", "error", "number"),
    ("SL-003", "考核结果 assessResult", "非空", "令第3号 · 第二十二条", "error", "presence"),
    ("SL-004", "培训内容 trainingContent", "非空", "令第3号 · 第二十二条", "error", "presence"),
    ("SL-006", "证书编号 certNo", "非空", "令第60号 · 第三条", "error", "presence"),
    ("SL-007", "发证日期 → 有效期至", "间隔 ≥ 1095 天", "令第60号 · 第十四条", "warn", "dateGap"),
    ("SL-008", "作业日期 / 有效期至", "有效期 − 作业 ≥ 1 天", "令第60号 · 第十四条", "error", "dateGap"),
    ("SL-010", "发证日期 → 独立作业日期", "间隔 ≥ 182 天", "令第60号 · 第二十二条", "error", "dateGap"),
    ("SL-005", "教育级别 educationLevel", "非空 · 适用性存疑", "令第3号 · 第十二条", "warn", "presence"),
    ("SL-011", "姓名 personName", "不含模板占位符", "本机构资料归档办法 · 非法规", "info", "containsAny"),
]

BANDS = [
    ("直接依据 direct · 严重级上限 error", "error", 0, 8, 166, 152, 258, 174),
    ("原则推导 derived-from-principle · 上限 warn", "warn", 8, 9, 426, 412, 48, 434),
    ("机构配置 institutional-configuration · 上限 info", "info", 9, 10, 476, 462, 46, 484),
]


def flow(skin: str) -> str:
    p = LIGHT if skin == "light" else DARK
    w, h = 1100, 660
    kind_colour = {
        "number": p["kind_number"],
        "presence": p["kind_presence"],
        "dateGap": p["kind_date"],
        "containsAny": p["kind_contains"],
    }
    sev_colour = {"error": p["error"], "warn": p["warn"], "info": p["info"]}
    doc_colour = {
        "令第3号": p["accent"],
        "令第60号": p["doc60"],
        "本机构资料归档办法": p["kind_presence"],
    }
    parts: list[str] = []

    def esc(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def add(markup: str) -> None:
        parts.append(markup)

    def text(x: float, y: float, content: str, size: float, fill: str, *,
             font_family: str = CJK_FONT, weight: str | None = None,
             anchor: str | None = None, opacity: float | None = None) -> None:
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'fill="{fill}"',
                 f'font-family="{font_family}"', f'font-size="{size:g}"']
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if anchor:
            attrs.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        add(f'<text {" ".join(attrs)}>{esc(content)}</text>')

    def rect(x: float, y: float, width: float, height: float, *, rx: float = 0,
             fill: str = "none", stroke: str | None = None, sw: float = 1.2,
             dash: str | None = None, opacity: float | None = None,
             filt: str | None = None) -> None:
        attrs = [f'x="{x:g}"', f'y="{y:g}"', f'width="{width:g}"', f'height="{height:g}"',
                 f'rx="{rx:g}"', f'fill="{fill}"']
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw:g}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if filt:
            attrs.append(f'filter="url(#{filt})"')
        add(f'<rect {" ".join(attrs)}/>')

    def line(x1: float, y1: float, x2: float, y2: float, stroke: str, *,
             sw: float = 1.2, dash: str | None = None) -> None:
        attrs = [f'd="M{x1:g} {y1:g} L{x2:g} {y2:g}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw:g}"',
                 'stroke-linecap="round"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        add(f'<path {" ".join(attrs)}/>')

    def connector(x1: float, x2: float, cy: float, dashed: bool) -> None:
        line(x1, cy, x2 - 7, cy, p["muted"], sw=1.3, dash="3 3" if dashed else None)
        add(f'<path d="M{x2 - 7:g} {cy - 3:g} L{x2:g} {cy:g} L{x2 - 7:g} {cy + 3:g}" '
            f'fill="none" stroke="{p["muted"]}" stroke-width="1.3" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="dsh-safety-ledger-check 结构图：'
        f'台账的列 → 十条规则的判据 → 引用的条款号，按证据等级分成三带；'
        f'issues[] 与 skipped[] 两条出口，虚线边界列出 SL-009 未实现与只覆盖一本台账">')
    add('<title>dsh-safety-ledger-check · clause alignment</title>')
    add('<desc>Ledger columns, ten implemented criteria and the article each rule '
        'cites, grouped by evidence kind with the matching severity ceiling; issues[] '
        'and skipped[] leave to the reviewer, and a dashed boundary states the '
        'unimplemented rule and the ledger coverage limit.</desc>')
    add('<defs>')
    add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.28" y2="1">'
        f'<stop offset="0" stop-color="{p["bg1"]}"/>'
        f'<stop offset="1" stop-color="{p["bg2"]}"/></linearGradient>')
    add(f'<filter id="soft" x="-20%" y="-20%" width="140%" height="170%">'
        f'<feDropShadow dx="0" dy="6" stdDeviation="9" '
        f'flood-color="{p["bg2"]}" flood-opacity="0.30"/></filter>')
    add('</defs>')
    add(f'<rect width="{w}" height="{h}" fill="url(#bg)"/>')

    # ---- header -----------------------------------------------------------
    text(44, 54, "dsh-safety-ledger-check", 26, p["text"], font_family=MONO_FONT,
         weight="700")
    tool_w = tw("safety_ledger_check", "mono", 11) + 24
    rect(404, 34, tool_w, 24, rx=12, fill=p["surface2"], stroke=p["border"], sw=1)
    text(416, 51, "safety_ledger_check", 11, p["muted"], font_family=MONO_FONT)

    pack = "规则包 2026.1 · 10 条已实现 · 1 条未实现"
    pack_w = tw(pack, "cjk", 12) + 24
    rect(1056 - pack_w, 33, pack_w, 26, rx=13, fill=p["accent_tint"],
         stroke=p["accent_soft"], sw=1)
    text(1056 - pack_w + 12, 51, pack, 12, p["accent"])

    text(44, 82,
         "一份安全教育与资格台账，逐行对到条款上：差异回行号与字段，未执行的检查写明原因。",
         14, p["sub"])
    line(44, 100, 1056, 100, p["border"], sw=1)

    # ---- column headers ---------------------------------------------------
    text(60, 126, "台账列 · 一人一行", 13, p["text"], weight="700")
    text(360, 126, "规则 · 判据", 13, p["text"], weight="700")
    text(730, 126, "依据条款", 13, p["text"], weight="700")
    text(1044, 126, "级别", 11, p["muted"], anchor="end")

    text(60, 145, "JSON / YAML · rows[] · 一行一人", 11, p["muted"])
    legend_x = 360.0
    for label, key in (("数值", "number"), ("存在", "presence"),
                       ("日期差", "dateGap"), ("占位符", "containsAny")):
        rect(legend_x, 138.5, 7, 7, rx=2, fill=kind_colour[key])
        text(legend_x + 12, 145, label, 11, p["muted"])
        legend_x += 12 + len(label) * 11 + 14
    text(730, 145, "条款号 · 引文逐字核对", 11, p["muted"])

    # ---- three evidence bands with ten criteria --------------------------
    for label, sev, start, end, label_y, rail_y, rail_h, row_y in BANDS:
        text(60, label_y, label, 12, sev_colour[sev], weight="700")
        rect(40, rail_y, 5, rail_h, rx=2.5, fill=sev_colour[sev], opacity=0.85)

        for row in ROWS[start:end]:
            rule, field, criterion, clause, severity, kind = row
            cy = row_y + 12

            # ledger column chip
            rect(60, row_y, 272, 24, rx=7, fill=p["surface2"], stroke=p["border"], sw=1)
            text(72, row_y + 16.5, field, 14, p["text"])

            # rule criterion pill
            rect(360, row_y, 356, 24, rx=7, fill=p["surface"],
                 stroke=p["border_strong"], sw=1)
            rect(360, row_y, 4, 24, rx=2, fill=kind_colour[kind])
            text(376, row_y + 16.5, rule, 14, p["text"], font_family=MONO_FONT, weight="700")
            text(704, row_y + 16.5, criterion, 14, p["sub"], anchor="end")

            # cited clause chip
            rect(730, row_y, 250, 24, rx=7, fill=p["surface2"], stroke=p["border"], sw=1)
            rect(730, row_y, 3, 24, rx=1.5, fill=doc_colour[clause.split(" ")[0]])
            text(744, row_y + 16.5, clause, 14, p["text"])

            # severity: the rule's declared level, not the band ceiling
            add(f'<circle cx="992" cy="{cy:g}" r="4" fill="{sev_colour[severity]}"/>')
            text(1004, row_y + 16.5, severity, 14, sev_colour[severity], weight="700")

            # ledger column -> criterion (dashed: the rule reads it)
            connector(333, 359, cy, dashed=True)
            # criterion -> clause (solid: the rule cites it)
            connector(716, 730, cy, dashed=False)

            row_y += 30

    # ---- output band ------------------------------------------------------
    card_top, card_bottom = 518, 610
    rect(44, card_top, 1012, card_bottom - card_top, rx=18, fill=p["surface"],
         stroke=p["border"], sw=1, filt="soft")
    text(64, 542, "输出 · buildView() 投影", 13, p["text"], weight="700")
    text(1036, 542, "结论留给审核人", 13, p["ok"], weight="700", anchor="end")
    line(64, 552, 1036, 552, p["border"], sw=1)

    rect(64, 560, 70, 18, rx=9, fill=p["error_tint"], stroke=p["error_soft"], sw=1)
    text(74, 573, "issues[]", 11, p["error"], font_family=MONO_FONT, weight="700")
    text(146, 575, "SL-001 [第1行 · 字段 trainingHours] 16 < 24", 13.5, p["text"])
    text(64, 596, "每条带 规则号 · 行号 · 字段 · 条款 · 建议核对", 11, p["muted"])

    line(616, 560, 616, 600, p["border"], sw=1)
    rect(632, 560, 82, 18, rx=9, fill=p["warn_tint"], stroke=p["warn_soft"], sw=1)
    text(642, 573, "skipped[]", 11, p["warn"], font_family=MONO_FONT, weight="700")
    text(726, 575, "缺列 / disabledRules / onlyRules", 13.5, p["text"])
    text(632, 596, "逐条写明原因；空 issues ≠ 没问题", 11, p["muted"])

    # ---- dashed boundary --------------------------------------------------
    rect(44, 618, 1012, 28, rx=14, fill=p["surface2"], stroke=p["muted"], sw=1.1,
         dash="4 4", opacity=0.95)
    boundary_head = "SL-009 未实现"
    text(60, 637, boundary_head, 11, p["warn"], weight="700")
    text(60 + tw(boundary_head, "cjk_bold", 11) + 12, 637,
         "（证书工种 = 实际工种，引擎无文本精确相等判据） · 仅覆盖 1/10 本台账 · "
         "只读 · 无网络 · 不判合规 · 不认定责任", 11, p["muted"])

    add("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        name = f"dsh-safety-ledger-check-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow(skin))
        print(f"wrote {name}")
    print("done: 4 webp + 2 svg in docs/assets/")


if __name__ == "__main__":
    main()
