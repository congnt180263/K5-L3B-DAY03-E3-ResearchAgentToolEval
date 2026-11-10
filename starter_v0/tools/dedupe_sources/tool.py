from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from tools._shared import err


def _source_key(url: str) -> str:
    url = url.strip()
    if not url or any(char.isspace() or ord(char) < 32 or char == "\\" for char in url):
        raise ValueError("invalid URL characters")

    parts = urlsplit(url)
    host = parts.hostname
    if parts.scheme not in {"http", "https"} or not host or parts.username is not None:
        raise ValueError("expected an absolute HTTP(S) URL without credentials")

    port = parts.port
    authority = f"[{host}]" if ":" in host else host
    default_port = 443 if parts.scheme == "https" else 80
    if port is not None and port != default_port:
        authority = f"{authority}:{port}"
    return urlunsplit((parts.scheme, authority, parts.path or "/", parts.query, ""))


def dedupe_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Return the first item for each normalized source URL in input order."""
    if not isinstance(items, list):
        return err("dedupe_sources", TypeError("items must be a list of source objects"))
    try:
        json.dumps(items, allow_nan=False)
    except (TypeError, ValueError, OverflowError, RecursionError):
        return err("dedupe_sources", ValueError("items must contain only JSON-serializable data"))

    seen: set[str] = set()
    unique = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get("url"), str):
            return err("dedupe_sources", TypeError(f"items[{index}].url must be a string"))
        try:
            key = _source_key(item["url"])
        except ValueError:
            return err("dedupe_sources", ValueError(f"items[{index}].url is not a valid HTTP(S) URL"))
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return {
        "tool": "dedupe_sources",
        "items": unique,
        "duplicate_count": len(items) - len(unique),
    }
