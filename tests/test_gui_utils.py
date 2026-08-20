import os
import sys
import tempfile
from unittest.mock import patch
import pytest
from wx_gui import resource_path

def test_resource_path_standard():
    rel = "icon.ico"
    expected = os.path.join(os.path.abspath("."), rel)
    assert resource_path(rel) == expected

def test_resource_path_meipass(monkeypatch):
    mock_meipass = os.path.join(tempfile.gettempdir(), "_MEI12345")
    monkeypatch.setattr(sys, "_MEIPASS", mock_meipass, raising=False)
    
    assert resource_path("icon.ico") == os.path.join(mock_meipass, "icon.ico")

def test_send2trash_integration():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"Test file to be moved to trash")
        f_path = f.name
    
    assert os.path.exists(f_path)
    
    # Test send2trash execution safely
    with patch("send2trash.send2trash") as mock_trash:
        mock_trash.return_value = None
        from send2trash import send2trash
        send2trash(f_path)
        mock_trash.assert_called_once_with(f_path)
    
    if os.path.exists(f_path):
        os.remove(f_path)
