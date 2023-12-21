
import tkinter as tk
from digital_signature_app import DigitalSignatureApp


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalSignatureApp(root)
    root.mainloop()