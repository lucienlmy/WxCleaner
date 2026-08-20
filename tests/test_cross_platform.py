import os
import sys
import subprocess
from unittest.mock import patch, MagicMock
import pytest

# 导入跨平台工具函数（Red Phase 此时可能尚未实现）
try:
    from platform_utils import (
        get_platform_font,
        open_in_file_manager,
        get_default_wechat_path,
        should_load_ico,
        normalize_file_path,
    )
except ImportError:
    # 允许 Red Phase 下捕获导入错误并暴露断言
    get_platform_font = None
    open_in_file_manager = None
    get_default_wechat_path = None
    should_load_ico = None
    normalize_file_path = None


def test_platform_utils_imported():
    assert get_platform_font is not None, "platform_utils.get_platform_font 未实现"
    assert open_in_file_manager is not None, "platform_utils.open_in_file_manager 未实现"
    assert get_default_wechat_path is not None, "platform_utils.get_default_wechat_path 未实现"
    assert should_load_ico is not None, "platform_utils.should_load_ico 未实现"
    assert normalize_file_path is not None, "platform_utils.normalize_file_path 未实现"


@pytest.mark.parametrize(
    "plat,expected_family",
    [
        ("win32", "Microsoft YaHei"),
        ("darwin", "PingFang SC"),
        ("linux", "Noto Sans CJK SC"),
    ],
)
def test_get_platform_font(plat, expected_family, monkeypatch):
    if get_platform_font is None:
        pytest.fail("get_platform_font 未定义")
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
    if should_load_ico is None:
        pytest.fail("should_load_ico 未定义")
    monkeypatch.setattr(sys, "platform", "win32")
    assert should_load_ico() is True

    monkeypatch.setattr(sys, "platform", "darwin")
    assert should_load_ico() is False

    monkeypatch.setattr(sys, "platform", "linux")
    assert should_load_ico() is False


def test_get_default_wechat_path(monkeypatch):
    if get_default_wechat_path is None:
        pytest.fail("get_default_wechat_path 未定义")
    
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
    if open_in_file_manager is None:
        pytest.fail("open_in_file_manager 未定义")
    monkeypatch.setattr(sys, "platform", "win32")
    mock_startfile = MagicMock()
    monkeypatch.setattr(os, "startfile", mock_startfile, raising=False)

    open_in_file_manager("C:/test/folder")
    mock_startfile.assert_called_once_with("C:/test/folder")


def test_open_in_file_manager_macos(monkeypatch):
    if open_in_file_manager is None:
        pytest.fail("open_in_file_manager 未定义")
    monkeypatch.setattr(sys, "platform", "darwin")
    with patch("subprocess.Popen") as mock_popen:
        open_in_file_manager("/Users/test/folder")
        mock_popen.assert_called_once_with(["open", "/Users/test/folder"])


def test_open_in_file_manager_linux(monkeypatch):
    if open_in_file_manager is None:
        pytest.fail("open_in_file_manager 未定义")
    monkeypatch.setattr(sys, "platform", "linux")
    with patch("subprocess.Popen") as mock_popen:
        open_in_file_manager("/home/test/folder")
        mock_popen.assert_called_once_with(["xdg-open", "/home/test/folder"])


def test_normalize_file_path():
    if normalize_file_path is None:
        pytest.fail("normalize_file_path 未定义")
    raw = "some//folder/..//file.txt"
    norm = normalize_file_path(raw)
    assert norm == os.path.abspath(os.path.normpath(raw))
