# 规格说明 (Specification) - 跨平台兼容性适配 (macOS / Linux)

## 1. 概述 (Overview)
根据 GitHub Issues 反馈 (Issue #3)，当前 WxCleaner 存在多处 Windows 专属硬编码，导致在 macOS 和 Linux 上无法正常运行。本 Track 目标是对 `wx_gui.py` 和 `main.py` 进行代码层面的跨平台适配，使应用在 macOS 和 Linux 上可通过 `python main.py` 正常启动和使用。

## 2. 功能需求 (Functional Requirements)

### FR-1: 「打开文件位置」跨平台适配
- 当前 `open_file_location()` 使用 `os.startfile()`，该 API 仅 Windows 可用。
- 修改为基于 `sys.platform` 的三路分支：
  - **Windows**: 保持 `os.startfile(folder)`
  - **macOS (darwin)**: `subprocess.Popen(["open", folder])`
  - **Linux**: `subprocess.Popen(["xdg-open", folder])`

### FR-2: 字体回退链 (Font Fallback)
- 当前字体硬编码为 `Microsoft YaHei`，macOS/Linux 无此字体会导致界面异常。
- 修改为平台自适应字体选择：
  - **Windows**: `Microsoft YaHei`
  - **macOS**: `PingFang SC`
  - **Linux**: `Noto Sans CJK SC` → 回退至 `WenQuanYi Micro Hei` → 再回退至 `sans-serif`

### FR-3: 图标加载跨平台守卫
- `.ico` 格式仅 Windows Tkinter 原生支持。
- 修改为：仅在 `sys.platform == "win32"` 时加载 `.ico` 图标，其他平台安全跳过。

### FR-4: 默认扫描路径跨平台适配
- 启动时根据平台预填默认微信文件目录（仅当路径存在时预填）：
  - **Windows**: `~/Documents/WeChat Files/`
  - **macOS**: `~/Library/Containers/com.tencent.xinWeChat/`
  - **Linux**: 不预填（微信 Linux 版路径不固定）

### FR-5: DPI/windll 守卫
- `WxCleaner_bundled.py` 中使用的 `ctypes.windll` 仅 Windows 可用。
- 修改为仅在 `sys.platform == "win32"` 时执行 DPI 相关调用。

### FR-6: 路径规范化增强
- 在 `delete_selected()` 中增加 `os.path.normpath()` 规范化路径分隔符，确保跨平台路径一致性。

## 3. 非功能性需求 (Non-Functional Requirements)
- 所有修改必须通过 `sys.platform` 条件分支实现，在 Windows 上无任何行为变更。
- 现有 pytest 测试套件（9 项）必须继续 100% 通过。
- 新增跨平台相关单元测试（字体选择、路径规范化、平台分支）。

## 4. 验收标准 (Acceptance Criteria)
- [ ] `python main.py` 在 Windows 上启动无回归、所有功能正常。
- [ ] 代码中不再存在不受 `sys.platform` 守卫的 Windows 专属 API 调用。
- [ ] pytest 全量测试通过，新增跨平台测试覆盖。
- [ ] 所有提示信息保持中文。

## 5. 范围外 (Out of Scope)
- macOS `.app` / `.dmg` 打包构建。
- Linux `.deb` / `.AppImage` 打包构建。
- 实际在 macOS / Linux 环境上的端到端测试（当前无测试环境）。
