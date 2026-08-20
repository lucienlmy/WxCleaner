# GitHub反馈Issues 1——v1.0.0 crashes on startup: delete_selected is missing from wx_gui.py 


Reproduction
On the v1.0.0 tag / current main:

uv venv --python 3.13
.venv\Scripts\activate
uv pip install -r requirements.txt
python main.py
The application crashes while building the UI:

AttributeError: 'WxCleanerApp' object has no attribute 'delete_selected'
wx_gui.py binds the "移至回收站" button to self.delete_selected, but the WxCleanerApp class does not define that method. The same source file also lacks sort_column, although it is referenced by the table headings.

The repository's WxCleaner_bundled.py still contains implementations of these methods, which suggests they were accidentally omitted during the refactor/cleanup release.

# GitHub反馈Issues 2——Python3.9环境下运行出错'WxCleanerApp' object has no attribute 'delete_selected'

WxCleaner (main -> origin)> python main.py
Traceback (most recent call last):
File "C:\Users\c\Desktop\WxCleaner\main.py", line 8, in
app = WxCleanerApp(root)
File "C:\Users\c\Desktop\WxCleaner\wx_gui.py", line 42, in init
self.setup_ui()
File "C:\Users\c\Desktop\WxCleaner\wx_gui.py", line 130, in setup_ui
ttk.Button(btn_frame, text="移至回收站", command=self.delete_selected, bootstyle="danger").pack(side=LEFT, padx=5)
AttributeError: 'WxCleanerApp' object has no attribute 'delete_selected'

wx_gui.py文件最后添加方法可解决：

    def delete_selected(self):
        """将 Treeview 中选中的项目移至回收站"""
        import tkinter.messagebox as msgbox
        # 获取所有选中的 item ID
        selected_items = self.tree.selection()
        if not selected_items:
            msgbox.showwarning("未选择", "请先在表格中选择要删除的项目")
            return

        # 确认对话框
        count = len(selected_items)
        if not msgbox.askyesno("确认删除", f"确定要将 {count} 个项目移至回收站吗？"):
            return

        errors = []
        for item in selected_items:
            file_path = self.tree.set(item, "path")  # 列名为 "path"
            # 👇 关键修复：规范化路径，统一分隔符
            file_path = os.path.normpath(file_path)
            if not file_path or not os.path.exists(file_path):
                errors.append(f"路径无效或不存在: {file_path}")
                continue

            try:
                send2trash(file_path)
            except Exception as e:
                errors.append(f"删除失败: {file_path}\n{str(e)}")

        # 如果有错误则汇总提示
        if errors:
            msgbox.showerror("部分操作失败", "\n".join(errors))
        for item in selected_items:
            if self.tree.exists(item):
                self.tree.delete(item)
				
				
# GitHub反馈Issues 3——希望可以出一个mac版本

这个项目Mac可以用的，但是需要稍微修改一下wx_gui.py里面的代码，我改好了，同时把 delete_selected 里关于 macOS 下的路径打开方式也做了兼容处理（原版本里写的 os.startfile 是windows专属，Mac用会报错）。使用macOS的小伙伴替换一下这个文件即可使用～

if sys.platform == "darwin":
        default_path = os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/")  设了默认 mac 下的扫描路径 