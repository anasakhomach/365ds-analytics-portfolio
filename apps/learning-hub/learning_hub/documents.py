from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .catalog import Project, describe_gold_tables, load_catalog
from .paths import display_path


TEXT_EXTENSIONS = {".md", ".py", ".sql", ".txt"}


@dataclass(frozen=True)
class SourceDocument:
    id: str
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class TextChunk:
    id: str
    text: str
    metadata: dict[str, str]


def stable_id(*parts: str) -> str:
    payload = "|".join(parts).encode("utf-8", errors="replace")
    return hashlib.sha1(payload).hexdigest()


def source_type_for(path: Path) -> str:
    parts = set(path.parts)
    if "project-instructions" in parts:
        return "project_instruction"
    if "reports" in parts:
        return "report"
    if "docs" in parts:
        return "documentation"
    if "tests" in parts:
        return "quality_check"
    if path.suffix == ".sql":
        return "sql"
    if path.suffix == ".py":
        return "python"
    if path.name.lower() == "readme.md":
        return "readme"
    return "text"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def collect_project_documents(project: Project) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for path in (*project.document_paths, *project.code_paths):
        if not path.exists() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel_path = display_path(path)
        documents.append(
            SourceDocument(
                id=stable_id(project.slug, rel_path),
                text=_read_text(path),
                metadata={
                    "project_slug": project.slug,
                    "project_title": project.title,
                    "source_type": source_type_for(path),
                    "path": rel_path,
                    "section": "",
                    "table_name": "",
                },
            )
        )

    table_lines = [f"# Gold Table Catalog: {project.title}", ""]
    for table in describe_gold_tables(project):
        columns = ", ".join(table.columns) if table.columns else "columns unavailable"
        rows = "unknown" if table.row_count is None else f"{table.row_count:,}"
        table_lines.append(f"- `{table.name}`: {rows} rows; columns: {columns}")
    text = "\n".join(table_lines)
    documents.append(
        SourceDocument(
            id=stable_id(project.slug, "gold-table-catalog"),
            text=text,
            metadata={
                "project_slug": project.slug,
                "project_title": project.title,
                "source_type": "gold_catalog",
                "path": f"generated://{project.slug}/gold-table-catalog",
                "section": "Gold Table Catalog",
                "table_name": "",
            },
        )
    )
    return documents


def collect_documents(projects: Iterable[Project] | None = None) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for project in projects or load_catalog():
        documents.extend(collect_project_documents(project))
    return documents


def _sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", text))
    if not matches:
        return [("", text)]

    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = match.group(2).strip()
        sections.append((title, text[start:end].strip()))
    if matches[0].start() > 0:
        intro = text[: matches[0].start()].strip()
        if intro:
            sections.insert(0, ("", intro))
    return sections


def chunk_document(document: SourceDocument, max_chars: int = 1800, overlap: int = 200) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for section_title, section_text in _sections(document.text):
        if not section_text.strip():
            continue
        start = 0
        chunk_number = 0
        step = max(1, max_chars - overlap)
        while start < len(section_text):
            piece = section_text[start : start + max_chars].strip()
            if piece:
                metadata = dict(document.metadata)
                metadata["section"] = section_title
                metadata["chunk_number"] = str(chunk_number)
                chunks.append(
                    TextChunk(
                        id=stable_id(document.id, section_title, str(chunk_number), piece[:80]),
                        text=piece,
                        metadata=metadata,
                    )
                )
            if start + max_chars >= len(section_text):
                break
            start += step
            chunk_number += 1
    return chunks


def chunk_documents(documents: Iterable[SourceDocument]) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks
