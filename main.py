import tkinter as tk
import sys
import os


class Main_window:

    def __init__(self):
        self.window = tk.Tk()

    def get_path_icon(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    def configure_window(self):
        root = tk.Tk()
        width_screen = int(int(root.winfo_screenwidth()) / 2) - 75
        heigth_screen = int(int(root.winfo_screenheight()) / 4)
        root.destroy()

        self.window.geometry(f'400x500+{width_screen}+{heigth_screen}')
        self.window.resizable(False, False)
        self.window.title('Downloader music - MF Dev')
        self.window.iconbitmap(self.get_path_icon('logo.ico'))
        self.window.config(bg='sky blue')


    def run(self):
        self.window.mainloop()






























# Main window




if __name__ == '__main__':
    window=Main_window()
    window.configure_window()
    window.run()
