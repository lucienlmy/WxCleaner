# 技术栈 (Technology Stack) - WxCleaner

## 核心语言与运行时
- **语言**: Python 3.8+
- **目标平台**: Windows、macOS (Darwin)、Linux (跨平台兼容)

## 界面与图形框架 (GUI)
- **GUI 框架**: `ttkbootstrap` (v1.10+) - 提供现代化 Flat 主题、自适应字体与高 DPI 适配、现代化组件库。
- **底层支持**: Tkinter (Python 标准库)

## 核心库与系统交互
- **跨平台工具支持**:
  - `platform_utils.py`: 操作系统自适应字体、跨平台文件管理器唤起、微信默认存储目录自动探测、ICO 图标平台守卫。
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
  - `PyInstaller`: 二进制打包与资源打包集成（`icon.ico`）。
