import os
import sys
import subprocess
from unittest.mock import patch, MagicMock
import pytest

from platform_utils import (
    get_platform_font,
    open_in_file_manager,
    get_default_wechat_path,
    should_load_ico,
    normalize_file_path,
)


def test_platform_utils_imported():
    assert get_platform_font is not None
    assert open_in_file_manager is not None
    assert get_default_wechat_path is not None
    assert should_load_ico is not None
    assert normalize_file_path is not None


@pytest.mark.parametrize(
    "plat,expected_family",
    [
        ("win32", "Microsoft YaHei"),
        ("darwin", "PingFang SC"),
        ("linux", "Noto Sans CJK SC"),
    ],
)
def test_get_platform_font(plat, expected_family, monkeypatch):
    monkeypatch.setattr(sys, "platform", plat)
    font_normal = get_platform_font(is_bold=False, size=10)
    assert font_normal[0] == expected_family
    assert font_normal[1] == 10
    assert len(font_normal) == 2

    font_bold = get_platform_font(is_bold=True, size=11)
    assert font_bold[0] == expected_family
    assert font_bold[1] == 11
    assert "bold" in font_bold


def test_should_load_ico(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    assert should_load_ico() is True

    monkeypatch.setattr(sys, "platform", "darwin")
    assert should_load_ico() is False

    monkeypatch.setattr(sys, "platform", "linux")
    assert should_load_ico() is False


def test_get_default_wechat_path(monkeypatch):
    # Windows
    monkeypatch.setattr(sys, "platform", "win32")
    win_path = get_default_wechat_path()
    assert "WeChat Files" in win_path

    # macOS
    monkeypatch.setattr(sys, "platform", "darwin")
    mac_path = get_default_wechat_path()
    assert "com.tencent.xinWeChat" in mac_path

    # Linux
    monkeypatch.setattr(sys, "platform", "linux")
    linux_path = get_default_wechat_path()
    assert linux_path == ""


def test_open_in_file_manager_windows(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    mock_startfile = MagicMock()
    monkeypatch.setattr(os, "startfile", mock_startfile, raising=False)

    open_in_file_manager("C:/test/folder")
    mock_startfile.assert_called_once_with(os.path.normpath("C:/test/folder"))


def test_open_in_file_manager_macos(monkeypatch):
    monkeypatch.setattr(sys, "platform", "darwin")
    with patch("subprocess.Popen") as mock_popen:
        open_in_file_manager("/Users/test/folder")
        mock_popen.assert_called_once_with(["open", "/Users/test/folder"])


def test_open_in_file_manager_linux(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    with patch("subprocess.Popen") as mock_popen:
        open_in_file_manager("/home/test/folder")
        mock_popen.assert_called_once_with(["xdg-open", "/home/test/folder"])


def test_normalize_file_path():
    raw = "some//folder/..//file.txt"
    norm = normalize_file_path(raw)
    assert norm == os.path.abspath(os.path.normpath(raw))
