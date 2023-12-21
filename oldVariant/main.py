import tkinter as tk
from tkinter import filedialog, messagebox
from app.generators import generate_keys
from app.signeter import improved_sign_file, improved_verify_signature
import json
import os

# Глобальные переменные
signature = None
keys = None  # Содержит публичный и приватный ключи, множитель и модуль

# Функции для графического интерфейса
def create_signature_ui():
    global keys
    public_key, private_key, multiplier, modulus = generate_keys()
    keys = {'public_key': public_key, 'private_key': private_key, 'multiplier': multiplier, 'modulus': modulus}
    messagebox.showinfo("Keys Generated", "Public and private keys have been generated.")

def save_keys_ui():
    if keys:
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(keys, file)
            messagebox.showinfo("Keys Saved", "Keys have been saved to file.")
    else:
        messagebox.showwarning("No Keys", "No keys to save. Please generate keys first.")

def load_keys_ui():
    global keys
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            keys = json.load(file)
        messagebox.showinfo("Keys Loaded", "Keys have been loaded.")

def sign_file_ui():
    global signature
    if not keys or 'private_key' not in keys:
        messagebox.showwarning("No Keys", "No private key available. Please load keys first.")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            file_data = file.read()
        signature = improved_sign_file(file_data, keys['private_key'], keys['modulus'], keys['multiplier'])

        # Сохраняем подпись в той же директории, что и файл
        signature_file_path = file_path + ".signature"
        with open(signature_file_path, 'w') as file:
            json.dump(signature, file)

        messagebox.showinfo("File Signed", f"File has been signed and signature saved to {signature_file_path}")


def verify_signature_ui():
    if not keys or 'public_key' not in keys or 'modulus' not in keys:
        messagebox.showwarning("No Keys", "No keys available. Please load keys first.")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        signature_file_path = file_path + ".signature"
        if os.path.exists(signature_file_path):
            with open(file_path, 'r') as file:
                file_data = file.read()
            with open(signature_file_path, 'r') as file:
                signature = json.load(file)

            is_valid = improved_verify_signature(file_data, signature, keys['public_key'], keys['modulus'])
            messagebox.showinfo("Signature Verification", f"Signature is {'valid' if is_valid else 'invalid'}.")
        else:
            messagebox.showwarning("Signature File Not Found", "The signature file was not found.")

# Создание графического интерфейса

root = tk.Tk()
root.title("Digital Signature Application")

create_sig_button = tk.Button(root, text="Create Keys", command=create_signature_ui)
save_keys_button = tk.Button(root, text="Save Keys", command=save_keys_ui)
load_keys_button = tk.Button(root, text="Load Keys", command=load_keys_ui)
sign_file_button = tk.Button(root, text="Sign File", command=sign_file_ui)
verify_sig_button = tk.Button(root, text="Verify Signature", command=verify_signature_ui)

create_sig_button.pack(fill=tk.X, padx=50, pady=10)
save_keys_button.pack(fill=tk.X, padx=50, pady=10)
load_keys_button.pack(fill=tk.X, padx=50, pady=10)
sign_file_button.pack(fill=tk.X, padx=50, pady=10)
verify_sig_button.pack(fill=tk.X, padx=50, pady=10)

root.mainloop()