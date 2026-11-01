#!/usr/bin/env python3
"""Map an Atomic Wireframe project onto Bricks payloads.

Reads either shape:
  * the `atomic-wireframe/get-project` ability result (parts: settings, breakpoints, tokens, classes),
    saved as JSON, with or without the outer {"success":..,"data":..} wrapper;
  * a project envelope exported from Atomic Wireframe (schemaVersion 2: variables, settings, breakpoints, ...).

Writes one JSON plan with:
  variables        rows for bricks/set-global-variables  ({name, value, category}); Bricks assigns ids, upserts by name
  categories       rows for bricks/set-global-variable-categories (no `scale` key: the framework owns its scales)
  themeStyle       Root theme style payload for bricks/create-theme-style ({label, conditions, settings}), every value a var()
  breakpoints      mobile-first rows for bricks/set-breakpoints
  darkCss          the [data-theme="dark"] override block, for when the site ships dark mode
  classPrefix      the project prefix that replaces `awf-`, plus per-class renames
  warnings         things a human must decide

It writes nothing to any site. The naming and rem rebasing are ported from the plugin's own exporter
(packages/tokens-core/src/export.ts) so the result matches its "Bricks JSON" export.

Usage: python3 aw_to_bricks.py project.json [-o plan.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent.parent / "assets" / "atomic-framework-ids.json"


def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        data = data["data"]
    return data


def rnd(n, d=4):
    return round(n + 0.0, d)


def rebase_rem(value, root):
    if root != "62.5%":
        return value
    return re.sub(r"(-?[\d.]+)rem", lambda m: f"{rnd(float(m.group(1)) * 1.6):g}rem", str(value))


def export_name(name, base, prefix):
    typ = base.get("afwtyp", {}).get("naming", "text")
    sp = base.get("afwsp", {}).get("naming", "space")
    if name.startswith("text-") and typ and typ != "text":
        name = typ + "-" + name[5:]
    elif name.startswith("space-") and sp and sp != "space":
        name = sp + "-" + name[6:]
    return f"{prefix}-{name}" if prefix else name


def apply_rename(value, rename, root):
    renamed = re.sub(r"var\(--([a-zA-Z0-9-]+)\)", lambda m: f"var(--{rename.get(m.group(1), m.group(1))})", str(value))
    return rebase_rem(renamed, root)


def normalise(data, meta):
    """Return (tokens, settings, breakpoints, strategy, prefix, renames)."""
    if "variables" in data:  # envelope
        toks = [
            {"name": v["name"], "value": v["value"], "dark": v.get("darkValue"), "category": v["category"],
             "layer": v.get("layer"), "type": v.get("type"), "id": v.get("id")}
            for v in data["variables"]
        ]
        return (toks, data.get("settings", {}), data.get("breakpoints", []), data.get("breakpointStrategy"),
                data.get("settings", {}).get("classPrefix", ""), data.get("classRenames") or {}, data.get("baseSettings"))
    toks = []
    for t in data.get("tokens", []):
        known = meta["tokens"].get(t["name"], {})
        toks.append({"name": t["name"], "value": t["value"], "dark": t.get("dark_value"), "category": t["category"],
                     "layer": known.get("layer"), "type": t.get("type"), "id": known.get("id")})
    return (toks, data.get("settings", {}), data.get("breakpoints", []), data.get("breakpoint_strategy"),
            data.get("class_prefix", data.get("settings", {}).get("classPrefix", "")), data.get("class_renames") or {}, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    meta = json.loads(ASSET.read_text(encoding="utf-8"))
    data = load(args.project)
    toks, settings, bps, strategy, prefix, renames, base = normalise(data, meta)
    base = base or meta["defaultBaseSettings"]
    root = settings.get("rootFontSize", "100%")
    vprefix = settings.get("variablePrefix", "")
    warnings = []

    if not toks:
        sys.exit("No tokens found. Call atomic-wireframe/get-project with parts including \"tokens\".")
    missing = sorted(set(meta["tokens"]) - {t["name"] for t in toks})
    if missing:
        warnings.append(f"{len(missing)} framework tokens absent from the project: {', '.join(missing)}. Read every category, or confirm they were removed on purpose.")
    unknown = [t["name"] for t in toks if t["name"] not in meta["tokens"]]
    if unknown:
        warnings.append(f"Tokens not in Atomic Framework 2.2.0: {', '.join(unknown)}. They get generated ids; check the framework version.")

    rename = {t["name"]: export_name(t["name"], base, vprefix) for t in toks}
    variables = []
    for t in toks:
        variables.append({
            "name": rename[t["name"]],
            "value": apply_rename(t["value"], rename, root),
            "category": t["category"],
        })
        if t["name"] == "font-heading" and t["value"].strip() == "inherit":
            warnings.append("font-heading is `inherit`. Set the site's heading family in Atomic Wireframe (or confirm headings share the body family) before building.")

    dark_lines = [f"  --{rename[t['name']]}: {apply_rename(t['dark'], rename, root)};"
                  for t in toks if t["dark"] and (t["layer"] in (None, "atom"))]
    dark_css = "[data-theme=\"dark\"] {\n" + "\n".join(dark_lines) + "\n}" if dark_lines else ""

    used = {t["category"] for t in toks}
    categories = [c for c in meta["categories"] if c["id"] in used]

    def v(n):
        return f"var(--{rename.get(n, n)})"

    theme_style = {
        "label": "Root",
        "conditions": [{"main": "any"}],
        "settings": {
            "typography": {
                "typographyHtml": root,
                "typographyBody": {"font-family": v("font-body"), "font-size": v("text-m"), "line-height": v("text-line-height"),
                                   "font-weight": v("text-font-weight"), "color": v("text-color")},
                "typographyHeadings": {"font-family": v("font-heading"), "font-weight": v("heading-font-weight"),
                                       "line-height": v("heading-line-height"), "color": v("heading-color")},
                **{f"typographyHeadingH{i}": {"font-size": v(f"h{i}")} for i in range(1, 7)},
            },
        },
    }

    enabled = sorted([b for b in bps if b.get("enabled")], key=lambda b: b["px"])
    rows = []
    if enabled:
        if (strategy or "mobile-first") != "mobile-first":
            warnings.append(f"Project breakpoint strategy is {strategy}; this plan assumes mobile-first. Ask before mapping.")
        for i, b in enumerate(enabled):
            row = {"key": b["id"], "label": f"{b['name']} ({b['px']}px)", "width": b["px"]}
            if i == 0:
                row["base"] = True
            rows.append(row)
        if len(rows) > 5:
            warnings.append(f"{len(rows)} breakpoints enabled. Each adds a responsive column to every control in Bricks; confirm all are needed.")
        if enabled[0]["px"] <= 360:
            warnings.append("The base breakpoint is 360px or less. Mobile-first base styles already cover small phones; consider disabling it in Atomic Wireframe.")
        warnings.append("Replacing Bricks' default breakpoint keys needs allowRemovedBreakpoints: true after reviewing the usage evidence. After set-breakpoints, stop unless list-breakpoints reads back isMobileFirst: true.")

    if root == "62.5%":
        warnings.append("Root font size is 62.5%: every rem value has been multiplied by 1.6. The Root theme style must set html font-size to 62.5% or every size renders 1.6x too small.")

    if prefix and not re.fullmatch(r"sw-[a-z0-9]+", prefix):
        warnings.append(f"Class prefix `{prefix}` is not company plus site code (`sw-<site>`, e.g. `sw-md`). House rule: ask before using it.")
    if not prefix:
        warnings.append("No class prefix set in the project. Classes would export as `awf-`. Ask for the prefix.")

    plan = {
        "source": {"rootFontSize": root, "variablePrefix": vprefix, "tokenCount": len(toks), "framework": meta["source"]},
        "categories": categories,
        "variables": variables,
        "themeStyle": theme_style,
        "themeStyleNote": "Typography keys match the bundled theme-style schema; read the live schema for link, button and container keys before adding them.",
        "breakpoints": rows,
        "darkCss": dark_css,
        "classPrefix": prefix,
        "classRenames": renames,
        "warnings": warnings,
    }
    text = json.dumps(plan, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"Wrote {args.out}: {len(variables)} variables, {len(rows)} breakpoints, {len(warnings)} warnings")
        for w in warnings:
            print(" -", w)
    else:
        print(text)


if __name__ == "__main__":
    main()
