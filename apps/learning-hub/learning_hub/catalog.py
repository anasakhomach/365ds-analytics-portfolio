from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb
import yaml

from .cloud_data import resolve_warehouse_path
from .paths import CATALOG_PATH, REPO_ROOT, display_path, repo_path


@dataclass(frozen=True)
class GoldTable:
    name: str
    row_count: int | None = None
    columns: tuple[str, ...] = ()


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    summary: str
    project_dir: Path
    instruction_path: Path
    readme_path: Path
    dashboard_path: Path
    source_warehouse_path: Path
    docs: tuple[Path, ...]
    reports: tuple[Path, ...]
    gold_tables: tuple[str, ...]
    starter_questions: tuple[str, ...]
    traits: dict[str, str]

    @property
    def warehouse_path(self) -> Path:
        return resolve_warehouse_path(self.slug, self.source_warehouse_path)

    @property
    def document_paths(self) -> tuple[Path, ...]:
        return (
            self.instruction_path,
            self.readme_path,
            *self.docs,
            *self.reports,
        )

    @property
    def code_paths(self) -> tuple[Path, ...]:
        script_dir = self.project_dir / "scripts"
        test_dir = self.project_dir / "tests"
        paths: list[Path] = []
        for pattern in ("*.py", "*.sql"):
            paths.extend(sorted(script_dir.rglob(pattern)))
            paths.extend(sorted(test_dir.rglob(pattern)))
        paths.append(self.dashboard_path)
        return tuple(path for path in paths if path.exists())


def _required_path(value: str, field: str, project_slug: str) -> Path:
    if not value:
        raise ValueError(f"{project_slug}: missing required path field {field}")
    return repo_path(value)


def _load_project(raw: dict[str, Any]) -> Project:
    slug = raw["slug"]
    return Project(
        slug=slug,
        title=raw["title"],
        summary=raw.get("summary", ""),
        project_dir=_required_path(raw["project_dir"], "project_dir", slug),
        instruction_path=_required_path(raw["instruction_path"], "instruction_path", slug),
        readme_path=_required_path(raw["readme_path"], "readme_path", slug),
        dashboard_path=_required_path(raw["dashboard_path"], "dashboard_path", slug),
        source_warehouse_path=_required_path(raw["warehouse_path"], "warehouse_path", slug),
        docs=tuple(repo_path(path) for path in raw.get("docs", [])),
        reports=tuple(repo_path(path) for path in raw.get("reports", [])),
        gold_tables=tuple(raw.get("gold_tables", [])),
        starter_questions=tuple(raw.get("starter_questions", [])),
        traits=dict(raw.get("traits", {})),
    )


def load_catalog(path: Path = CATALOG_PATH) -> list[Project]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    projects = [_load_project(item) for item in payload.get("projects", [])]
    slugs = [project.slug for project in projects]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Project catalog contains duplicate slugs")
    return projects


def get_project(slug: str, projects: list[Project] | None = None) -> Project:
    projects = projects or load_catalog()
    for project in projects:
        if project.slug == slug:
            return project
    raise KeyError(f"Unknown project slug: {slug}")


def validate_catalog(projects: list[Project] | None = None) -> list[str]:
    errors: list[str] = []
    for project in projects or load_catalog():
        for path in (
            project.project_dir,
            project.instruction_path,
            project.readme_path,
            project.dashboard_path,
            project.source_warehouse_path,
            *project.docs,
            *project.reports,
        ):
            if not path.exists():
                errors.append(f"{project.slug}: missing {display_path(path)}")
        if not project.gold_tables:
            errors.append(f"{project.slug}: no Gold tables listed")
        for trait in ("workflow", "analytics_engine", "visualization", "ai_data_access"):
            if not project.traits.get(trait):
                errors.append(f"{project.slug}: missing trait {trait}")
    return errors


def describe_gold_tables(project: Project) -> list[GoldTable]:
    if not project.warehouse_path.exists():
        return [GoldTable(name=name) for name in project.gold_tables]

    tables: list[GoldTable] = []
    with duckdb.connect(str(project.warehouse_path), read_only=True) as con:
        existing = {
            row[0]
            for row in con.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'gold'
                """
            ).fetchall()
        }
        for table_name in project.gold_tables:
            if table_name not in existing:
                tables.append(GoldTable(name=table_name))
                continue
            row_count = con.execute(f'SELECT COUNT(*) FROM gold."{table_name}"').fetchone()[0]
            columns = tuple(
                row[0]
                for row in con.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'gold'
                      AND table_name = ?
                    ORDER BY ordinal_position
                    """,
                    [table_name],
                ).fetchall()
            )
            tables.append(GoldTable(name=table_name, row_count=row_count, columns=columns))
    return tables


def catalog_summary(projects: list[Project] | None = None) -> list[dict[str, Any]]:
    return [
        {
            "slug": project.slug,
            "title": project.title,
            "summary": project.summary,
            "warehouse": display_path(project.warehouse_path),
            "gold_tables": len(project.gold_tables),
            "documents": len(project.document_paths),
            "code_files": len(project.code_paths),
            "workflow": project.traits.get("workflow", ""),
            "analytics_engine": project.traits.get("analytics_engine", ""),
            "visualization": project.traits.get("visualization", ""),
        }
        for project in projects or load_catalog()
    ]


def ensure_repo_path(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(f"Path is outside repository: {path}") from exc
    return resolved
