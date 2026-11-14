---
type: llm
---

PASS if the answer defines fields with stable snake_case ids (via rwmb_meta_boxes or MB Builder, not both), wraps labels in __(), binds output through Oxygen's native Meta Box dynamic data instead of shortcodes, and escapes output in any PHP. FAIL if it holds layout in [rwmb_meta] shortcodes.
