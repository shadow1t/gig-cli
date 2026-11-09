import io
import tarfile

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


def test_generate_combines_and_dedups(monkeypatch, tmp_path):
    monkeypatch.setattr(core, "USER_TEMPLATES_DIR", tmp_path / "empty_user_templates")
    out = core.generate(["python", "node"])
    assert "# ===== python =====" in out
    assert "# ===== node =====" in out
    assert "node_modules/" in out
    # .env appears in both official templates but must appear only once
    assert [l.strip() for l in out.splitlines()].count(".env") == 1


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


def test_normalize_name():
    assert core._normalize_name("C++") == "cpp"
    assert core._normalize_name("C#") == "csharp"
    assert core._normalize_name("Python") == "python"


def _make_fake_tarball() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for path, content in [
            ("gitignore-main/Python.gitignore", "__pycache__/\n"),
            ("gitignore-main/C++.gitignore", "*.o\n"),
            ("gitignore-main/Global/macOS.gitignore", ".DS_Store\n"),
            ("gitignore-main/README.md", "not a template"),
        ]:
            info = tarfile.TarInfo(path)
            data = content.encode()
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def test_fetch_official_templates_parses_tarball(monkeypatch):
    def fake_urlopen(request, timeout=0):
        class Resp:
            def read(self):
                return _make_fake_tarball()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        return Resp()

    monkeypatch.setattr(core.urllib.request, "urlopen", fake_urlopen)
    templates = core.fetch_official_templates()
    assert templates["python"] == "__pycache__/\n"
    assert templates["cpp"] == "*.o\n"
    assert templates["global-macos"] == ".DS_Store\n"
    assert "readme" not in templates


def test_update_user_templates(monkeypatch, tmp_path):
    monkeypatch.setattr(core, "USER_TEMPLATES_DIR", tmp_path / "user_templates")
    monkeypatch.setattr(core, "fetch_official_templates", lambda timeout=120: {"zig": "*.zig-cache\n"})
    fetched, new, total = core.update_user_templates()
    assert fetched == 1
    assert new == 1
    assert "zig" in core.available_templates()
    assert core.available_templates()["zig"] == "*.zig-cache\n"


def test_update_user_templates_via_git(monkeypatch, tmp_path):
    monkeypatch.setattr(core, "USER_TEMPLATES_DIR", tmp_path / "user_templates")
    called = {}

    def fake_git_fetcher(timeout=120):
        called["via_git"] = True
        return {"zig": "*.zig-cache\n"}

    monkeypatch.setattr(core, "fetch_official_templates_git", fake_git_fetcher)
    core.update_user_templates(via_git=True)
    assert called.get("via_git") is True


def test_collect_templates_from_dir(tmp_path):
    (tmp_path / "Python.gitignore").write_text("__pycache__/\n")
    (tmp_path / "C++.gitignore").write_text("*.o\n")
    global_dir = tmp_path / "Global"
    global_dir.mkdir()
    (global_dir / "macOS.gitignore").write_text(".DS_Store\n")
    (tmp_path / "README.md").write_text("not a template")
    templates = core._collect_templates_from_dir(tmp_path)
    assert templates["python"] == "__pycache__/\n"
    assert templates["cpp"] == "*.o\n"
    assert templates["global-macos"] == ".DS_Store\n"
