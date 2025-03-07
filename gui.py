import tkinter as tk
import sys
import os
from downloader import MusicDownloader as MD

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
        self.window.iconbitmap(self.get_path_icon('assets/logo.ico'))
        self.window.config(bg='sky blue')

    def destroy_element(self,element:tk):
        element.destroy()

        # def show_popup_notification(self, message: str, type_: str):
        #     frame = tk.Frame(self.window, bg='lightgray')
        #     frame.configure(width=250, height=150)  # Ajustar tamaño del frame
        #     label = tk.Label(frame, text=message, bg='lightgray')
        #     label.pack(pady=10)  # Añadir algo de espacio para que no quede pegado al borde
        #     button = tk.Button(frame, width=15, height=2, bg='blue', text='Aceptar',
        #                        command=lambda: self.destroy_element(frame))  # Botón más pequeño
        #     button.pack(pady=10)  # Añadir espacio al botón
        #
        #     frame.pack_propagate(False)
        #     frame.pack()

    def show_popup_notification(self, message:str,type_:str,callback=None):

        popup = tk.Toplevel(self.window)
        popup.config(bg='azure2')
        if type_ == 'Error':
            popup.title("¡Error!")
            icon_path = self.get_path_icon('assets/error.ico')
        elif type_ == 'Accept':
            popup.title("¡Éxito!")
            icon_path = self.get_path_icon('assets/accept.ico')
        else:
            popup.title("Notificación")
            icon_path = self.get_path_icon('assets/notification.ico')

        popup.geometry('300x180')
        popup.iconbitmap(icon_path)

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        popup_width = 250
        popup_height = 150

        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 4) - (popup_height // 2)
        popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

        label = tk.Label(popup, text=message, bg=popup['bg'], wraplength=popup_width-20, justify="center")
        label.pack(pady=10,padx=10)

        background='gray'
        match type_:
            case 'Error':
                background='firebrick1'
            case 'Accept':
                background='chartreuse3'
            case 'Notification':
                background='SteelBlue1'

        def on_close():
            popup.destroy()
            if callback:
                callback()

        button = tk.Button(popup, width=15, height=2, bg=background, text='Aceptar', command=on_close)
        button.pack(pady=10)

        # popup.pack_propagate(False)

    def verify_input_name_directory(self,input_):
        value=input_.get()

        if value == "":
            self.show_popup_notification('Debes de buscar algo','Error')

        else:
            self.show_popup_notification('Creando, espera...', 'Accept')



    def input_name_directory(self):

        popup = tk.Toplevel(self.window)
        popup.config(bg='azure2')

        icon_path = self.get_path_icon('assets/notification.ico')

        popup.geometry('300x180')
        popup.iconbitmap(icon_path)

        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        popup_width = 250
        popup_height = 150

        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 4) - (popup_height // 2)
        popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

        label = tk.Label(popup, text='Ingrese el nombre de la carpeta', bg=popup['bg'], wraplength=popup_width - 20, justify="center")
        label.pack(pady=10, padx=10)

        width_input = int(int(popup_width / 10) / 2)
        input_ = tk.Entry(popup)
        input_.configure(width=width_input)
        input_.pack()
        button = tk.Button(self.window, text='Crear', command=lambda: self.verify_input_name_directory(input_))
        button.pack(pady=10)


    def choose_election(self,message):
        popup = tk.Toplevel(self.window)
        popup.config(bg='azure2')
        icon_path = self.get_path_icon('assets/notification.ico')
        popup.geometry('300x180')
        popup.iconbitmap(icon_path)
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        popup_width = 250
        popup_height = 150
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 4) - (popup_height // 2)
        popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

        label = tk.Label(popup, text='Deseas crear una nueva carpeta? Nota: Si colocas "No" se hara uso de la carpeta por defecto', bg=popup['bg'], wraplength=popup_width - 20, justify="center")
        label.pack(pady=10, padx=10)

        def click_option(value):
            if value == 'Ok':
                popup.destroy()
                return True
            popup.destroy()
            return False

        button = tk.Button(self.window, text='Si', command=lambda: click_option('Ok'))
        button.pack(pady=10)

        button = tk.Button(popup, width=15, height=2, bg='chartreuse3', text='No', command=lambda: click_option('No'))
        button.pack(pady=10)

    def verify_input(self,input_):
        value=input_.get()

        if value == "":
            self.show_popup_notification('Debes de buscar algo','Error')
        elif not 'https://' in value:
            self.show_popup_notification('Debe ser una URL','Error')
        elif not 'https://www.youtube.com/' in value:
            self.show_popup_notification('Debe ser una url de Youtube', 'Error')
        else:
            # self.show_popup_notification('Buscando, espera', 'Accept')
            downloader = MD()
            downloader.run(input_.get().strip(), self)



    def run(self):

        label=tk.Label(self.window)
        label.configure(text='Ingrese la URL: ',bg='sky blue',fg='black')
        label.pack(pady=10)

        width_input = int(int(self.width_screen / 10)/2)
        input_=tk.Entry(self.window)
        input_.configure(width=width_input)
        input_.pack()
        button=tk.Button(self.window,text='Buscar',command=lambda: self.verify_input(input_))
        button.pack(pady=10)



        self.window.mainloop()



if __name__ == '__main__':
    window=Main_window()
    window.configure_window()
    window.run()
