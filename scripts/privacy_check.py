"""Lightweight pre-publication scan for obvious secret/privacy indicators."""

from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SKIP_DIRS={".git",".venv","venv","env","__pycache__",".ipynb_checkpoints"}
SKIP_FILES={Path("scripts/privacy_check.py")}
TEXT_SUFFIXES={".py",".md",".txt",".yml",".yaml",".json",".toml",".ini",".cfg",".sql",".ipynb"}

PATTERNS={
    "private IPv4":re.compile(r"\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})\b"),
    "secret assignment":re.compile(r"""(?i)\b(?:password|passwd|api[_-]?key|access[_-]?token|secret)\b\s*[:=]\s*["\'][^"\']{4,}["\']"""),
    "private key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "local domain":re.compile(r"(?i)\b[a-z0-9.-]+\.local\b")
}

def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel=path.relative_to(ROOT)
        if rel in SKIP_FILES or any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"README","LICENSE","NOTICE"}:
            yield path,rel

def main():
    findings=[]
    for path,rel in iter_text_files():
        try:
            text=path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label,pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line=text.count("\n",0,match.start())+1
                findings.append((str(rel),line,label))
    if findings:
        print("Potential publication risks found:")
        for rel,line,label in findings:
            print(f"- {rel}:{line} — {label}")
        return 1
    print("Privacy check passed: no configured risk patterns found.")
    return 0

if __name__=="__main__":
    sys.exit(main())
