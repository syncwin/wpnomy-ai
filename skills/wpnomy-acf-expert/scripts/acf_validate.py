#!/usr/bin/env python3
"""Validate ACF JSON before handover.

Usage: python3 acf_validate.py <file-or-directory> [...]

Exit 0 = clean. Exit 1 = errors found. Warnings never block.
"""
import json
import sys
from pathlib import Path

BOOL_FLAGS = {"required", "active", "allow_null", "multiple", "ui", "disabled",
              "readonly", "wrapper_required", "hierarchical", "public",
              "show_in_rest", "allow_in_bindings", "media_upload", "delay"}
MAX_SLUG = 20      # register_post_type hard limit
MAX_TAX_SLUG = 32  # register_taxonomy hard limit

errors, warnings = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


def load(path):
    """Return a list of (source_label, object) pairs."""
    out = []
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        err(path.name, f"not valid JSON ({e})")
        return out
    items = data if isinstance(data, list) else [data]
    for i, obj in enumerate(items):
        if isinstance(obj, dict):
            label = path.name if len(items) == 1 else f"{path.name}[{i}]"
            out.append((label, obj))
        else:
            err(path.name, f"entry {i} is not an object")
    return out


def walk_fields(fields, where, seen_keys, names_in_group, path=""):
    """Recurse fields, sub_fields and flexible-content layouts."""
    for f in fields or []:
        if not isinstance(f, dict):
            err(where, f"{path}: field entry is not an object")
            continue
        key = f.get("key", "")
        name = f.get("name", "")
        label = f"{path}{name or key or '<unnamed>'}"

        if not key:
            err(where, f"{label}: missing key")
        else:
            if key in seen_keys:
                err(where, f"{label}: key '{key}' already used in {seen_keys[key]}")
            else:
                seen_keys[key] = where
            if not key.startswith("field_"):
                err(where, f"{label}: key '{key}' must start with field_")
            elif name and key != f"field_{name}":
                warn(where, f"{label}: key '{key}' does not match name '{name}'")

        if not name:
            err(where, f"{label}: missing name")
        elif name in names_in_group:
            err(where, f"{label}: duplicate field name '{name}' in the same group")
        else:
            names_in_group.add(name)

        ftype = f.get("type")
        if not ftype:
            err(where, f"{label}: missing type")

        for flag in BOOL_FLAGS & set(f):
            if isinstance(f[flag], bool):
                err(where, f"{label}: '{flag}' is {f[flag]}, must be 0 or 1")

        for ch in f.get("choices", {}) or {}:
            if " " in str(ch) or str(ch) != str(ch).lower():
                warn(where, f"{label}: choice value '{ch}' looks like a label, not a slug")

        if ftype in ("repeater", "group") and not f.get("sub_fields"):
            err(where, f"{label}: {ftype} has no sub_fields")
        if ftype == "flexible_content" and not f.get("layouts"):
            err(where, f"{label}: flexible_content has no layouts")

        walk_fields(f.get("sub_fields"), where, seen_keys, names_in_group, f"{label} > ")
        layouts = f.get("layouts")
        if isinstance(layouts, dict):
            layouts = list(layouts.values())
        for lay in layouts or []:
            if isinstance(lay, dict):
                walk_fields(lay.get("sub_fields"), where, seen_keys,
                            names_in_group, f"{label} > {lay.get('name', '?')} > ")


def collect_logic(fields, refs, where):
    for f in fields or []:
        if not isinstance(f, dict):
            continue
        for group in f.get("conditional_logic") or []:
            for rule in group if isinstance(group, list) else []:
                if isinstance(rule, dict) and rule.get("field"):
                    refs.append((where, f.get("name", "?"), rule["field"]))
        collect_logic(f.get("sub_fields"), refs, where)
        layouts = f.get("layouts")
        if isinstance(layouts, dict):
            layouts = list(layouts.values())
        for lay in layouts or []:
            if isinstance(lay, dict):
                collect_logic(lay.get("sub_fields"), refs, where)


def main(argv):
    paths = []
    for arg in argv or ["."]:
        p = Path(arg)
        if p.is_dir():
            paths += sorted(p.glob("*.json"))
        elif p.exists():
            paths.append(p)
        else:
            err(arg, "path does not exist")

    if not paths:
        print("No JSON files found.")
        return 1

    all_keys, logic_refs = {}, []

    for path in paths:
        for where, obj in load(path):
            key = obj.get("key", "")
            if key:
                if key in all_keys:
                    err(where, f"object key '{key}' already used in {all_keys[key]}")
                else:
                    all_keys[key] = where

            if "fields" in obj or key.startswith("group_"):
                if not obj.get("title"):
                    err(where, "field group has no title")
                if not obj.get("location"):
                    err(where, "field group has no location rules")
                if not obj.get("fields"):
                    err(where, "field group has no fields")
                walk_fields(obj.get("fields"), where, all_keys, set())
                collect_logic(obj.get("fields"), logic_refs, where)

            if key.startswith("post_type_"):
                slug = obj.get("post_type", "")
                if not slug:
                    err(where, "post type has no post_type slug")
                elif len(slug) > MAX_SLUG:
                    err(where, f"post type slug '{slug}' is {len(slug)} chars, limit {MAX_SLUG}")

            if key.startswith("taxonomy_"):
                slug = obj.get("taxonomy", "")
                if not slug:
                    err(where, "taxonomy has no taxonomy slug")
                elif len(slug) > MAX_TAX_SLUG:
                    err(where, f"taxonomy slug '{slug}' is {len(slug)} chars, limit {MAX_TAX_SLUG}")
                if not obj.get("object_type"):
                    warn(where, "taxonomy is not attached to any post type")

            if key.startswith("ui_options_page_"):
                if not obj.get("page_title"):
                    err(where, "options page has no page_title")
                if not obj.get("menu_slug"):
                    err(where, "options page has no menu_slug")

    for where, fname, target in logic_refs:
        if target not in all_keys:
            err(where, f"{fname}: conditional logic points at '{target}', which does not exist")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    print(f"\n{len(paths)} file(s), {len(all_keys)} key(s). "
          f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
