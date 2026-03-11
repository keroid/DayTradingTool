import tkinter as tk
from tkinter import ttk, messagebox
import traceback

class TCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("T+0 交易计算器")
        self.root.geometry("800x500")
        
        # 设置现代化配色方案
        self.setup_colors()
        
        # 配置ttk样式
        self.setup_styles()
        
        # 创建左右分栏主容器
        main_container = tk.Frame(root, bg=self.bg_color)
        main_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # 左侧输入区域
        left_frame = tk.Frame(main_container, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 右侧结果区域
        right_frame = tk.Frame(main_container, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 标题（放在左侧顶部）
        title_label = tk.Label(left_frame, text="T+0 交易计算器", 
                              font=("微软雅黑", 14, "bold"), 
                              bg=self.bg_color, fg=self.text_color)
        title_label.pack(pady=(0, 15))
        
        # 创建输入区域
        self.create_input_area(left_frame)
        
        # 创建结果显示区域
        self.create_result_area(right_frame)
    
    def setup_colors(self):
        """设置现代化配色方案"""
        self.bg_color = "#f8fafc"  # 更浅的背景色
        self.text_color = "#1e293b"  # 深蓝色文字
        self.accent_color = "#3b82f6"  # 明亮的蓝色
        self.card_bg = "#ffffff"  # 卡片背景色
        self.border_color = "#e2e8f0"  # 边框色
    
    def setup_styles(self):
        """配置ttk样式"""
        self.style = ttk.Style()
        # 使用默认主题
        # 配置按钮样式
        self.style.configure("TButton",
                           padding=8,
                           background=self.accent_color,
                           foreground="white",
                           font=("微软雅黑", 10, "bold"))
        
        # 按钮鼠标悬停效果
        self.style.map("TButton",
                     background=[('active', '#2563eb'), ('!active', self.accent_color)])
    
    def create_input_area(self, parent):
        """创建简化的输入区域"""
        # 使用预定义的圆角样式
        # 输入区域框架 - 使用透明背景，减少框线
        input_frame = tk.Frame(parent, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 紧凑的输入字段布局
        fields = [
            ("当前股价 (元)", "50"),
            ("交易手数", "10"),
            ("总税费 (元)", "10"),
            ("目标盈利 (元)", "0")
        ]
        
        self.entries = {}
        for i, (label_text, default_value) in enumerate(fields):
            # 标签 - 使用更简洁的样式
            label = tk.Label(input_frame, text=label_text, 
                           bg=self.bg_color, fg=self.text_color,
                           font=("微软雅黑", 10))
            label.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=5)
            
            # 输入框 - 使用ttk Entry以获得更好样式
            entry = ttk.Entry(input_frame, width=25, font=("微软雅黑", 10))
            entry.grid(row=i, column=1, sticky="w", pady=5)
            entry.insert(0, default_value)
            
            # 存储引用
            key = label_text.split(" (")[0]  # 使用括号分割，获取"当前股价"而不是"当前"
            self.entries[key] = entry
        
        # T类型选择 - 简化布局
        self.t_type = tk.StringVar(value="正T")
        
        # 使用Frame包装单选按钮，但减少边框
        type_frame = tk.Frame(input_frame, bg=self.bg_color)
        type_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")
        
        rb1 = tk.Radiobutton(type_frame, text="正T (先买后卖)", variable=self.t_type, value="正T",
                            bg=self.bg_color, fg=self.text_color, selectcolor=self.accent_color,
                            font=("微软雅黑", 10))
        rb1.pack(side=tk.LEFT, padx=(0, 15))
        
        rb2 = tk.Radiobutton(type_frame, text="反T (先卖后买)", variable=self.t_type, value="反T",
                            bg=self.bg_color, fg=self.text_color, selectcolor=self.accent_color,
                            font=("微软雅黑", 10))
        rb2.pack(side=tk.LEFT)
        
        # 计算按钮 - 使用ttk Button获得更好样式
        calc_btn = ttk.Button(input_frame, text="开始计算", command=self.calculate)
        calc_btn.grid(row=5, column=0, columnspan=2, pady=12)
        
        # 配置列权重
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
    
    def create_result_area(self, parent):
        """创建简化的结果显示区域"""
        # 结果标题
        result_title = tk.Label(parent, text="计算结果", 
                               font=("微软雅黑", 12, "bold"), 
                               bg=self.bg_color, fg=self.text_color)
        result_title.pack(pady=(0, 8))
        
        # 创建可滚动结果区域容器
        result_container = tk.Frame(parent, bg=self.bg_color)
        result_container.pack(fill=tk.BOTH, expand=True)
        
        # 创建Canvas和Scrollbar用于滚动
        self.result_canvas = tk.Canvas(result_container, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(result_container, orient="vertical", command=self.result_canvas.yview)
        
        # 创建可滚动的内部框架
        self.result_inner_frame = tk.Frame(self.result_canvas, bg="#ffffff")
        
        # 配置Canvas
        self.result_canvas.configure(yscrollcommand=scrollbar.set)
        self.result_canvas.create_window((0, 0), window=self.result_inner_frame, anchor="nw")
        
        # 布局
        self.result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定事件以更新滚动区域
        def configure_scroll_region(_):
            self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))
        
        self.result_inner_frame.bind("<Configure>", configure_scroll_region)
        
        # 存储结果标签
        self.result_labels = []
    
    def clear_result_area(self):
        """清除结果区域"""
        for widget in self.result_inner_frame.winfo_children():
            widget.destroy()
        self.result_labels = []
    
    def add_result_line(self, text, font_size=10, is_bold=False, color=None, pady=2):
        """添加一行结果文本"""
        if color is None:
            color = self.text_color
        
        font_style = "微软雅黑"
        if is_bold:
            font_style = ("微软雅黑", font_size, "bold")
        else:
            font_style = ("微软雅黑", font_size)
        
        label = tk.Label(self.result_inner_frame, text=text, 
                        bg="#ffffff", fg=color,
                        font=font_style, justify=tk.LEFT, anchor="w")
        label.pack(fill=tk.X, pady=pady)
        self.result_labels.append(label)
        
    def calculate(self):
        try:
            # 获取输入值
            price_str = self.entries["当前股价"].get().strip()
            hands_str = self.entries["交易手数"].get().strip()
            tax_str = self.entries["总税费"].get().strip()
            profit_str = self.entries["目标盈利"].get().strip()
            t_type = self.t_type.get()
            
            # 验证并转换数字
            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError("股价必须大于0")
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的股价（大于0的数字）")
                return
                
            try:
                hands = int(float(hands_str))
                if hands <= 0:
                    raise ValueError("手数必须大于0")
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的手数（大于0的整数）")
                return
                
            try:
                total_tax = float(tax_str)
                if total_tax < 0:
                    raise ValueError("税费不能为负数")
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的税费（大于等于0的数字）")
                return
                
            try:
                profit_target = float(profit_str)
                if profit_target < 0:
                    raise ValueError("目标盈利不能为负数")
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的目标盈利（大于等于0的数字）")
                return
            
            # 执行计算
            shares = hands * 100
            diff_needed = (2 * total_tax + profit_target) / shares
            
            if t_type == "正T":
                action_desc = "卖出价需比买入价高"
                target_price = price + diff_needed
            else:
                action_desc = "买入价需比卖出价低"
                target_price = price - diff_needed
            
            percent_needed = (diff_needed / price) * 100
            
            # 清除并显示新的结果
            self.clear_result_area()
            
            # 显示简洁的结果
            self.add_result_line(f"{t_type}交易策略分析", 12, True, pady=8)
            
            self.add_result_line("交易信息", 11, True, pady=5)
            self.add_result_line(f"   当前股价: {price:.2f} 元")
            self.add_result_line(f"   交易数量: {hands} 手 ({shares:,} 股)")
            self.add_result_line(f"   预估税费: {total_tax:.2f} 元")
            self.add_result_line(f"   目标盈利: {profit_target:.2f} 元", pady=8)
            
            self.add_result_line("关键指标", 11, True, pady=5)
            self.add_result_line(f"   {action_desc}:")
            self.add_result_line(f"   • 价差要求: {diff_needed:.4f} 元")
            self.add_result_line(f"   • 涨跌幅: {percent_needed:.2f}%", pady=8)
            
            self.add_result_line("目标价格", 11, True, pady=5)
            self.add_result_line(f"   {target_price:.4f} 元", pady=8)
            
            # 添加成功提示
            if percent_needed < 1:
                self.add_result_line("策略可行！涨跌幅较小，容易实现", color="#10b981", pady=5)
            elif percent_needed < 3:
                self.add_result_line("需要关注！涨跌幅适中，注意市场波动", color="#f59e0b")
            else:
                self.add_result_line("难度较大！涨跌幅较高，建议谨慎操作", color="#ef4444")
            
            # 更新Canvas滚动区域，确保滚动生效
            self.result_canvas.update_idletasks()
            self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))
            
        except Exception as e:
            # 在终端输出详细错误信息
            print("=== 计算错误详情 ===")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}")
            print("=== 堆栈跟踪 ===")
            traceback.print_exc()
            print("==================")
            
            messagebox.showerror("计算错误", f"计算过程中出现错误:\n{str(e)}\n\n请检查输入数据，详细错误信息已输出到终端")

if __name__ == "__main__":
    root = tk.Tk()
    app = TCalculator(root)
    root.mainloop()