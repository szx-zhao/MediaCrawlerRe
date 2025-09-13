import csv
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Set, Optional
import datetime  # 添加datetime模块用于生成时间戳

class CSVKeywordFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV关键词筛选工具")
        self.root.geometry("600x500")
        self.encoding = 'utf-8-sig'
        
        # 设置默认目录
        self.default_csv_dir = os.path.join(os.getcwd(), "data", "douyin", "csv")
        os.makedirs(self.default_csv_dir, exist_ok=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="CSV关键词筛选工具", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 输入文件选择
        ttk.Label(main_frame, text="输入文件:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.input_file_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_file_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Button(main_frame, text="浏览...", command=self.select_input_file).grid(row=1, column=2, padx=(5, 0))
        
        # 关键词输入
        ttk.Label(main_frame, text="关键词(逗号分隔):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.keywords_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.keywords_var, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # 输出文件选择
        ttk.Label(main_frame, text="输出文件:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.output_file_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_file_var, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Button(main_frame, text="浏览...", command=self.select_output_file).grid(row=3, column=2, padx=(5, 0))
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # 结果信息
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(main_frame, textvariable=self.result_var, foreground="green")
        self.result_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="开始筛选", command=self.start_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="打开输出目录", command=self.open_output_dir).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="选择CSV文件",
            initialdir=self.default_csv_dir,
            filetypes=[
                ("CSV文件", "*.csv"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.input_file_var.set(file_path)
            # 自动生成输出文件名
            self.auto_generate_output_filename()
    
    def select_output_file(self):
        if not self.input_file_var.get():
            messagebox.showwarning("警告", "请先选择输入文件")
            return
            
        default_filename = self.generate_output_filename()
        file_path = filedialog.asksaveasfilename(
            title="保存筛选结果",
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[
                ("CSV文件", "*.csv"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.output_file_var.set(file_path)
    
    def auto_generate_output_filename(self):
        if self.input_file_var.get() and self.keywords_var.get():
            output_file = self.generate_output_filename()
            self.output_file_var.set(output_file)
    
    def generate_output_filename(self):
        input_file = self.input_file_var.get()
        keywords = self.keywords_var.get().split(",")
        
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        keyword_str = "_".join([kw.strip() for kw in keywords[:2] if kw.strip()])
        
        # 添加时间戳确保文件名唯一
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.dirname(input_file)
        
        return os.path.join(output_dir, f"{base_name}_筛选_{keyword_str}_{timestamp}.csv")
    
    def start_filter(self):
        # 验证输入
        if not self.input_file_var.get():
            messagebox.showerror("错误", "请选择输入文件")
            return
            
        if not self.keywords_var.get():
            messagebox.showerror("错误", "请输入关键词")
            return
            
        if not self.output_file_var.get():
            messagebox.showerror("错误", "请选择输出文件")
            return
        
        # 获取关键词列表
        keywords = [kw.strip() for kw in self.keywords_var.get().split(",") if kw.strip()]
        
        # 开始处理
        self.progress.start()
        self.result_var.set("正在筛选数据...")
        self.root.update()
        
        try:
            result_file = self.filter_csv_by_keywords(
                self.input_file_var.get(), 
                keywords, 
                self.output_file_var.get()
            )
            
            # 统计结果
            with open(result_file, 'r', encoding=self.encoding) as f:
                line_count = sum(1 for line in f) - 1  # 减去标题行
            
            self.result_var.set(f"筛选完成！找到 {line_count} 条匹配记录")
            messagebox.showinfo("完成", f"筛选完成！\n找到 {line_count} 条匹配记录\n文件已保存至: {result_file}")
            
        except Exception as e:
            self.result_var.set("处理失败")
            messagebox.showerror("错误", f"处理过程中出错: {e}")
        finally:
            self.progress.stop()
    
    def filter_csv_by_keywords(self, input_file: str, keywords: List[str], output_file: str) -> str:
        """根据关键词筛选CSV文件内容"""
        # 验证输入文件是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件不存在: {input_file}")
        
        # 预处理关键词
        processed_keywords = [kw.lower().strip() for kw in keywords if kw.strip()]
        
        if not processed_keywords:
            raise ValueError("没有提供有效的关键词")
        
        # 读取并筛选数据
        filtered_rows = []
        with open(input_file, 'r', encoding=self.encoding, newline='') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            
            for row in reader:
                content = row.get('content', '')
                if content and self._contains_any_keyword(content, processed_keywords):
                    filtered_rows.append(row)
        
        # 写入筛选后的数据
        with open(output_file, 'w', encoding=self.encoding, newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)
        
        return output_file
    
    def _contains_any_keyword(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含任何关键词(不区分大小写)"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def open_output_dir(self):
        output_file = self.output_file_var.get()
        if output_file and os.path.exists(output_file):
            os.startfile(os.path.dirname(output_file))
        else:
            messagebox.showwarning("警告", "输出文件不存在或未设置")

def main():
    """主函数"""
    root = tk.Tk()
    app = CSVKeywordFilterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()