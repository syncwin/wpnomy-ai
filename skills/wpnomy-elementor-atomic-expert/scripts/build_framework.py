#!/usr/bin/env python3
"""Build the Atomic Framework CSS and the Elementor Variable manifest from an
Atomic Framework token export.

The framework is maintained separately as a product. A new version is a file
drop plus a re-run. Nothing it emits is hand-edited.

Consumes any of the framework's export shapes: the full export carrying meta,
layer, type and darkValue, or a lighter one (a Bricks export) carrying only
name, value, id and category. Anything missing is inferred from the value.

Token names pass through exactly as the framework writes them. If the framework
prefixes its names the prefix flows through; if it does not, none is added. The
framework owns its own namespace.

Usage:
    python3 build_framework.py <tokens.json> [-o OUTDIR]

Emits:
    atomic-framework.css        the :root block, plus a dark block when the
                                export carries dark values
    variables-manifest.json     every token that can register as an Elementor
                                Variable, with label, type, value and mode
    report.txt                  what registers, what needs a site value, what
                                stays in CSS, and why
"""
import argparse
import json
import re
import sys
from pathlib import Path

COLOUR_FUNCS = ("oklch", "rgb", "hsl", "lab", "lch", "color(")
LENGTH = re.compile(r"\d\s*(px|rem|em|%|vw|vh|ch|ex|fr)\b")
EXPR = re.compile(r"(var|color-mix|calc|clamp|min|max)\(")
KEYWORD = {"inherit", "initial", "unset", "revert", ""}


def infer_type(tok):
    """The export may or may not carry a type. Work it out from the value."""
    if tok.get("type"):
        return tok["type"]
    name, v = tok["name"], str(tok["value"]).strip()
    if name.startswith("font-") and not name.endswith(("weight", "size")):
        return "font"
    if name.startswith("shadow-") and " " in v:
        return "shadow"
    if name.startswith("transition"):
        return "transition"
    if name.endswith("line-height"):
        # A length-bearing calc() that is not a length: line-height is unitless
        # against the font size, and registering it as a size variable would
        # type-check and still be wrong.
        return "string"
    if name.endswith(("font-weight", "weight")):
        return "number"
    if v.startswith("#") or v.startswith(COLOUR_FUNCS):
        return "color"
    if "color-mix(" in v or (v.startswith("var(") and
                             ("color" in name or name.startswith(("bg-", "on-", "border")))):
        return "color"
    if v == "0" or LENGTH.search(v) or v.startswith("clamp("):
        return "size"
    if re.fullmatch(r"-?\d+(\.\d+)?", v):
        return "number"
    return "string"


def infer_layer(tok):
    if tok.get("layer"):
        return tok["layer"]
    v = str(tok["value"])
    return "molecule" if EXPR.search(v) and "clamp(" not in v else "atom"


def classify(tok, ttype):
    """Return (elementor_type, mode, note). elementor_type None means CSS only."""
    v = str(tok["value"]).strip()
    if ttype == "color":
        if v.startswith("#") or v.startswith(COLOUR_FUNCS):
            return "color", "mirror", ""
        return None, None, "derived value; a colour variable holds a literal"
    if ttype == "font":
        if v in KEYWORD:
            return "font", "site", "ships as a keyword; set the site's real family at install"
        return "font", "mirror", ""
    if ttype == "size":
        return "size", "reference", ""
    return None, None, f"no Elementor Variable type for '{ttype}'"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tokens")
    ap.add_argument("-o", "--outdir", default=".")
    a = ap.parse_args()

    data = json.loads(Path(a.tokens).read_text())
    meta = data.get("meta", {})
    cats = {c["id"]: c["name"] for c in data.get("categories", [])}
    toks = data["variables"]
    # The export is untrusted text that becomes CSS: refuse anything that could break out of a declaration.
    bad = [t.get("name") for t in toks if not re.fullmatch(r"[A-Za-z0-9_-]+", str(t.get("name", "")))
           or any(re.search(r"[{};<>]|/\*|\*/|@import", str(t.get(k) or "")) for k in ("value", "darkValue"))]
    if bad:
        sys.exit(f"Refusing to write CSS: unsafe token name or value in {bad[:5]}")
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)

    root_size = meta.get("rootFontSize")
    has_dark = any(t.get("darkValue") for t in toks)
    dark_sel = meta.get("darkModeSelector", '[data-theme="dark"]')

    order = list(dict.fromkeys(t.get("category") for t in toks))
    root, dark = [], []
    for c in order:
        rows = [t for t in toks if t.get("category") == c]
        root.append(f"  /* {cats.get(c, c or 'Tokens')} */")
        for t in rows:
            root.append(f"  --{t['name']}: {t['value']};")
        root.append("")
        dk = [t for t in rows if t.get("darkValue") and t["darkValue"] != t["value"]]
        if dk:
            dark.append(f"  /* {cats.get(c, c or 'Tokens')} */")
            for t in dk:
                dark.append(f"  --{t['name']}: {t['darkValue']};")
            dark.append("")

    head = [f"/* Atomic Framework {meta.get('version', '(version not in export)')}. "
            f"{len(toks)} tokens. Generated from the framework export, do not hand-edit. */"]
    if root_size:
        head += [
            f"/* Needs html font-size {root_size} so 1rem = {meta.get('remBase', '10px')}.",
            "   Verify the COMPUTED value on a rendered page: a theme that sets the base size",
            "   on body does nothing for rem, and every clamp() then renders too large. */",
            "",
            f"html {{ font-size: {root_size}; }}",
        ]
    else:
        head.append("/* This export carries no root font size. The scales are in rem, "
                    "so confirm the rem base before install. */")
    css = head + ["", ":root {", *root, "}"]
    if has_dark:
        css += ["", dark_sel + " {", *dark, "}"]
    (out / "atomic-framework.css").write_text("\n".join(css) + "\n")

    registers, needs_site, css_only = [], [], []
    for t in toks:
        ttype = infer_type(t)
        etype, mode, note = classify(t, ttype)
        entry = {
            "label": t["name"],
            "token": f"--{t['name']}",
            "category": cats.get(t.get("category"), t.get("category")),
            "layer": infer_layer(t),
            "source_type": ttype,
        }
        if etype and mode == "site":
            entry.update(type=etype, value=None, mode="site", note=note)
            needs_site.append(entry)
        elif etype:
            entry.update(
                type=etype,
                # A size accepts a CSS expression, so it can point at the CSS
                # layer. A colour and a font must carry the value.
                value=f"var(--{t['name']})" if etype == "size" else t["value"],
                mode=mode,
            )
            registers.append(entry)
        else:
            entry["reason"] = note
            css_only.append(entry)

    (out / "variables-manifest.json").write_text(json.dumps({
        "framework_version": meta.get("version"),
        "source_export": Path(a.tokens).name,
        "token_names_prefixed": bool(re.match(r"^[a-z]{2,4}-", toks[0]["name"])),
        "registers": registers,
        "needs_site_value": needs_site,
        "css_only": css_only,
    }, indent=2))

    def tally(rows):
        d = {}
        for r in rows:
            d[r["type"]] = d.get(r["type"], 0) + 1
        return ", ".join(f"{v} {k}" for k, v in sorted(d.items()))

    rep = [
        f"Atomic Framework {meta.get('version', '(no version in export)')}  "
        f"source {Path(a.tokens).name}",
        f"{len(toks)} tokens: {len(registers)} register, {len(needs_site)} need a site value, "
        f"{len(css_only)} stay in CSS.",
        f"Dark values in export: {'yes' if has_dark else 'no'}. "
        f"Root font size in export: {root_size or 'not specified'}.",
        "",
        f"Register: {tally(registers)}",
        f"  reference mode (value is var(--token)): "
        f"{sum(1 for m in registers if m['mode'] == 'reference')}",
        f"  mirror mode (value copied, keep in step with the CSS): "
        f"{sum(1 for m in registers if m['mode'] == 'mirror')}",
        "",
    ]
    if needs_site:
        rep.append("Need a site value before registering:")
        for s in needs_site:
            rep.append(f"  {s['label']:24} {s['note']}")
        rep.append("")
    rep.append("CSS only:")
    for s in css_only:
        rep.append(f"  {s['label']:24} {s['reason']}")
    if has_dark:
        rep += ["", "Dark mode is CSS only: Elementor Variables have no dark variant."]
    (out / "report.txt").write_text("\n".join(rep) + "\n")
    print("\n".join(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
