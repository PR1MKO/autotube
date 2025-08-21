import hashlib
import re


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    return re.sub(r"\n{2,}", "\n\n", text).strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_content(text: str | None, html: str) -> str:
    if text:
        norm = normalize_text(text)
        return sha256_text(norm)
    return hashlib.sha256(html.encode("utf-8")).hexdigest()