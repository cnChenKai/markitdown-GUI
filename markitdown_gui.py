import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from markitdown import MarkItDown

class MarkItDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown GUI")
        self.root.geometry("600x400")

        # 初始化MarkItDown
        self.md = MarkItDown()

        # 文件选择
        self.file_frame = ttk.LabelFrame(root, text="输入文件", padding="10")
        self.file_frame.pack(fill="x", padx=10, pady=5)

        self.file_listbox = tk.Listbox(self.file_frame, height=4)
        self.file_listbox.pack(side="left", fill="both", expand=True)

        self.button_frame = ttk.Frame(self.file_frame)
        self.button_frame.pack(side="right", fill="y")

        ttk.Button(self.button_frame, text="添加文件", command=self.add_files).pack(fill="x", pady=2)
        ttk.Button(self.button_frame, text="移除选中", command=self.remove_selected).pack(fill="x", pady=2)
        ttk.Button(self.button_frame, text="清空列表", command=self.clear_files).pack(fill="x", pady=2)

        # 输出路径
        self.output_frame = ttk.LabelFrame(root, text="输出路径", padding="10")
        self.output_frame.pack(fill="x", padx=10, pady=5)

        self.output_entry = ttk.Entry(self.output_frame)
        self.output_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(self.output_frame, text="选择文件夹", command=self.select_output_dir).pack(side="right")

        # 转换按钮
        self.convert_button = ttk.Button(root, text="开始转换", command=self.start_conversion)
        self.convert_button.pack(pady=10)

        # 状态显示
        self.status_frame = ttk.LabelFrame(root, text="转换状态", padding="10")
        self.status_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.status_text = tk.Text(self.status_frame, height=10, state="disabled")
        self.status_text.pack(fill="both", expand=True)

        # 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        self.progress.pack(fill="x", padx=10, pady=5)

        self.files = []

    def add_files(self):
        filetypes = [
            ("所有支持的文件", "*.pdf;*.docx;*.pptx;*.xlsx;*.xls;*.txt;*.html;*.epub;*.jpg;*.png;*.mp3;*.wav;*.m4a"),
            ("PDF文件", "*.pdf"),
            ("Word文档", "*.docx"),
            ("PowerPoint", "*.pptx"),
            ("Excel文件", "*.xlsx;*.xls"),
            ("文本文件", "*.txt"),
            ("HTML文件", "*.html"),
            ("EPUB文件", "*.epub"),
            ("图片文件", "*.jpg;*.png;*.jpeg;*.gif;*.bmp"),
            ("音频文件", "*.mp3;*.wav;*.m4a"),
            ("所有文件", "*.*")
        ]

        files = filedialog.askopenfilenames(filetypes=filetypes)
        for file in files:
            if file not in self.files:
                self.files.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))

    def remove_selected(self):
        selected = self.file_listbox.curselection()
        if selected:
            index = selected[0]
            self.file_listbox.delete(index)
            del self.files[index]

    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.files.clear()

    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)

    def start_conversion(self):
        if not self.files:
            messagebox.showerror("错误", "请先选择要转换的文件")
            return

        output_dir = self.output_entry.get().strip()
        if not output_dir:
            # 使用第一个文件的目录作为默认输出目录
            output_dir = os.path.dirname(self.files[0])

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"创建输出目录失败: {e}")
                return

        self.convert_button.config(state="disabled")
        self.progress.start()
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "开始转换...\n")
        self.status_text.config(state="disabled")

        # 在后台线程中执行转换
        thread = threading.Thread(target=self.convert_files, args=(output_dir,))
        thread.start()

    def convert_files(self, output_dir):
        try:
            for i, file_path in enumerate(self.files):
                self.update_status(f"正在转换: {os.path.basename(file_path)}\n")

                try:
                    result = self.md.convert(file_path)

                    # 生成输出文件名
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_file = os.path.join(output_dir, f"{base_name}.md")

                    # 保存结果
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(result.text_content)

                    self.update_status(f"✓ 转换完成: {os.path.basename(output_file)}\n")

                except Exception as e:
                    self.update_status(f"✗ 转换失败 {os.path.basename(file_path)}: {str(e)}\n")

            self.update_status("所有文件转换完成！\n")

        except Exception as e:
            self.update_status(f"转换过程中发生错误: {str(e)}\n")

        finally:
            self.root.after(0, self.conversion_finished)

    def update_status(self, message):
        self.root.after(0, lambda: self._update_status_text(message))

    def _update_status_text(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

    def conversion_finished(self):
        self.progress.stop()
        self.convert_button.config(state="normal")
        messagebox.showinfo("完成", "文件转换完成！")

def main():
    root = tk.Tk()
    app = MarkItDownGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()