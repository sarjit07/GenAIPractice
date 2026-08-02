"""Fills the report template with one JSON blob. No chart markup, no editorial
text, and no arithmetic happens in this module — all of that lives in the
template's own inline `<script>` (driven entirely by DATA) or in metrics.py.
"""

import json
from pathlib import Path

_TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "report_template.html"


def render_html(metrics: dict) -> str:
    template = _TEMPLATE_PATH.read_text()
    data_json = json.dumps(metrics, separators=(",", ":"))
    # A narration could in principle contain the literal text "</script>" — escape
    # the slash so it can't close the inline <script> tag early and break the page.
    data_json = data_json.replace("</", "<\\/")
    return template.replace("__DATA__", data_json)
