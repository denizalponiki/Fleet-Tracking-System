"""ADR-002 rule 2: a module imports another module only through its public api.py.

import-linter (`lint-imports`) checks the dependency direction; this test checks the facade rule,
which import-linter cannot express for "every module except my own".
"""

import ast
import sys
from pathlib import Path

import pytest

MODULES_DIR = Path(__file__).resolve().parents[1] / "app" / "modules"
MODULE_NAMES = sorted(p.name for p in MODULES_DIR.iterdir() if p.is_dir() and not p.name.startswith("_"))


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.append(node.module)
            names.extend(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def find_facade_violations(module_name: str) -> list[str]:
    violations = []
    for path in (MODULES_DIR / module_name).rglob("*.py"):
        for imported in _imported_modules(path):
            parts = imported.split(".")
            if parts[:2] != ["app", "modules"] or len(parts) < 3 or parts[2] == module_name:
                continue
            target = parts[2]
            # allowed: "from app.modules.<target> import api" and "app.modules.<target>.api[...]"
            if len(parts) == 3 or parts[3] == "api":
                continue
            violations.append(f"{path.relative_to(MODULES_DIR).as_posix()} imports {imported} (use app.modules.{target}.api)")
    return violations


def test_all_eight_modules_exist():
    assert MODULE_NAMES == [
        "carpool", "fuel", "handover", "identity", "maintenance", "reporting", "reservation", "vehicle",
    ]


@pytest.mark.parametrize("module_name", MODULE_NAMES)
def test_modules_use_only_public_facades(module_name):
    assert find_facade_violations(module_name) == []


def test_facade_rule_detects_internal_import(tmp_path, monkeypatch):
    fake = tmp_path / "modules"
    (fake / "carpool").mkdir(parents=True)
    (fake / "carpool" / "service.py").write_text(
        "from app.modules.reservation.models import Reservation\n"
        "from app.modules.reservation import api\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "MODULES_DIR", fake)
    violations = find_facade_violations("carpool")
    assert violations
    assert all("app.modules.reservation.models" in v for v in violations)
