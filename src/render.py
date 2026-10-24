import json
from html import escape
from pathlib import Path

VALID_STATUSES = {"operational", "degraded", "outage"}


def render_page(data):
    service = data["service"]
    status = data["status"]

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    return (
        "<!doctype html>"
        '<html lang="en"><head>'
        '<meta charset="utf-8">'
        "<title>Service Status</title>"
        "</head><body>"
        f"<h1>{escape(service)}</h1>"
        f"<p>Status: {escape(status)}</p>"
        "</body></html>"
    )


def main():
    data = json.loads(Path("data/status.json").read_text(encoding="utf-8"))
    output = Path("site")
    output.mkdir(exist_ok=True)
    (output / "index.html").write_text(render_page(data), encoding="utf-8")


if __name__ == "__main__":
    main()