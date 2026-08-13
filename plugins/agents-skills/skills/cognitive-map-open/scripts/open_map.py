#!/usr/bin/env python3
"""Resolve and open a generated cognitive-map HTML file."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def newest(paths: list[Path]) -> Path | None:
    files = [path.resolve() for path in paths if path.is_file()]
    return max(files, key=lambda path: path.stat().st_mtime) if files else None


def render_source(source: Path) -> Path:
    webpage = source.with_suffix(".html")
    renderer = Path(__file__).resolve().parents[2] / "cognitive-map" / "scripts" / "render_map.py"
    if not renderer.is_file():
        raise RuntimeError(f"Cognitive-map renderer is missing: {renderer}")
    subprocess.run(
        [sys.executable, str(renderer), str(source), "--output", str(webpage)],
        check=True,
    )
    return webpage.resolve()


def rendered_or_refresh(source: Path, webpage: Path) -> Path:
    if not webpage.is_file() or source.stat().st_mtime > webpage.stat().st_mtime:
        return render_source(source)
    return webpage.resolve()


def resolve_target(raw_path: str | None) -> Path:
    requested = Path(raw_path).expanduser() if raw_path else Path.cwd()

    if requested.is_file():
        if requested.suffix.lower() == ".md":
            return rendered_or_refresh(requested, requested.with_suffix(".html"))
        if requested.suffix.lower() != ".html":
            raise ValueError(f"Expected an HTML cognitive map, got: {requested}")
        return requested.resolve()

    if raw_path and not requested.is_dir():
        raise FileNotFoundError(f"Map path does not exist: {requested}")

    directory = requested if requested.is_dir() else Path.cwd()
    conventional = directory / "map.html"
    markdown = directory / "map.md"
    if conventional.is_file():
        return rendered_or_refresh(markdown, conventional) if markdown.is_file() else conventional.resolve()

    candidate = newest(list(directory.glob("*-map.html")))
    if candidate:
        source = candidate.with_suffix(".md")
        return rendered_or_refresh(source, candidate) if source.is_file() else candidate

    other_markdown = newest(list(directory.glob("*-map.md")))
    source = markdown if markdown.is_file() else other_markdown
    if source:
        return render_source(source)
    raise FileNotFoundError(f"No cognitive-map webpage exists in {directory.resolve()}")


def launch(target: Path) -> None:
    if sys.platform == "darwin":
        command = ["open", str(target)]
    elif os.name == "nt":
        os.startfile(str(target))  # type: ignore[attr-defined]
        return
    elif shutil.which("xdg-open"):
        command = ["xdg-open", str(target)]
    elif shutil.which("wslview"):
        command = ["wslview", str(target)]
    else:
        raise RuntimeError("No supported browser opener was found; open the printed file URL manually.")

    subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Map HTML/Markdown file or directory")
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Resolve and print the map URL without opening a browser",
    )
    args = parser.parse_args()

    try:
        target = resolve_target(args.path)
    except (FileNotFoundError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

    print(f"Cognitive map: {target.as_uri()}", flush=True)
    if not args.print_only:
        try:
            launch(target)
        except RuntimeError as error:
            print(str(error), file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
