import tkinter as tk
from threading import Thread
import time

def test_example_function():
    assert True

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("400x250")

        # 确保窗口始终在最上层
        self.root.attributes('-topmost', True)

        # 绑定Tab键事件
        self.root.bind('<Tab>', self.toggle_border)

        self.label = tk.Label(root, text="Enter time:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.frame = tk.Frame(root)
        self.frame.pack(pady=5)

        self.hours_entry = tk.Entry(self.frame, width=5, font=("Helvetica", 14))
        self.hours_entry.insert(0, "00")
        self.hours_entry.grid(row=0, column=0)
        self.hours_label = tk.Label(self.frame, text="hours", font=("Helvetica", 14))
        self.hours_label.grid(row=0, column=1)

        self.minutes_entry = tk.Entry(self.frame, width=5, font=("Helvetica", 14))
        self.minutes_entry.insert(0, "00")
        self.minutes_entry.grid(row=0, column=2)
        self.minutes_label = tk.Label(self.frame, text="minutes", font=("Helvetica", 14))
        self.minutes_label.grid(row=0, column=3)

        self.seconds_entry = tk.Entry(self.frame, width=5, font=("Helvetica", 14))
        self.seconds_entry.insert(0, "00")
        self.seconds_entry.grid(row=0, column=4)
        self.seconds_label = tk.Label(self.frame, text="seconds", font=("Helvetica", 14))
        self.seconds_label.grid(row=0, column=5)

        self.start_button = tk.Button(root, text="Start Countdown", command=self.start_countdown, font=("Helvetica", 14))
        self.start_button.pack(pady=10)

        self.time_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.time_label.pack(expand=True)

        self.button_frame = tk.Frame(root)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.toggle_pause, font=("Helvetica", 14), width=10)
        self.pause_button.grid(row=0, column=0, padx=5)
        self.pause_button.grid_remove()  # 初始隐藏

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset, font=("Helvetica", 14), width=10)
        self.reset_button.grid(row=0, column=1, padx=5)
        self.reset_button.grid_remove()  # 初始隐藏

        self.borderless = False

        self.running = False
        self.paused = False

        # 处理关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def countdown(self, total_seconds):
        while total_seconds >= 0 and self.running:
            if not self.paused:
                mins, secs = divmod(total_seconds, 60)
                hours, mins = divmod(mins, 60)
                time_format = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
                self.time_label.config(text=time_format)
                self.root.update()
                time.sleep(1)
                total_seconds -= 1
            else:
                time.sleep(0.1)
        if total_seconds < 0:
            self.time_label.config(text="Time's up!")

    def start_countdown(self):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            total_seconds = hours * 3600 + minutes * 60 + seconds
            self.running = True
            self.paused = False
            self.start_button.pack_forget()
            self.pause_button.grid()  # 显示暂停按钮
            self.reset_button.grid()  # 显示重置按钮
            Thread(target=self.countdown, args=(total_seconds,)).start()
            self.label.pack_forget()
            self.frame.pack_forget()
            self.button_frame.pack(pady=10)  # 显示按钮框架
        except ValueError:
            self.time_label.config(text="Invalid time format")

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.pause_button.config(text="Pause")
        else:
            self.paused = True
            self.pause_button.config(text="Resume")

    def reset(self):
        self.running = False
        self.paused = False
        self.time_label.config(text="")
        self.start_button.pack(pady=10)
        self.label.pack(pady=10)
        self.frame.pack(pady=5)
        self.pause_button.grid_remove()  # 隐藏暂停按钮
        self.reset_button.grid_remove()  # 隐藏重置按钮
        self.hours_entry.delete(0, tk.END)
        self.hours_entry.insert(0, "00")
        self.minutes_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "00")
        self.seconds_entry.delete(0, tk.END)
        self.seconds_entry.insert(0, "00")
        self.button_frame.pack_forget()  # 隐藏按钮框架

    def toggle_border(self, event=None):
        if self.borderless:
            self.root.overrideredirect(False)
        else:
            self.root.overrideredirect(True)
        self.borderless = not self.borderless

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
