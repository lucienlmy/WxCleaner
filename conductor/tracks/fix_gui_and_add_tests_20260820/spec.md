# 规格说明 (Specification) - 完善 GUI 逻辑与核心测试套件

## 1. 概述 (Overview)
修复 `wx_gui.py` 中因历史原因遗漏/截断的清理与排序函数，使其与模块化入口 `main.py` 及单文件打包版逻辑保持一致；同时搭建 `pytest` 测试套件，对 `scanner.py` 的三级筛选算法及回收站删除逻辑实现高覆盖率自动化测试。

## 2. 功能需求 (Functional Requirements)
1. **补齐 `wx_gui.py` 功能**:
   - 补全 `delete_selected`（支持多线程并发移至回收站、进度弹窗与中止）。
   - 补齐 `show_delete_report`（清理结果与错误报告）。
   - 补齐 `sort_column`（Treeview 序号、大小、路径等多列排序）。
   - 引入 `resource_path` 兼容资源文件定位。
2. **测试架构搭建**:
   - 新建 `tests/` 目录及 `pytest` 配置文件。
3. **扫描算法测试套件 (`test_scanner.py`)**:
   - 测试 `calculate_hash`（全量哈希、前 1024 字节头部哈希、异常文件处理）。
   - 测试 `find_duplicates`（空文件过滤、不同大小文件、同大小不同内容、同头部不同尾部、真实重复文件的三级筛选流程）。
   - 测试进度回调函数（Progress Callback）的正确触发与进度递增。
4. **清理与删除逻辑测试 (`test_deletion.py`)**:
   - 对 `send2trash` 进行 Mock 测试，验证批量并发删除与错误捕获统计。

## 3. 验收标准 (Acceptance Criteria)
- [ ] `pytest` 测试全部通过，核心算法测试覆盖率达标 (>85%)。
- [ ] 运行 `python main.py`，图形界面能够正常进行扫描、排序、全选重复项并弹出删除进度窗口。
- [ ] 所有错误与提示信息均以中文输出。
