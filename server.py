"""Flask server for Trip.com replica with dynamic injection."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).parent
STATIC_DIRS = {
    "css": BASE_DIR / "css",
    "js": BASE_DIR / "js",
    "data": BASE_DIR / "data",
    "images": BASE_DIR / "images",
}

injected_content: List[Dict] = []


def find_closing_tag_index(html: str, container_start: int, tag: str = "div") -> int:
    """Find the matching closing tag index for the container starting at container_start."""
    open_token = f"<{tag}"
    close_token = f"</{tag}>"
    depth = 1
    cursor = html.find(">", container_start) + 1
    while depth > 0:
        next_open = html.find(open_token, cursor)
        next_close = html.find(close_token, cursor)
        if next_close == -1:
            return -1
        if next_open != -1 and next_open < next_close:
            depth += 1
            cursor = next_open + len(open_token)
            continue
        depth -= 1
        cursor = next_close + len(close_token)
    return cursor - len(close_token)


def inject_content_into_html(html_content: str, target: str, snippet: str) -> str:
    marker = f'data-inject="{target}"'
    marker_index = html_content.find(marker)
    if marker_index == -1:
        return html_content

    if 'data-injected="true"' not in html_content[marker_index: marker_index + len(marker) + 40]:
        html_content = (
            html_content[: marker_index + len(marker)]
            + ' data-injected="true"'
            + html_content[marker_index + len(marker):]
        )

    closing_index = find_closing_tag_index(html_content, marker_index)
    if closing_index == -1:
        return html_content

    return (
        html_content[:closing_index]
        + snippet
        + html_content[closing_index:]
    )


def build_content_card(item: Dict) -> str:
    component = item.get("component", "destination")
    title = item.get("title", "New experience")
    subtitle = item.get("subtitle", item.get("meta", ""))
    image = item.get("image") or "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=800&q=80"
    badge = item.get("badge")

    if component == "deal":
        return f"""
        <article class=\"coupon-card border-2 border-dashed border-yellow-300\">
          <div class=\"tag\">{item.get('tag', 'New') }</div>
          <h3 class=\"text-lg font-semibold\">{title}</h3>
          <button class=\"ghost-btn\">{item.get('cta', 'View')}</button>
        </article>
        """

    if component == "recommendation":
        badge_html = f"<div class='badge'>{badge}</div>" if badge else ""
        return f"""
        <article class=\"recommend-card ring-2 ring-yellow-200 injected\">
          {badge_html}
          <img src=\"{image}\" alt=\"{title}\">
          <div class=\"card-body\">
            <p class=\"eyebrow\">{title}</p>
            <p class=\"caption\">{subtitle}</p>
          </div>
        </article>
        """

    return f"""
    <article class=\"destination-card ring-2 ring-yellow-200 injected\">
      {'<div class=\"badge\">'+badge+'</div>' if badge else ''}
      <img src=\"{image}\" alt=\"{title}\">
      <div>
        <h3>{title}</h3>
        <p>{subtitle}</p>
      </div>
    </article>
    """


def apply_injections(html_content: str, section: str) -> str:
    updated = html_content
    for item in injected_content:
        target_section = item.get("section")
        if target_section not in (None, section):
            continue
        target_slot = item.get("target")
        if not target_slot:
            continue
        updated = inject_content_into_html(
            updated,
            target_slot,
            build_content_card(item),
        )
    return updated


def render_page(filename: str) -> str:
    html_path = BASE_DIR / filename
    if not html_path.exists():
        return "Page not found", 404
    html = html_path.read_text(encoding="utf-8")
    section = html_path.stem
    return apply_injections(html, section)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_page("index.html")

    for prefix, directory in STATIC_DIRS.items():
        directory.mkdir(parents=True, exist_ok=True)

        @app.route(f"/{prefix}/<path:filename>", defaults={"_prefix": prefix})
        def serve_static(filename: str, _prefix: str):  # type: ignore
            return send_from_directory(STATIC_DIRS[_prefix], filename)

    @app.route("/<path:page>")
    def other_pages(page: str):
        if not page.endswith(".html"):
            page = f"{page}.html"
        return render_page(page)

    @app.route("/api/content", methods=["GET"])
    def list_content():
        return jsonify({"content": injected_content, "count": len(injected_content)})

    @app.route("/api/inject", methods=["POST"])
    def add_content():
        payload = request.get_json(silent=True) or {}
        if "target" not in payload:
            return jsonify({"error": "target field is required"}), 400
        injected_content.append(payload)
        return jsonify({"status": "ok", "count": len(injected_content)})

    return app


def start_server(port: int = 5000):
    app = create_app()
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    start_server()
