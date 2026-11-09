"""Launch only this demo; reuse existing dependencies without installing anything."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import threading
import time
import webbrowser

BASE_DIR = Path(__file__).resolve().parent
# Read existing project-local web dependencies, preserving the Conda environment.
WEB_DEPENDENCIES = BASE_DIR.parent / ".runtime" / "web"
if WEB_DEPENDENCIES.is_dir():
    sys.path.insert(0, str(WEB_DEPENDENCIES))
sys.path.insert(0, str(BASE_DIR))


def open_browser(url: str) -> None:
    time.sleep(1.2)
    webbrowser.open(url)


def main() -> None:
    parser = argparse.ArgumentParser(description="Eye AI frontend for the existing RETFound service")
    parser.add_argument("--port", type=int, default=int(os.environ.get("EYE_AI_PORT", "8001")))
    parser.add_argument("--api-url", help="Override RETFound origin; otherwise read base_url from connection.json")
    parser.add_argument("--connection-file", type=Path, help="Private connection.json for the trial Bearer credential")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if args.api_url:
        os.environ["RETFOUND_API_URL"] = args.api_url
    if args.connection_file:
        os.environ["RETFOUND_CONNECTION_FILE"] = str(args.connection_file.resolve())
    from backend.app.retfound_client import Connection
    connection = Connection.from_environment()
    from urllib.parse import urlsplit
    upstream = urlsplit(connection.base_url)
    if upstream.hostname in {"127.0.0.1", "localhost", "::1"} and (upstream.port or (443 if upstream.scheme == "https" else 80)) == args.port:
        parser.error("demo port must differ from the RETFound service port")
    try:
        import uvicorn
    except ImportError as exc:
        raise SystemExit("Missing demo dependencies; use the existing ml-homework interpreter. See README_AR.md.") from exc
    if not args.no_browser and os.environ.get("EYE_AI_NO_BROWSER") != "1":
        threading.Thread(target=open_browser, args=(f"http://127.0.0.1:{args.port}",), daemon=True).start()
    host = os.environ.get("EYE_AI_HOST", "127.0.0.1")
    if host not in {"127.0.0.1", "localhost", "::1", "0.0.0.0"}:
        parser.error("unsupported host")
    uvicorn.run("backend.app.main:app", host=host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
