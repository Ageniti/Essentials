from __future__ import annotations

from pathlib import Path

import pytest

from essentials.config.paths import get_config_dir, get_config_file_path, get_data_dir, get_logs_dir
from essentials.config.settings import resolve_settings_path


def test_resolve_settings_path_returns_none_for_empty_input() -> None:
    assert resolve_settings_path(None) is None
    assert resolve_settings_path("   ") is None


def test_resolve_settings_path_returns_resolved_existing_path(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("{}", encoding="utf-8")

    assert resolve_settings_path(str(settings_file)) == settings_file.resolve()


def test_resolve_settings_path_rejects_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"

    with pytest.raises(ValueError, match="--settings path does not exist"):
        resolve_settings_path(str(missing))


def test_path_helpers_honor_environment_overrides(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"
    logs_dir = tmp_path / "logs"
    monkeypatch.setenv("ESSENTIALS_CONFIG_DIR", str(config_dir))
    monkeypatch.setenv("ESSENTIALS_DATA_DIR", str(data_dir))
    monkeypatch.setenv("ESSENTIALS_LOGS_DIR", str(logs_dir))

    assert get_config_dir() == config_dir
    assert get_config_file_path() == config_dir / "settings.json"
    assert get_data_dir() == data_dir
    assert get_logs_dir() == logs_dir
    assert config_dir.is_dir()
    assert data_dir.is_dir()
    assert logs_dir.is_dir()
