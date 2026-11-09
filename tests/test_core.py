import pytest

from gig import core


def test_templates_loaded():
    templates = core.available_templates()
    assert "python" in templates
    assert "node" in templates
    assert len(templates) >= 15


def test_alias_resolution():
    assert core.resolve_name("py") == "python"
    assert core.resolve_name("JS") == "node"
    assert core.resolve_name("golang") == "go"


def test_generate_single():
    out = core.generate(["python"])
    assert "__pycache__/" in out
    assert "# ===== python =====" in out


def test_generate_combines_and_dedups():
    out = core.generate(["python", "node"])
    assert "# ===== python =====" in out
    assert "# ===== node =====" in out
    assert "node_modules/" in out
    # .DS_Store appears in both templates but must appear only once
    assert out.count(".DS_Store") == 1


def test_generate_alias():
    out = core.generate(["py", "js"])
    assert "# ===== python =====" in out
    assert "# ===== node =====" in out


def test_generate_unknown_raises():
    with pytest.raises(KeyError):
        core.generate(["cobol"])


def test_search():
    results = core.search_templates("py")
    assert any("python" in r for r in results)


def test_write_gitignore(tmp_path):
    target = tmp_path / ".gitignore"
    core.write_gitignore("*.log\n", path=target)
    assert target.read_text() == "*.log\n"
    core.write_gitignore("*.tmp\n", path=target, append=True)
    assert "*.log" in target.read_text()
    assert "*.tmp" in target.read_text()
