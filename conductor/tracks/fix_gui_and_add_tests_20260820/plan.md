# 实施计划 (Implementation Plan) - 完善 GUI 逻辑与核心测试套件

## Phase 1: 测试框架搭建与扫描算法单测 (TDD) [checkpoint: 41bb68d]
- [x] Task: 配置 pytest 测试框架与 requirements.txt 更新 [f406d2b]
- [x] Task: 编写 scanner.py 单元测试 (`tests/test_scanner.py`) [ea81014]
- [x] Task: 运行 pytest 验证算法测试通过与覆盖率 [41bb68d]
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) [41bb68d]

## Phase 2: 修复并完善 wx_gui.py 功能 [checkpoint: d6e4632]
- [x] Task: 同步补全 wx_gui.py 的 resource_path 与 sort_column 排序逻辑 [d6e4632]
- [x] Task: 补齐 delete_selected 与 show_delete_report 多线程安全删除 [d6e4632]
- [x] Task: 编写删除逻辑 Mock 测试 (`tests/test_gui_utils.py`) [d6e4632]
- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md) [d6e4632]

## Phase 3: 端到端集成与代码质量门禁
- [ ] Task: 运行完整 pytest 测试套件并确保无回归
- [ ] Task: 执行 main.py 入口启动与打包 spec 一致性检查
- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
