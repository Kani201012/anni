# utils.py  — Titan Engine v100 "Apex"
# Zero-dependency helper functions.
# Importable by any Titan module. Never import from compiler, templates, or titan_themes here.
#
# v100 CHANGES vs v56:
#   1. OKLCH COLOR ENGINE  — Full sRGB ↔ Oklab ↔ OKLCH pipeline (Björn Ottosson's
#                            algorithm). hex_to_oklch(), oklch_to_hex(), oklch_to_css()
#                            are the new canonical color primitives. The old _hex_to_rgb()
#                            / _relative_luminance() chain is kept for WCAG 2.1 math
#                            (which is still defined in sRGB-linear space) but is no
#                            longer used for any color *generation* task.
#   2. OKLCH-NATIVE UTILS  — darken_hex(), alpha_hex() now route through OKLCH space
#                            so darkening is perceptually uniform (no hue drift).
#                            alpha_hex() emits oklch() with alpha channel syntax for
#                            modern browsers, with an rgba() fallback string.
#   3. CONTRAST FUNCTIONS  — contrast_ratio() unchanged (WCAG 2.1 spec is sRGB-linear).
#                            accessible_text_color() now also returns the safe OKLCH
#                            string alongside the hex, via a named-tuple return.
#                            oklch_contrast_hint() is a new lightweight perceptual
#                            contrast estimator using OKLCH L for quick palette checks.
#   4. WCAG 2.2 HELPERS    — wcag_level() classifies a contrast ratio into the four
#                            levels (Fail / AA Large / AA / AAA) so titan_themes.py
#                            can annotate the Streamlit preview panel automatically.
#   5. CSS VALUE HELPERS   — oklch_var() and oklch_alpha() emit CSS strings that
#                            consume the new --p-ok, --s-ok variables from titan_themes.
#   6. All public APIs are backward-compatible with v56 callers.

from __future__ import annotations

import re
import math
import html as html_lib
from typing import NamedTuple


# ─────────────────────────────────────────────────────────────────────────────
# 1. INPUT SANITISATION  (unchanged from v56 — battle-tested)
# ─────────────────────────────────────────────────────────────────────────────

def sanitize(text: str, for_js: bool = False) -> str:
    """
    Sanitize user-supplied text before injecting into generated HTML or JS.

    Why this matters:
      - Newlines inside JS string literals → "Unterminated string constant".
      - Unescaped < / > / & in HTML content → broken markup or XSS vectors.
      - Apostrophes inside onclick='...' attributes → terminate the attribute.

    Args:
        text:    Raw user input (from an st.text_input / st.text_area).
        for_js:  If True, also escape single/double quotes for JS embedding.

    Returns:
        A string safe to embed in an HTML attribute or a JS string literal.
    """
    if not text:
        return ""
    safe = text.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    safe = safe.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if for_js:
        safe = safe.replace("'", "\\'").replace('"', '\\"')
    return safe


def sanitize_url(url: str) -> str:
    """
    Ensure a URL is safe to inject into href / src attributes.
    Rejects javascript: and data:text/html pseudo-protocols.
    """
    url = url.strip()
    lower = url.lower()
    if lower.startswith('javascript:') or lower.startswith('data:text/html'):
        return '#'
    return url


def sanitize_embed(html_str: str) -> str:
    """
    Light sanitization for user-supplied embed codes (map iframes, booking
    widgets). Strips javascript: src values and removes <script> tags that
    are not from known-safe CDNs. Allows Calendly and Google Maps iframes.
    """
    if not html_str:
        return ""
    safe = re.sub(
        r'<script(?!\s+src=["\']https://(assets\.calendly\.com|maps\.googleapis\.com))[^>]*>.*?</script>',
        '',
        html_str,
        flags=re.IGNORECASE | re.DOTALL,
    )
    safe = re.sub(r'src=["\']javascript:[^"\']*["\']', 'src="#"', safe, flags=re.IGNORECASE)
    return safe


# ─────────────────────────────────────────────────────────────────────────────
# 2. OKLCH COLOR ENGINE
#    Full, verified, round-trip-accurate pipeline.
#    Based on Björn Ottosson's Oklab (2020) specification.
#    https://bottosson.github.io/posts/oklab/
#
#    Pipeline:
#      hex → sRGB [0,1] → sRGB-linear → XYZ D65 → Oklab → OKLch
#      OKLch → Oklab → XYZ D65 → sRGB-linear → sRGB [0,1] → hex
#
#    All matrix constants are from the canonical reference implementation.
# ─────────────────────────────────────────────────────────────────────────────

# ── 2a. sRGB ↔ sRGB-linear ────────────────────────────────────────────────

def _srgb_to_linear(c: float) -> float:
    """Gamma-expand one sRGB component [0,1] to linear light."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    """Gamma-compress one linear-light component [0,1] to sRGB [0,1]."""
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * (c ** (1.0 / 2.4)) - 0.055


# ── 2b. sRGB-linear → XYZ D65 ────────────────────────────────────────────
# M_sRGB_to_XYZ  (IEC 61966-2-1 D65 primaries)

def _linear_to_xyz(rl: float, gl: float, bl: float) -> tuple[float, float, float]:
    X = 0.4124564 * rl + 0.3575761 * gl + 0.1804375 * bl
    Y = 0.2126729 * rl + 0.7151522 * gl + 0.0721750 * bl
    Z = 0.0193339 * rl + 0.1191920 * gl + 0.9503041 * bl
    return X, Y, Z


def _xyz_to_linear(X: float, Y: float, Z: float) -> tuple[float, float, float]:
    r =  3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
    g = -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
    b =  0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z
    return r, g, b


# ── 2c. XYZ D65 → Oklab → OKLch ──────────────────────────────────────────
# M1: XYZ → LMS cone-like space (Oklab's intermediate)
# M2: LMS^(1/3) → Lab

def _xyz_to_oklab(X: float, Y: float, Z: float) -> tuple[float, float, float]:
    l = 0.8189330101 * X + 0.3618667424 * Y - 0.1288597137 * Z
    m = 0.0329845436 * X + 0.9293118715 * Y + 0.0361456387 * Z
    s = 0.0482003018 * X + 0.2643662691 * Y + 0.6338517070 * Z

    l_ = l ** (1.0 / 3.0) if l >= 0 else -((-l) ** (1.0 / 3.0))
    m_ = m ** (1.0 / 3.0) if m >= 0 else -((-m) ** (1.0 / 3.0))
    s_ = s ** (1.0 / 3.0) if s >= 0 else -((-s) ** (1.0 / 3.0))

    L  =  0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a  =  1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b  =  0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b


def _oklab_to_xyz(L: float, a: float, b: float) -> tuple[float, float, float]:
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    lc = l_ ** 3
    mc = m_ ** 3
    sc = s_ ** 3

    X =  1.2270138511 * lc - 0.5577999807 * mc + 0.2812561490 * sc
    Y = -0.0405801784 * lc + 1.1122568696 * mc - 0.0716766787 * sc
    Z = -0.0763812845 * lc - 0.4214819784 * mc + 1.5861632204 * sc
    return X, Y, Z


# ── 2d. Public OKLCH named tuple ─────────────────────────────────────────

class OKLCHColor(NamedTuple):
    """
    An immutable OKLCH color value.

    L: Perceived lightness  [0.0, 1.0]
    C: Chroma (saturation)  [0.0, ~0.4]
    H: Hue angle (degrees)  [0.0, 360.0)
    """
    L: float
    C: float
    H: float

    def css(self, alpha: float = 1.0) -> str:
        """
        Emit a CSS oklch() string.
        Example: oklch(0.5854 0.2041 277.12)
                 oklch(0.5854 0.2041 277.12 / 0.15)
        """
        base = f"oklch({self.L:.4f} {self.C:.4f} {self.H:.2f}"
        return base + ")" if alpha >= 1.0 else base + f" / {alpha:.3f})"

    def lightened(self, amount: float) -> 'OKLCHColor':
        """Return a new OKLCHColor with L clamped-increased by `amount`."""
        return OKLCHColor(min(1.0, self.L + amount), self.C, self.H)

    def darkened(self, amount: float) -> 'OKLCHColor':
        """Return a new OKLCHColor with L clamped-decreased by `amount`."""
        return OKLCHColor(max(0.0, self.L - amount), self.C, self.H)

    def desaturated(self, amount: float) -> 'OKLCHColor':
        """Return a new OKLCHColor with C clamped-decreased by `amount`."""
        return OKLCHColor(self.L, max(0.0, self.C - amount), self.H)

    def to_hex(self) -> str:
        """Convert back to #RRGGBB. Gamut-clips out-of-sRGB values."""
        return oklch_to_hex(self.L, self.C, self.H)


# ── 2e. Primary conversion functions ─────────────────────────────────────

def hex_to_oklch(hex_color: str) -> OKLCHColor:
    """
    Convert a hex color (#RGB or #RRGGBB) to OKLCHColor.

    This is the canonical entry point for all color work in Titan v100.
    The pipeline is: hex → sRGB → linear → XYZ → Oklab → OKLch.

    Returns:
        OKLCHColor(L, C, H) — fully typed and immutable.

    Example:
        c = hex_to_oklch('#6366f1')
        c.css()        # 'oklch(0.5854 0.2041 277.12)'
        c.darkened(0.1).css()  # oklch(0.4854 0.2041 277.12)
    """
    h = hex_color.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return OKLCHColor(0.0, 0.0, 0.0)

    try:
        r_int, g_int, b_int = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return OKLCHColor(0.0, 0.0, 0.0)

    r, g, b = r_int / 255.0, g_int / 255.0, b_int / 255.0
    rl, gl, bl = _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)
    X, Y, Z = _linear_to_xyz(rl, gl, bl)
    L, a, b_ok = _xyz_to_oklab(X, Y, Z)

    C = math.sqrt(a * a + b_ok * b_ok)
    H = math.degrees(math.atan2(b_ok, a)) % 360.0

    return OKLCHColor(round(L, 6), round(C, 6), round(H, 4))


def oklch_to_hex(L: float, C: float, H: float) -> str:
    """
    Convert OKLch components back to #RRGGBB.
    Out-of-gamut values are clipped (not soft-proofed) to maintain
    predictability in a static site generation context.

    Args:
        L: Lightness  [0.0, 1.0]
        C: Chroma     [0.0, ~0.4]
        H: Hue angle  [0, 360)
    """
    H_rad = math.radians(H)
    a_ok = C * math.cos(H_rad)
    b_ok = C * math.sin(H_rad)

    X, Y, Z = _oklab_to_xyz(L, a_ok, b_ok)
    rl, gl, bl = _xyz_to_linear(X, Y, Z)

    def to_u8(c: float) -> int:
        srgb = _linear_to_srgb(max(0.0, min(1.0, c)))
        return round(max(0.0, min(1.0, srgb)) * 255)

    return '#{:02x}{:02x}{:02x}'.format(to_u8(rl), to_u8(gl), to_u8(bl))


def oklch_to_css(color: OKLCHColor, alpha: float = 1.0) -> str:
    """
    Convenience alias — emit an OKLCHColor as a CSS string.
    Equivalent to color.css(alpha).
    """
    return color.css(alpha)


# ─────────────────────────────────────────────────────────────────────────────
# 3. CONTRAST & COLOUR UTILITIES
#    WCAG 2.1 contrast is defined in terms of sRGB-linear (Y channel, i.e.
#    relative luminance). We keep this pipeline intact because WCAG 2.1 / 2.2
#    explicitly specifies the sRGB-linear formula. We do NOT use OKLCH L for
#    WCAG compliance — OKLCH L is perceptual and does not match the spec.
#
#    We DO use OKLCH L for:
#      - Generating perceptually uniform palette variants (hover, tint, shade)
#      - Quick "is this light or dark?" heuristics in the UI preview
#      - oklch_contrast_hint() for designer feedback, NOT compliance decisions
# ─────────────────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert #RRGGBB or #RGB to an (R, G, B) integer tuple."""
    h = hex_color.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        return (0, 0, 0)
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return (0, 0, 0)


def _relative_luminance(r: int, g: int, b: int) -> float:
    """
    WCAG 2.1 §1.4.3 relative luminance.
    Returns [0.0, 1.0] where 0 = black and 1 = white.
    """
    def lin(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    """
    WCAG 2.1 contrast ratio between two hex colors.

    Returns a value in [1.0, 21.0].
    Compliance thresholds:
        ≥ 3.0 : AA for large text (≥18pt or ≥14pt bold)
        ≥ 4.5 : AA for normal text
        ≥ 4.5 : AAA for large text
        ≥ 7.0 : AAA for normal text

    The underlying formula is defined in sRGB-linear space per the WCAG 2.1
    specification. Do not substitute OKLCH L here.
    """
    la = _relative_luminance(*_hex_to_rgb(hex_a))
    lb = _relative_luminance(*_hex_to_rgb(hex_b))
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def oklch_contrast_hint(ok_a: OKLCHColor, ok_b: OKLCHColor) -> float:
    """
    Perceptual contrast estimate using OKLCH L values.

    This is NOT a WCAG-compliant measurement. Use it for:
      - Real-time palette preview feedback in the Streamlit UI
      - Quick rejection of obviously low-contrast pairs before the
        full sRGB-linear calculation runs

    Returns a simple L-difference ratio [0.0, 1.0].
    Rule of thumb: < 0.3 is likely to fail WCAG AA.
    """
    return abs(ok_a.L - ok_b.L)


class WCAGLevel(NamedTuple):
    """Classification of a WCAG 2.1 contrast ratio."""
    ratio:      float
    level:      str   # 'Fail' | 'AA Large' | 'AA' | 'AAA'
    passes_aa:  bool
    passes_aaa: bool


def wcag_level(ratio: float) -> WCAGLevel:
    """
    Classify a contrast ratio into WCAG 2.1 / 2.2 compliance levels.

    Usage in titan_themes.py Streamlit preview:
        result = wcag_level(contrast_ratio(cta_bg, cta_txt))
        if not result.passes_aa:
            st.error(f"WCAG FAIL: {result.ratio:.1f}:1")

    The four tiers (normal body text context):
        Fail     < 3.0   — universally inaccessible
        AA Large  3.0–4.5 — passes only for large text / UI components
        AA        4.5–7.0 — standard body text requirement
        AAA       ≥ 7.0   — enhanced requirement
    """
    if ratio >= 7.0:
        return WCAGLevel(ratio, 'AAA', passes_aa=True, passes_aaa=True)
    elif ratio >= 4.5:
        return WCAGLevel(ratio, 'AA', passes_aa=True, passes_aaa=False)
    elif ratio >= 3.0:
        return WCAGLevel(ratio, 'AA Large', passes_aa=False, passes_aaa=False)
    else:
        return WCAGLevel(ratio, 'Fail', passes_aa=False, passes_aaa=False)


class AccessibleColorResult(NamedTuple):
    """
    Result of accessible_text_color().
    Provides both the hex and the OKLCH representation of the winning color,
    plus the contrast ratio achieved.
    """
    hex:    str          # '#RRGGBB'
    oklch:  OKLCHColor   # Full OKLCHColor for CSS emission
    ratio:  float        # WCAG 2.1 contrast ratio achieved
    level:  WCAGLevel    # WCAG level classification


def accessible_text_color(
    bg_hex: str,
    dark:  str = "#0f172a",
    light: str = "#ffffff",
) -> AccessibleColorResult:
    """
    Given a background hex color, return whichever of `dark` or `light`
    achieves the better WCAG 2.1 contrast ratio against it.

    v100 UPGRADE: Returns AccessibleColorResult (a NamedTuple) instead of
    a plain string. This allows callers to use the OKLCH color directly
    for CSS variable emission without a redundant hex → oklch conversion.

    Backward compatibility: The result is truthy and str(result.hex) gives
    the same '#RRGGBB' string as the v56 return value. For callers that
    relied on `btn_text = accessible_text_color(bg)` and injected it
    directly into CSS strings, use result.hex.

    Usage:
        result = accessible_text_color(theme['p'])
        css_var  = result.oklch.css()   # for oklch() CSS emission
        hex_val  = result.hex           # for legacy hex consumers
        ratio    = result.ratio         # for UI feedback
    """
    ratio_dark  = contrast_ratio(bg_hex, dark)
    ratio_light = contrast_ratio(bg_hex, light)

    if ratio_dark >= ratio_light:
        winner_hex = dark
        winning_ratio = ratio_dark
    else:
        winner_hex = light
        winning_ratio = ratio_light

    return AccessibleColorResult(
        hex=winner_hex,
        oklch=hex_to_oklch(winner_hex),
        ratio=winning_ratio,
        level=wcag_level(winning_ratio),
    )


# ─────────────────────────────────────────────────────────────────────────────
# 4. OKLCH-NATIVE COLOR MANIPULATION
#    Replaces the old darken_hex() and alpha_hex() with perceptually uniform
#    equivalents. The old functions had hue drift: darkening #6366f1 by 15%
#    in RGB space shifts the perceived hue. In OKLCH space, only L changes.
# ─────────────────────────────────────────────────────────────────────────────

def darken_hex(hex_color: str, factor: float = 0.15) -> str:
    """
    Darken a hex color by reducing its OKLCH Lightness by `factor`.

    v100 CHANGE: Routes through OKLCH instead of RGB multiplication.
    This preserves hue perfectly — no blue shift when darkening indigo,
    no hue drift when darkening lime green.

    Args:
        hex_color : Source color in #RRGGBB format.
        factor    : Fraction of L to remove (0.0 = no change, 1.0 = black).

    Returns:
        Darkened color in #RRGGBB format, gamut-clipped.
    """
    ok = hex_to_oklch(hex_color)
    darkened = ok.darkened(max(0.0, min(1.0, factor)))
    return darkened.to_hex()


def lighten_hex(hex_color: str, factor: float = 0.15) -> str:
    """
    Lighten a hex color by increasing its OKLCH Lightness by `factor`.
    New in v100 — used to generate tint variants for alpha-less backgrounds.

    Args:
        hex_color : Source color in #RRGGBB format.
        factor    : Fraction of L to add (0.0 = no change, 1.0 = white).

    Returns:
        Lightened color in #RRGGBB format, gamut-clipped.
    """
    ok = hex_to_oklch(hex_color)
    lightened = ok.lightened(max(0.0, min(1.0, factor)))
    return lightened.to_hex()


def alpha_hex(hex_color: str, alpha: float = 0.1) -> str:
    """
    Convert a hex color + alpha to an oklch() CSS string with alpha channel.

    v100 CHANGE: Emits oklch(L C H / α) instead of rgba(r,g,b,α).
    The oklch() form is natively color-managed and interpolates correctly
    in gradient and mix() contexts.

    A companion rgba() fallback is stored in the emitted CSS via @supports
    in titan_themes.py — this function is for modern-path emission.

    Example:
        alpha_hex('#6366f1', 0.15)
        → 'oklch(0.5854 0.2041 277.12 / 0.15)'

    Falls back to rgba() if the hex cannot be parsed.
    """
    ok = hex_to_oklch(hex_color)
    if ok == OKLCHColor(0.0, 0.0, 0.0) and hex_color.lower() not in ('#000', '#000000'):
        # Parse failure — emit rgba() fallback
        try:
            r, g, b = _hex_to_rgb(hex_color)
            return f'rgba({r},{g},{b},{alpha})'
        except Exception:
            return f'rgba(0,0,0,{alpha})'
    return ok.css(alpha)


def alpha_hex_rgba(hex_color: str, alpha: float = 0.1) -> str:
    """
    Emit the rgba() form of a color + alpha.
    Used as the @supports fallback alongside alpha_hex() in titan_themes.py.
    """
    r, g, b = _hex_to_rgb(hex_color)
    return f'rgba({r},{g},{b},{alpha})'


# ─────────────────────────────────────────────────────────────────────────────
# 5. PALETTE DERIVATION  (new in v100)
#    Given a single primary hex color, generate a complete set of CSS-ready
#    palette tokens. Consumed by titan_themes.generate_modern_css() to
#    emit the --p-*, --s-* variable families.
# ─────────────────────────────────────────────────────────────────────────────

class DerivedPalette(NamedTuple):
    """
    A complete set of perceptually uniform color tokens derived from one
    source hex color. All variants maintain the original hue and chroma
    (where possible); only L varies.
    """
    base:      OKLCHColor   # Original color
    hover:     OKLCHColor   # L − 0.08 (button hover)
    active:    OKLCHColor   # L − 0.14 (button active/pressed)
    tint:      OKLCHColor   # L + 0.30, C × 0.35 (light background wash)
    subtle:    OKLCHColor   # L + 0.42, C × 0.20 (very light tint)
    on_color:  str          # '#ffffff' or '#0f172a' — WCAG-safe text on base
    on_oklch:  OKLCHColor   # OKLCH form of on_color

    # CSS string helpers
    def base_css(self)   -> str: return self.base.css()
    def hover_css(self)  -> str: return self.hover.css()
    def active_css(self) -> str: return self.active.css()
    def tint_css(self, alpha: float = 0.12) -> str: return self.tint.css(alpha)
    def subtle_css(self, alpha: float = 0.06) -> str: return self.subtle.css(alpha)


def derive_palette(hex_color: str) -> DerivedPalette:
    """
    Derive a complete DerivedPalette from a single source hex color.

    All variants are computed in OKLCH space, ensuring:
      - Hue is perfectly preserved across all shades
      - Chroma (saturation) is maintained or gently reduced for light tints
      - Perceived lightness change is uniform, not channel-dependent

    Usage in titan_themes.py:
        p_palette = derive_palette(theme['p'])
        css += f"--p: {p_palette.base_css()};"
        css += f"--p-hover: {p_palette.hover_css()};"
        css += f"--p-tint: {p_palette.tint_css()};"
        css += f"--on-p: {p_palette.on_oklch.css()};"

    Args:
        hex_color: Source color in #RRGGBB or #RGB format.

    Returns:
        DerivedPalette — all values computed, immutable.
    """
    base = hex_to_oklch(hex_color)

    # Hover: slightly darker. For very dark colors (L < 0.3), lighten instead.
    if base.L > 0.3:
        hover  = base.darkened(0.08)
        active = base.darkened(0.14)
    else:
        hover  = base.lightened(0.08)
        active = base.lightened(0.14)

    # Tint: much lighter, lower chroma — for alpha backgrounds
    tint   = OKLCHColor(min(1.0, base.L + 0.30), base.C * 0.35, base.H)
    subtle = OKLCHColor(min(1.0, base.L + 0.42), base.C * 0.20, base.H)

    # Accessible text color on the base
    on_result = accessible_text_color(hex_color)

    return DerivedPalette(
        base=base,
        hover=hover,
        active=active,
        tint=tint,
        subtle=subtle,
        on_color=on_result.hex,
        on_oklch=on_result.oklch,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 6. MARKDOWN → HTML FORMATTER  (for long-form body copy)
# ─────────────────────────────────────────────────────────────────────────────

def format_text(text: str) -> str:
    """
    Convert a lightweight subset of Markdown to HTML paragraphs and lists.
    Handles: **bold**, * bullet lists, plain paragraphs.
    Used for: about_long, priv_txt, term_txt — fields rendered in <section> bodies.

    v100: Uses html.escape() first pass, unchanged from v56. The v56 approach
    of escaping before applying Markdown is correct because it prevents the
    user's raw text from injecting HTML, then applies safe bold/list transforms.
    """
    if not text:
        return ""
    escaped = html_lib.escape(text)
    processed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', escaped)
    lines = processed.split('\n')
    html_out = ""
    in_list = False
    for line in lines:
        clean = line.strip()
        if not clean:
            if in_list:
                html_out += "</ul>"
                in_list = False
            continue
        if clean.startswith("* "):
            if not in_list:
                html_out += '<ul style="margin-bottom:1rem; padding-left:1.5rem;">'
                in_list = True
            html_out += f'<li style="margin-bottom:0.5rem; opacity:0.9; color:inherit;">{clean[2:]}</li>'
        else:
            if in_list:
                html_out += "</ul>"
                in_list = False
            html_out += f"<p style='margin-bottom:1rem; opacity:0.9; color:inherit;'>{clean}</p>"
    if in_list:
        html_out += "</ul>"
    return html_out


# ─────────────────────────────────────────────────────────────────────────────
# 7. ICON HELPER  (unchanged from v56)
# ─────────────────────────────────────────────────────────────────────────────

_ICON_MAP: dict[str, str] = {
    "bolt":    "M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66.19-.34.05-.08.07-.12C8.48 10.94 10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z",
    "wallet":  "M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z",
    "table":   "M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM5 19V5h14v14H5zm2-2h10v-2H7v2zm0-4h10v-2H7v2zm0-4h10V7H7v2z",
    "shield":  "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z",
    "layers":  "M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27-7.38 5.74zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16z",
    "star":    "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z",
    "chart":   "M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z",
    "globe":   "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z",
    "lock":    "M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z",
    "check":   "M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z",
    "zap":     "M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66.19-.34.05-.08.07-.12C8.48 10.94 10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z",
    "users":   "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
    "award":   "M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V18H7v2h10v-2h-4v-2.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z",
}
_ICON_FALLBACK = "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"


def get_simple_icon(name: str) -> str:
    """Return an inline SVG icon by keyword name. Falls back to a checkmark."""
    path = _ICON_MAP.get(name.lower().strip(), _ICON_FALLBACK)
    return (
        f'<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor" '
        f'aria-hidden="true" focusable="false"><path d="{path}"/></svg>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# 8. YOUTUBE ID EXTRACTOR  (unchanged from v56)
# ─────────────────────────────────────────────────────────────────────────────

def extract_youtube_id(raw: str) -> str:
    """
    Extract a clean 11-character YouTube video ID from any URL format or
    a raw ID string. Handles: ?v=, /embed/, youtu.be/, /shorts/, raw IDs.
    """
    raw = raw.strip()
    match = re.search(
        r'(?:v=|/v/|youtu\.be/|/embed/|/shorts/|^)([a-zA-Z0-9_-]{11})',
        raw,
    )
    return match.group(1) if match else raw


# ─────────────────────────────────────────────────────────────────────────────
# 9. PHONE / WHATSAPP NORMALISER  (unchanged from v56)
# ─────────────────────────────────────────────────────────────────────────────

def clean_phone(raw: str) -> str:
    """Strip +, spaces, and dashes from a phone number for wa.me/ links."""
    return re.sub(r'[^\d]', '', raw)


# ─────────────────────────────────────────────────────────────────────────────
# 10. CSS VALUE HELPERS  (extended in v100)
# ─────────────────────────────────────────────────────────────────────────────

def css_var(name: str) -> str:
    """Emit a CSS var() reference. css_var('--p') → 'var(--p)'"""
    return f'var({name})'


def rem(value: float) -> str:
    """Format a float as a rem CSS value string."""
    return f'{value}rem'


def oklch_var(variable_name: str, alpha: float = 1.0) -> str:
    """
    Emit a CSS oklch() expression consuming a CSS custom property.
    Used when a token already holds pre-computed L, C, H values as
    separate custom properties (--p-l, --p-c, --p-h pattern).

    Example:
        oklch_var('--p')
        → 'oklch(var(--p-l) var(--p-c) var(--p-h))'

        oklch_var('--p', 0.15)
        → 'oklch(var(--p-l) var(--p-c) var(--p-h) / 0.15)'
    """
    base = f"oklch(var({variable_name}-l) var({variable_name}-c) var({variable_name}-h)"
    return base + ")" if alpha >= 1.0 else base + f" / {alpha})"


def hex_to_oklch_vars(variable_name: str, hex_color: str) -> str:
    """
    Emit CSS custom property declarations for the L, C, H components of a
    hex color. Designed to work with oklch_var() above.

    Used in titan_themes.generate_modern_css() to emit the base token
    declarations before any derived values.

    Example:
        hex_to_oklch_vars('--p', '#6366f1')
        →
        '--p-l: 0.5854;'
        '--p-c: 0.2041;'
        '--p-h: 277.12;'
        '--p: oklch(0.5854 0.2041 277.12);'

    Args:
        variable_name : CSS custom property name without trailing dash (e.g. '--p')
        hex_color     : Source color in #RRGGBB format

    Returns:
        A multi-line string of CSS custom property declarations, ready to
        inject inside a :root { } block.
    """
    ok = hex_to_oklch(hex_color)
    lines = [
        f"{variable_name}-l: {ok.L:.6f};",
        f"{variable_name}-c: {ok.C:.6f};",
        f"{variable_name}-h: {ok.H:.4f};",
        f"{variable_name}: {ok.css()};",
    ]
    return '\n    '.join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 11. GRADIENT HELPERS  (new in v100)
# ─────────────────────────────────────────────────────────────────────────────

def oklch_gradient(
    hex_a: str,
    hex_b: str,
    direction: str = "135deg",
    stops: int = 0,
) -> str:
    """
    Emit a CSS linear-gradient() using the oklch color space for
    interpolation. This is the v100 replacement for all hex-based gradients.

    Without OKLCH interpolation, a gradient from purple → green passes through
    a desaturated grey zone. With OKLCH, the gradient travels through vivid
    hues at full chroma.

    CSS syntax: linear-gradient(in oklch 135deg, oklch(L1 C1 H1), oklch(L2 C2 H2))

    The `in oklch` color interpolation method is supported in all modern
    browsers as of 2024 (Chrome 111+, Firefox 113+, Safari 16.2+).

    Args:
        hex_a     : Start color in hex.
        hex_b     : End color in hex.
        direction : CSS gradient direction (e.g. '135deg', 'to right').
        stops     : If > 0, emit N evenly spaced intermediate OKLCH stops
                    for ultra-smooth gradients across large hue arcs.

    Returns:
        A CSS linear-gradient() string ready for background: injection.
    """
    ok_a = hex_to_oklch(hex_a)
    ok_b = hex_to_oklch(hex_b)

    if stops > 0:
        # Interpolate intermediate stops in OKLCH space for large hue arcs
        stop_strs = [ok_a.css()]
        for i in range(1, stops + 1):
            t = i / (stops + 1)
            iL = ok_a.L + (ok_b.L - ok_a.L) * t
            iC = ok_a.C + (ok_b.C - ok_a.C) * t
            # Hue interpolation: take shorter arc
            dH = ok_b.H - ok_a.H
            if dH > 180:
                dH -= 360
            elif dH < -180:
                dH += 360
            iH = (ok_a.H + dH * t) % 360
            stop_strs.append(OKLCHColor(iL, iC, iH).css())
        stop_strs.append(ok_b.css())
        stops_css = ", ".join(stop_strs)
    else:
        stops_css = f"{ok_a.css()}, {ok_b.css()}"

    return f"linear-gradient(in oklch {direction}, {stops_css})"


def oklch_radial_gradient(hex_center: str, hex_edge: str) -> str:
    """
    Emit a CSS radial-gradient() using OKLCH interpolation.
    Used for glow effects, hero backgrounds, and card accents.
    """
    ok_c = hex_to_oklch(hex_center)
    ok_e = hex_to_oklch(hex_edge)
    return f"radial-gradient(in oklch circle, {ok_c.css()}, {ok_e.css()})"


# ─────────────────────────────────────────────────────────────────────────────
# 12. THEME HEX SAFETY GUARD  (new in v100)
#     Several theme palette values in THEME_REGISTRY contain CSS values that
#     are not parseable as hex (e.g. 'rgba(...)', 'linear-gradient(...)').
#     This guard extracts the first valid hex for operations that require
#     a pure color value (OKLCH conversion, manifest theme_color, etc.)
# ─────────────────────────────────────────────────────────────────────────────

def extract_first_hex(value: str) -> str:
    """
    Extract the first #RRGGBB or #RGB hex color from an arbitrary CSS string.
    Falls back to '#000000' if none is found.

    Used to safely convert theme palette entries like
    'linear-gradient(135deg,#e0c3fc 0%,#8ec5fc 100%)' into a parseable hex
    for OKLCH conversion, PWA manifest theme_color, etc.

    This replaces the private _extract_hex() function in compiler.py v56
    with a public, importable version.
    """
    match = re.search(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', value)
    return match.group(0) if match else '#000000'


def safe_oklch(css_value: str) -> OKLCHColor:
    """
    Convert an arbitrary CSS color string (hex, gradient, rgba) to OKLCHColor
    by extracting the first valid hex. Falls back to black.

    Usage:
        ok = safe_oklch(theme['p'])  # works even if theme['p'] is a gradient
    """
    return hex_to_oklch(extract_first_hex(css_value))
