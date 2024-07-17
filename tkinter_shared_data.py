import tkinter as tk
from tkinter import messagebox
import json
import os

"""
元件由大到小是 tk.Tk 到 tk.frame 到 tk. Label/ button

tk.Tk: 根窗口（Root Window）
    这是整个 Tkinter 应用程序的主窗口，所有其他组件都在这个窗口之内。

tk.Frame: 框架（Frame）
这是一个容器组件，可以包含其他组件（如按钮、标签、输入框等）。框架用于组织和布局子组件。
框架可以嵌套在根窗口或其他框架中。

其他组件: 如 tk.Label、tk.Button、tk.Entry 等
这些是实际的控件或小部件，用于显示信息或与用户交互。
这些组件通常放置在框架内，但也可以直接放置在根窗口中。
"""

class SharedDataApp(tk.Tk):
    """
    Main Class, 在 Page a & b 切換，然後儲存參數到 data.json 中, 實現參數共享
    """
    def __init__(self):
        super().__init__()
        self.title("Shared Data App")
        self.geometry("400x300")
        
        self.shared_data = self.load_data()
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (PageA, PageB):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            """
            row=0:
                将 frame 放置在网格的第 0 行。行和列的编号从 0 开始。

            column=0:
                将 frame 放置在网格的第 0 列。
                sticky="nsew":

            sticky :参数指定组件在网格单元格中的对齐方式。
            nsew: 是北、南、东、西四个方向的缩写。这意味着组件将拉伸并填满网格单元格的整个区域。
            具体来说：
            n 表示北（上）
            s 表示南（下）
            e 表示东（右）
            w 表示西（左）
            结合在一起，nsew 表示组件将扩展以填充单元格的整个区域，而不仅仅是放置在单元格的中央。
            """
        
        self.show_frame("PageA")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    
    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                return json.load(file)
        return {"data_a": "", "data_b": ""}
    
    def save_data(self):
        with open("data.json", "w") as file:
            json.dump(self.shared_data, file)
    
    def on_closing(self):
        self.save_data()
        self.destroy()

class PageA(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label_a = tk.Label(self, text="Page A - Save Data A")
        self.label_a.pack(pady=10, padx=10)
        
        self.entry_a = tk.Entry(self)
        self.entry_a.pack()
        self.entry_a.insert(0, self.controller.shared_data["data_a"])
        
        self.label_b = tk.Label(self, text="Page A - Save Data B")
        self.label_b.pack(pady=10, padx=10)
        
        self.entry_b = tk.Entry(self)
        self.entry_b.pack()
        self.entry_b.insert(0, self.controller.shared_data["data_b"])
        
        self.save_button = tk.Button(self, text="Save Data",
                                     command=self.save_data)
        self.save_button.pack()
        
        self.switch_button = tk.Button(self, text="Go to Page B",
                                       command=lambda: controller.show_frame("PageB"))
        self.switch_button.pack()
    
    def save_data(self):
        self.controller.shared_data["data_a"] = self.entry_a.get()
        self.controller.shared_data["data_b"] = self.entry_b.get()
        self.controller.save_data()
        messagebox.showinfo("Notification", "Data saved successfully!")

class PageB(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label_a = tk.Label(self, text="Page B - View Data A")
        self.label_a.pack(pady=10, padx=10)
        
        self.data_label_a = tk.Label(self, text=self.controller.shared_data["data_a"])
        self.data_label_a.pack(pady=10, padx=10)
        
        self.label_b = tk.Label(self, text="Page B - View Data B")
        self.label_b.pack(pady=10, padx=10)
        
        self.data_label_b = tk.Label(self, text=self.controller.shared_data["data_b"])
        self.data_label_b.pack(pady=10, padx=10)
        
        self.switch_button = tk.Button(self, text="Go to Page A",
                                       command=lambda: controller.show_frame("PageA"))
        self.switch_button.pack()
    
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        # 更新显示数据
        self.data_label_a.config(text=self.controller.shared_data["data_a"])
        self.data_label_b.config(text=self.controller.shared_data["data_b"])

if __name__ == "__main__":
    app = SharedDataApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
