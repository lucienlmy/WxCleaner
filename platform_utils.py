import os
import sys
import subprocess


def get_platform_font(is_bold=False, size=10):
    """
    根据运行操作系统返回适配的字体元组配置。
    - Windows: Microsoft YaHei
    - macOS: PingFang SC
    - Linux: Noto Sans CJK SC
    """
    if sys.platform == "darwin":
        font_family = "PingFang SC"
    elif sys.platform == "win32":
        font_family = "Microsoft YaHei"
    else:
        # Linux 及其他 Unix-like 系统
        font_family = "Noto Sans CJK SC"

    if is_bold:
        return (font_family, size, "bold")
    return (font_family, size)


def should_load_ico():
    """
    检测当前系统是否适合加载 .ico 格式的窗口图标。
    .ico 仅在 Windows 下被原生 Tkinter 良好支持，macOS/Linux 应跳过。
    """
    return sys.platform == "win32"


def get_default_wechat_path():
    """
    获取不同操作系统下微信接收文件的默认存储路径。
    - Windows: ~/Documents/WeChat Files
    - macOS: ~/Library/Containers/com.tencent.xinWeChat/
    - Linux: 无固定标准路径，返回空字符串
    """
    if sys.platform == "win32":
        return os.path.join(os.path.expanduser("~"), "Documents", "WeChat Files")
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/")
    return ""


def open_in_file_manager(folder_path):
    """
    跨平台打开文件管理器并定位到指定目录。
    - Windows: os.startfile
    - macOS: open
    - Linux: xdg-open
    """
    if sys.platform == "win32":
        os.startfile(os.path.normpath(folder_path))
    elif sys.platform == "darwin":
        subprocess.Popen(["open", folder_path])
    else:
        subprocess.Popen(["xdg-open", folder_path])


def normalize_file_path(path):
    """
    跨平台规范化路径，统一消除冗余分隔符与相对符号并转为绝对路径。
    """
    return os.path.abspath(os.path.normpath(path))
