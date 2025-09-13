import asyncio
import sys
import threading
import subprocess  # 添加subprocess模块用于运行外部脚本
from typing import Optional
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import cmd_arg
import config
from database import db
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from media_platform.zhihu import ZhihuCrawler


class CrawlerFactory:
    CRAWLERS = {
        # "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        # "bili": BilibiliCrawler,
        # "wb": WeiboCrawler,
        # "tieba": TieBaCrawler,
        # "zhihu": ZhihuCrawler,
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError(
                "Invalid Media Platform Currently only supported xhs or dy or ks or bili ..."
            )
        return crawler_class()


class CrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("社交媒体爬虫工具")
        self.root.geometry("800x700")  # 增加高度以容纳新控件
        self.root.minsize(700, 600)
        
        self.crawler: Optional[AbstractCrawler] = None
        self.is_running = False
        self.asyncio_loop = None
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 启动asyncio事件循环
        self.start_asyncio_loop()
        
        # 处理窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Title.TLabel", font=("Arial", 14, "bold"), background="#f0f0f0")
        style.configure("Button.TButton", font=("Arial", 10))
        style.configure("Red.TButton", font=("Arial", 10), background="#ff6b6b")
        style.map("Red.TButton", background=[("active", "#ff4b4b")])

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置行列权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)  # 增加行数以容纳新控件
        
        # 标题
        title_label = ttk.Label(main_frame, text="社交媒体爬虫工具", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 平台选择
        ttk.Label(main_frame, text="选择平台:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.platform_var = tk.StringVar(value="dy")
        platform_combo = ttk.Combobox(main_frame, textvariable=self.platform_var, 
                                     values=list(CrawlerFactory.CRAWLERS.keys()))
        platform_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 登录类型选择
        ttk.Label(main_frame, text="登录类型:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.login_type_var = tk.StringVar(value="qrcode")
        login_type_combo = ttk.Combobox(main_frame, textvariable=self.login_type_var, 
                                       values=["qrcode", "phone", "cookie"])
        login_type_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 爬取类型选择
        ttk.Label(main_frame, text="爬取类型:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.crawl_type_var = tk.StringVar(value="search")
        crawl_type_combo = ttk.Combobox(main_frame, textvariable=self.crawl_type_var, 
                                       values=["search", "detail", "user"])
        crawl_type_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 关键词输入
        ttk.Label(main_frame, text="关键词(英文逗号分割):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.keywords_var = tk.StringVar()
        keywords_entry = ttk.Entry(main_frame, textvariable=self.keywords_var)
        keywords_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="开始爬取", command=self.start_crawler, style="Button.TButton")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_crawler, style="Red.TButton", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 日志输出
        ttk.Label(main_frame, text="运行日志:").grid(row=6, column=0, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=20)
        self.log_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def start_asyncio_loop(self):
        """在后台线程中启动asyncio事件循环"""
        def run_loop():
            self.asyncio_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.asyncio_loop)
            self.asyncio_loop.run_forever()
            
        self.thread = threading.Thread(target=run_loop, daemon=True)
        self.thread.start()
        
    def log_message(self, message):
        """向日志区域添加消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def set_status(self, status):
        """更新状态栏"""
        self.status_var.set(status)
        
    def start_crawler(self):
        """开始爬取"""
        if self.is_running:
            return
            
        # 验证输入
        keywords = self.keywords_var.get().strip()
        if not keywords:
            messagebox.showerror("错误", "请输入关键词")
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        # 获取用户选择的参数
        platform = self.platform_var.get()
        login_type = self.login_type_var.get()
        crawl_type = self.crawl_type_var.get()
        keywords = self.keywords_var.get()
 
        self.log_message(f"开始爬取平台: {platform}")
        self.log_message(f"登录类型: {login_type}")
        self.log_message(f"爬取类型: { crawl_type}")
        self.log_message(f"关键词: {keywords}")
        
        # 设置配置参数（模拟命令行参数）
        config.PLATFORM = platform
        config.LOGIN_TYPE = login_type
        config.CRAWLER_TYPE = crawl_type
        config.KEYWORDS = keywords
        
        # 使用asyncio运行爬虫
        future = asyncio.run_coroutine_threadsafe(self.run_crawler(platform), self.asyncio_loop)
        future.add_done_callback(self.on_crawler_finished)
        
    async def run_crawler(self, platform):
        """运行爬虫的异步函数"""
        try:
            self.crawler = CrawlerFactory.create_crawler(platform=platform)
            await self.crawler.start()
            self.log_message("爬取完成")
            
        except Exception as e:
            self.log_message(f"错误: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
        finally:
            # 通知主线程爬虫已完成
            self.root.after(0, self.on_crawler_finished, None)
            
    def on_crawler_finished(self, future=None):
        """爬虫完成时的回调"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.set_status("就绪")
        
    def stop_crawler(self):
        """停止爬虫"""
        if not self.is_running:
            return
            
        self.log_message("正在停止爬虫...")
        self.set_status("正在停止...")
        
        self.force_close()
        
        # 这里需要实现实际的停止逻辑
        # 由于爬虫运行在另一个线程中，我们需要通知它停止
        # if self.crawler:
        #     # 假设crawler有一个stop方法
        #     if hasattr(self.crawler, 'stop'):
        #         asyncio.run_coroutine_threadsafe(self.crawler.stop(), self.asyncio_loop)
        
    def run_comment_filter(self):
        """运行commentFilter.py脚本"""
        try:
            # 使用当前Python解释器运行commentFilter.py
            subprocess.run([sys.executable, "tools\commentFilter.py"], check=True)
            self.log_message("评论筛选完成")
        except subprocess.CalledProcessError as e:
            self.log_message(f"运行评论筛选时出错: {e}")
        except Exception as e:
            self.log_message(f"运行评论筛选时发生意外错误: {e}")
        
    def cleanup(self):
        """清理资源"""
        if self.crawler:
            # 异步清理
            future = asyncio.run_coroutine_threadsafe(self.crawler.close(), self.asyncio_loop)
            try:
                future.result(timeout=5)  # 等待5秒
            except:
                pass
                
        if config.SAVE_DATA_OPTION in ["db", "sqlite"]:
            future = asyncio.run_coroutine_threadsafe(db.close(), self.asyncio_loop)
            try:
                future.result(timeout=5)  # 等待5秒
            except:
                pass
                
        # 停止asyncio事件循环
        if self.asyncio_loop:
            self.asyncio_loop.call_soon_threadsafe(self.asyncio_loop.stop)
            
    def on_closing(self):
        """处理窗口关闭事件"""
        if self.is_running:
            if messagebox.askokcancel("退出", "爬虫正在运行，确定要退出吗？"):
               self.force_close()
        else:
            self.force_close()
            
    def force_close(self):
        """强制关闭窗口"""
        self.cleanup()
        self.root.destroy()
        # 关闭后运行commentFilter.py
        self.run_comment_filter()


def main():
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()