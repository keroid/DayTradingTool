import tkinter as tk
from tkinter import ttk, messagebox

class TCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("T+0 盈亏计算器")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # 设置样式
        style = ttk.Style()
        style.configure("Title.TLabel", font=("微软雅黑", 12, "bold"))
        style.configure("Result.TLabel", font=("微软雅黑", 11), foreground="#2c3e50")
        style.configure("Highlight.TLabel", font=("微软雅黑", 11, "bold"), foreground="#27ae60")
        
        # 标题
        title_label = ttk.Label(root, text="T+0 交易盈亏计算器", style="Title.TLabel")
        title_label.pack(pady=15)
        
        # 主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # 股价输入
        ttk.Label(input_frame, text="当前股价 (元):").grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.price_entry = ttk.Entry(input_frame, width=20, font=("微软雅黑", 10))
        self.price_entry.grid(row=0, column=1, pady=8, padx=5)
        self.price_entry.insert(0, "50.00")
        
        # 手数输入
        ttk.Label(input_frame, text="交易手数:").grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.hands_entry = ttk.Entry(input_frame, width=20, font=("微软雅黑", 10))
        self.hands_entry.grid(row=1, column=1, pady=8, padx=5)
        self.hands_entry.insert(0, "10")
        ttk.Label(input_frame, text="(1手=100股)", foreground="#7f8c8d").grid(row=1, column=2, padx=5)
        
        # 税费输入
        ttk.Label(input_frame, text="总税费 (元):").grid(row=2, column=0, sticky=tk.W, pady=8, padx=5)
        self.tax_entry = ttk.Entry(input_frame, width=20, font=("微软雅黑", 10))
        self.tax_entry.grid(row=2, column=1, pady=8, padx=5)
        self.tax_entry.insert(0, "10.00")
        ttk.Label(input_frame, text="(买卖合计)", foreground="#7f8c8d").grid(row=2, column=2, padx=5)
        
        # 目标盈利输入
        ttk.Label(input_frame, text="目标盈利 (元):").grid(row=3, column=0, sticky=tk.W, pady=8, padx=5)
        self.profit_entry = ttk.Entry(input_frame, width=20, font=("微软雅黑", 10))
        self.profit_entry.grid(row=3, column=1, pady=8, padx=5)
        self.profit_entry.insert(0, "0.00")
        ttk.Label(input_frame, text="(0为保本)", foreground="#7f8c8d").grid(row=3, column=2, padx=5)
        
        # T类型选择
        ttk.Label(input_frame, text="T类型:").grid(row=4, column=0, sticky=tk.W, pady=8, padx=5)
        self.t_type = tk.StringVar(value="正T")
        ttk.Radiobutton(input_frame, text="正T (先买后卖)", variable=self.t_type, value="正T").grid(row=4, column=1, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="反T (先卖后买)", variable=self.t_type, value="反T").grid(row=4, column=2, sticky=tk.W)
        
        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # 计算按钮
        calc_btn = ttk.Button(main_frame, text="计算", command=self.calculate, width=20)
        calc_btn.pack(pady=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, width=50, font=("微软雅黑", 10), 
                                    wrap=tk.WORD, relief=tk.FLAT, borderwidth=1)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        # 初始化显示
        self.result_text.insert(tk.END, "输入参数后点击计算按钮查看结果\n\n")
        self.result_text.insert(tk.END, "正T：低买高卖，先买入后卖出\n")
        self.result_text.insert(tk.END, "反T：高卖低买，先卖出后买入")
        self.result_text.config(state=tk.DISABLED)
    
    def calculate(self):
        try:
            # 获取输入值
            price = float(self.price_entry.get())
            hands = int(self.hands_entry.get())
            total_tax = float(self.tax_entry.get())
            profit_target = float(self.profit_entry.get())
            t_type = self.t_type.get()
            
            # 验证输入
            if price <= 0 or hands <= 0 or total_tax < 0 or profit_target < 0:
                messagebox.showerror("错误", "请输入有效的正数")
                return
            
            # 计算总股数
            shares = hands * 100
            
            # 计算需要变动的价格
            if t_type == "正T":
                # 正T：低价买入，高价卖出
                # 卖出价需要比买入价高多少
                diff_needed = (2 * total_tax + profit_target) / shares
                action_desc = "卖出价需比买入价高"
                target_desc = "目标卖出价"
            else:
                # 反T：高价卖出，低价买入
                # 买入价需要比卖出价低多少
                diff_needed = (2 * total_tax + profit_target) / shares
                action_desc = "买入价需比卖出价低"
                target_desc = "目标买入价"
            
            # 计算百分比
            percent_needed = (diff_needed / price) * 100
            
            # 计算目标价格
            if t_type == "正T":
                target_price = price + diff_needed
            else:
                target_price = price - diff_needed
            
            # 准备结果文本
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            
            result = f"【{t_type} 计算结果】\n"
            result += "=" * 40 + "\n\n"
            result += f"当前股价: {price:.2f} 元\n"
            result += f"交易手数: {hands} 手 ({shares} 股)\n"
            result += f"总税费: {total_tax:.2f} 元\n"
            result += f"目标盈利: {profit_target:.2f} 元\n\n"
            
            result += f"✅ {action_desc}\n"
            result += f"   {diff_needed:.4f} 元\n"
            result += f"   ({percent_needed:.2f}%)\n\n"
            
            result += f"🎯 {target_desc}\n"
            result += f"   {target_price:.4f} 元\n\n"
            
            if profit_target > 0:
                result += f"包含目标盈利 {profit_target:.2f} 元\n"
            else:
                result += "（保本交易，不含盈利）\n"
            
            self.result_text.insert(tk.END, result)
            self.result_text.config(state=tk.DISABLED)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"计算出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TCalculator(root)
    root.mainloop()