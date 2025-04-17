from pathlib import Path
from typing import Union

from scripts.add_init_files import ensure_init_files


def test_ensure_init_files(tmp_path: Union[str, Path]) -> None:
    # Ensure tmp_path is a Path object
    tmp_path = Path(tmp_path)
    pkg_path = tmp_path / "newpackage"
    pkg_path.mkdir()
    (pkg_path / "sample.py").write_text("print('hello')")

    assert not (pkg_path / "__init__.py").exists()

    ensure_init_files(str(tmp_path))

    assert (pkg_path / "__init__.py").exists()
    assert (pkg_path / "__init__.py").read_text().startswith("# Automatically added")
