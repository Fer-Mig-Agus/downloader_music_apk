import tkinter as tk
import sys
import os


class Main_window:

    def __init__(self):
        self.window = tk.Tk()
        root = tk.Tk()
        self.width_screen = int(int(root.winfo_screenwidth()) / 2) - 75
        self.heigth_screen = int(int(root.winfo_screenheight()) / 4)
        root.destroy()

    def get_path_icon(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    def configure_window(self):

        self.window.geometry(f'400x500+{self.width_screen}+{self.heigth_screen}')
        self.window.configure(pady=20)
        self.window.resizable(False, False)
        self.window.title('Downloader music - MF Dev')
        self.window.iconbitmap(self.get_path_icon('logo.ico'))
        self.window.config(bg='sky blue')


    def run(self):
        # with_input=int(self.width_screen-(self.width_screen/2))
        # print(with_input)

        label=tk.Label(self.window)
        label.configure(text='Ingrese la URL: ',bg='sky blue',fg='black')
        label.pack(pady=10)

        width_input = int(int(self.width_screen / 10)/2)
        print(width_input)
        input=tk.Entry(self.window)
        input.configure(width=width_input)
        input.pack()


        self.window.mainloop()






























# Main window




if __name__ == '__main__':
    window=Main_window()
    window.configure_window()
    window.run()
