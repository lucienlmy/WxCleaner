# WxCleaner - 微信重复文件清理工具

WxCleaner 是一款专为清理微信接收文件而设计的轻量级、跨平台桌面工具。它能够高效扫描指定目录，通过智能哈希算法快速识别重复文件，并提供可视化的清理界面，帮助用户安全释放磁盘空间。

## ✨ 核心功能

*   **智能三级扫描**: 采用 "文件大小初筛 -> 头部哈希 (Partial Hash) -> 全量哈希 (Full Hash)" 策略，极大降低磁盘 I/O，极速识别重复文件，确保 100% 准确率。
*   **跨平台兼容**: 原生支持 Windows、macOS 与 Linux，针对不同平台自适应界面字体（微软雅黑 / 苹方 / 思源黑体）与原生文件管理器定位。
*   **可视化预览与排序**: 清晰展示重复文件的序号、路径、大小、修改时间与状态，支持点击表头多维度排序，支持右键直接在系统文件管理器中打开文件位置。
*   **智能标记**: 扫描完成后自动标记建议删除的重复项（默认保留路径较短的文件），支持一键全选。
*   **安全清理**: 
    *   文件并非直接永久物理删除，而是通过 `send2trash` 安全移动至 **系统回收站/废纸篓**，防止误删。
    *   删除前提供二次确认与多线程并发进度弹窗，支持随时安全中止。
*   **现代化 UI**: 基于 `ttkbootstrap` 构建的现代化扁平界面，美观易用，支持深色/浅色主题。

---

## 🛠️ 技术栈

*   **语言**: Python 3.8+
*   **GUI 框架**: [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) (基于 Tkinter)
*   **核心依赖**: 
    *   `send2trash`: 跨平台安全删除（移至系统回收站/废纸篓）。
*   **打包构建**: PyInstaller (Windows `.exe`)

---

## 🚀 快速开始

### 方式一：运行 Windows 可执行文件
在 [Releases](https://github.com/yqxie1991/WxCleaner/releases) 页面下载最新的 `WxCleaner.exe`，双击即可直接运行，无需配置 Python 环境。

### 方式二：源码运行 (Windows / macOS / Linux)

#### 1. 环境要求
确保系统已安装 **Python 3.8** 或更高版本。

> **提示（macOS / Linux 用户）**：
> 部分 Linux 或 Homebrew 安装的 Python 可能未自带 Tkinter，请根据系统安装：
> - **macOS (Homebrew)**: `brew install python-tk`
> - **Ubuntu / Debian**: `sudo apt-get install python3-tk`
> - **Fedora / RHEL**: `sudo dnf install python3-tkinter`
> - **Arch Linux**: `sudo pacman -S tk`

#### 2. 克隆仓库与安装依赖
```bash
git clone https://github.com/yqxie1991/WxCleaner.git
cd WxCleaner

# 推荐创建虚拟环境
python -m venv venv
# Windows 激活:
venv\Scripts\activate
# macOS / Linux 激活:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 运行程序
```bash
python main.py
```

---

## 📖 使用指南

1.  **选择路径**:
    *   程序会自动尝试探测并预填各平台微信默认文件存储目录。
    *   您也可以点击 **"浏览"** 按钮手动选择目标文件夹：
        *   **Windows**: 通常位于 `此电脑/文档/WeChat Files`
        *   **macOS**: 通常位于 `~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/`
        *   **Linux**: 自定义微信数据或下载目录
2.  **开始扫描**: 点击 **"开始扫描"**，程序将在后台异步分析目录下的所有文件并实时显示进度。
3.  **查看结果**: 扫描完成后，列表中会显示所有发现的重复文件组。红色高亮表示建议删除的冗余副本，绿色表示保留项。可通过右键打开文件所在位置确认内容。
4.  **执行清理**: 
    *   可点击 **"全选重复项"** 或手动多选/调整勾选状态。
    *   确认无误后，点击 **"移至回收站"**。
    *   在二次确认弹窗中点击确认，系统将安全地把选中的文件移动到回收站/废纸篓。

---

## 📦 打包构建 (Windows EXE)

如果您想自行打包生成单文件可执行程序：

```bash
pip install pyinstaller
pyinstaller WxCleaner.spec
```
打包完成后，单文件 `WxCleaner.exe` 将输出在 `dist/` 目录下。

---

## ⚠️ 免责声明

本工具旨在帮助用户管理和清理冗余文件，虽然提供了安全删除机制（移至系统回收站），但建议在执行大规模清理前**务必确认文件内容与重要程度**。作者不对因误操作或第三方软件冲突导致的任何数据丢失承担责任。

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。
