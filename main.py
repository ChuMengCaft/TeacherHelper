import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TeacherHelper")
        self.root.geometry("600x500")

        self.names_file_path = None
        self.folder_path = None
        self.skip_animation = tk.BooleanVar()
        self.font_size = tk.IntVar(value=18)
        self.pending_students = None
        self.check_round = 1

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.menu_bar.add_command(label="随机点名", command=self.random_name_ui)
        self.menu_bar.add_command(label="作业检查", command=self.homework_check_ui)
        self.menu_bar.add_command(label="设置", command=self.settings_ui)
        self.menu_bar.add_command(label="关于", command=self.about_ui)
        self.menu_bar.add_command(label="MySQL",command=self.mysql_ui)

        self.display_area = tk.Label(root, text="Welcome to use\n请在菜单栏选择需要的功能",
                                     font=("Arial", self.font_size.get()))
        self.display_area.pack(pady=20)
        self.display_area.pack_propagate(False)

        self.current_buttons = []
        self.current_widgets = [self.display_area]

    def clear_widgets(self):
        for widget in self.current_widgets:
            widget.pack_forget()
        self.current_widgets.clear()

    def random_name_ui(self):
        self.clear_widgets()

        if self.names_file_path is None:
            self.display_area.config(text="未定义学生名字文件路径\n\n请在设置中指定names.txt文件")
            self.display_area.pack(pady=20)
            return

        self.display_area.config(text="请选择随机点名")
        self.display_area.pack(pady=20)
        self.random_name_button = tk.Button(self.root, text="开始点名", font=("Arial", self.font_size.get()),
                                            command=self.start_random_name)
        self.random_name_button.pack(pady=10)
        self.current_widgets.append(self.random_name_button)

    def start_random_name(self):
        with open(self.names_file_path, 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f.readlines()]

        if self.skip_animation.get():
            chosen_name = random.choice(names)
            self.display_area.config(text=f"随机点到：{chosen_name}")
        else:
            self.display_area.config(text="正在点名...")
            self.animate_random_name(names)

    def animate_random_name(self, names):
        for _ in range(50):
            chosen_name = random.choice(names)
            self.display_area.config(text=chosen_name)
            self.root.update_idletasks()
            self.root.after(50)
        chosen_name = random.choice(names)
        self.display_area.config(text=f"最终点名：{chosen_name}")

    def homework_check_ui(self):
        self.clear_widgets()

        self.display_area.config(text="请选择作业文件夹\n\n最好每个人单独提交\n不要出现在同一个文件名中出现2个人名")
        self.display_area.pack(pady=20)

        self.folder_path_input = tk.Entry(self.root, font=("Arial", self.font_size.get()), width=40)
        self.folder_path_input.pack(pady=10)
        if self.folder_path:
            self.folder_path_input.insert(0, self.folder_path)
        self.current_widgets.append(self.folder_path_input)

        self.select_folder_button = tk.Button(self.root, text="选择文件夹", font=("Arial", self.font_size.get()),
                                              command=self.select_folder)
        self.select_folder_button.pack(pady=10)
        self.current_widgets.append(self.select_folder_button)

        self.start_checking_button = tk.Button(self.root, text="开始检查", font=("Arial", self.font_size.get()),
                                               command=self.check_homework)
        self.start_checking_button.pack(pady=10)
        self.current_widgets.append(self.start_checking_button)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_path_input.delete(0, tk.END)
            self.folder_path_input.insert(0, folder_path)

    def check_homework(self):
        if not self.folder_path:
            self.display_area.config(text="请先选择作业文件夹\n最好每个人单独提交，不要出现在同一个文件名中出现2个人名")
            return

        if self.names_file_path is None:
            self.display_area.config(text="未定义学生名字文件路径")
            return

        with open(self.names_file_path, 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f.readlines()]

        self.display_area.config(text="检查中，请稍后...")

        self.pending_students = set(names)

        for root_dir, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root_dir, file)

                for name in names:
                    if name in file_path:
                        self.pending_students.discard(name)
                        break

        self.auto_check_rounds()

    def auto_check_rounds(self):
        if self.check_round < 3 and self.pending_students:
            self.check_round += 1
            self.root.after(1000, self.auto_check_rounds)
        elif self.check_round == 3:
            if self.pending_students:
                self.display_area.config(text="未交作业的学生：\n" + "\n".join(self.pending_students))
            else:
                self.display_area.config(text="所有学生的作业都已经提交。\n")

    def settings_ui(self):
        self.clear_widgets()

        self.display_area.config(text="设置学生名字文件路径")
        self.display_area.pack(pady=20)

        self.names_file_input = tk.Entry(self.root, font=("Arial", self.font_size.get()), width=40)
        self.names_file_input.pack(pady=10)
        if self.names_file_path:
            self.names_file_input.insert(0, self.names_file_path)
        self.current_widgets.append(self.names_file_input)

        self.set_names_file_button = tk.Button(self.root, text="指定names.txt路径",
                                               font=("Arial", self.font_size.get()), command=self.set_names_file)
        self.set_names_file_button.pack(pady=10)
        self.current_widgets.append(self.set_names_file_button)

        self.skip_animation_checkbox = tk.Checkbutton(self.root, text="跳过点名动画", variable=self.skip_animation,
                                                      font=("Arial", 12))
        self.skip_animation_checkbox.pack(pady=10)
        self.current_widgets.append(self.skip_animation_checkbox)

        self.font_size_label = tk.Label(self.root, text="字体大小", font=("Arial", 12))
        self.font_size_label.pack(pady=5)
        self.font_size_scale = tk.Scale(self.root, from_=1, to=100, orient="horizontal", variable=self.font_size,
                                        font=("Arial", 10), command=self.adjust_font_size)
        self.font_size_scale.pack(pady=10)
        self.current_widgets.append(self.font_size_label)
        self.current_widgets.append(self.font_size_scale)

    def adjust_font_size(self, event=None):
        self.display_area.config(font=("Arial", self.font_size.get()))

    def set_names_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.names_file_path = file_path
            self.names_file_input.delete(0, tk.END)
            self.names_file_input.insert(0, file_path)

    def about_ui(self):
        self.clear_widgets()

        self.display_area.config(text="TeacherHelper\n\nDev:ChuMengCaft\n\nPython比C语言简单多了！！！！！！")
        self.display_area.pack(pady=20)
        self.current_widgets.append(self.display_area)

    def mysql_ui(self):
        self.clear_widgets()

        self.display_area.config(text="MySQL(开发中)\nIP:\nPort:\nAccount:\nPassword:\n")
        self.display_area.pack(pady=20)
        self.current_widgets.append((self.display_area))
        self.mysql_submit = tk.Button(self.root,text="尝试连接",command="#")
        self.mysql_submit.pack(pady=10)
        self.mysql_submit.append(self.mysql_submit)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
