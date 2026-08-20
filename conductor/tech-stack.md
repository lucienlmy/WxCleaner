# 技术栈 (Technology Stack) - WxCleaner

## 核心语言与运行时
- **语言**: Python 3.8+
- **目标平台**: Windows (原生支持), 可移植跨平台

## 界面与图形框架 (GUI)
- **GUI 框架**: `ttkbootstrap` (v1.10+) - 提供现代化 Flat 主题、高 DPI 字体适配、现代化组件库。
- **底层支持**: Tkinter (Python 标准库)

## 核心库与系统交互
- **文件去重与哈希**:
  - `hashlib` (SHA-256): 分级（头部 Partial Hash 1024B + 全量 Full Hash）去重算法。
  - `collections.defaultdict`: 高效哈希分组。
- **安全删除**:
  - `send2trash` (v1.8+): 将待清理文件安全发送至系统回收站，避免不可逆丢失。
- **并发与异步调度**:
  - `threading`: 扫描工作线程与 UI 线程解耦。
  - `concurrent.futures.ThreadPoolExecutor`: 多线程批量并发文件回收处理。
- **测试框架与质量门禁**:
  - `pytest`: 单元与集成自动化测试套件。
  - `pytest-cov`: 代码覆盖率统计。
- **系统集成与打包**:
  - `ctypes` (`windll`): Windows 系统层与高分屏适配。
  - `PyInstaller`: 单文件 `.exe` 二进制打包与资源打包集成（`icon.ico`）。
