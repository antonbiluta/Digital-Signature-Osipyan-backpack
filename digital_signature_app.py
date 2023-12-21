import tkinter as tk
from tkinter import messagebox, filedialog
from user_controller import UserController
from signeter import improved_sign_file, improved_verify_signature
from generators import generate_keys_json
import json, os


class DigitalSignatureApp:
    def __init__(self, root):
        self.password_entry = None
        self.username_entry = None
        self.signature_data = None
        self.root = root
        self.root.title("Digital Signature Application")
        self.user_controller = UserController("users.db")
        self.current_user = None
        self.initialize_login_screen()

    def initialize_login_screen(self):
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Элементы для входа
        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")
        login_button = tk.Button(self.root, text="Войти", command=self.login)
        register_button = tk.Button(self.root, text="Регистрация", command=self.register)

        # Расположение элементов
        self.username_entry.pack(padx=10, pady=10)
        self.password_entry.pack(padx=10, pady=10)
        login_button.pack(padx=10, pady=5)
        register_button.pack(padx=10, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_controller.login_user(username, password):
            self.current_user = username
            self.signature_data = self.user_controller.get_signature_data(username)
            self.initialize_main_screen()
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.user_controller.register_user(username, password)
        messagebox.showinfo("Регистрация", message)
        if success:
            self.login()

    def initialize_main_screen(self):
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Элементы главного экрана приложения
        sign_file_button = tk.Button(self.root, text="Подписать файл", command=self.sign_file)
        verify_file_button = tk.Button(self.root, text="Проверить подпись файла", command=self.verify_signature)
        logout_button = tk.Button(self.root, text="Выйти из аккаунта", command=self.logout)
        recreate_signature_button = tk.Button(self.root, text="Пересоздать подпись", command=self.recreate_signature)

        # Расположение элементов
        sign_file_button.pack(padx=10, pady=5)
        verify_file_button.pack(padx=10, pady=5)
        logout_button.pack(padx=10, pady=5)
        recreate_signature_button.pack(padx=10, pady=5)

    def sign_file(self):
        if not self.current_user or 'private_key' not in self.signature_data or 'modulus' not in self.signature_data or 'multiplier' not in self.signature_data:
            messagebox.showwarning("Ошибка", "Необходимо войти в систему и иметь цифровую подпись")
            return

        file_path = filedialog.askopenfilename(title="Выберите файл для подписи")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    file_data = file.read()
                signature = improved_sign_file(
                    file_data,
                    self.signature_data['private_key'],
                    self.signature_data['modulus'],
                    self.signature_data['multiplier']
                )

                # Сохраняем подпись в файл рядом с исходным файлом
                signature_file_path = file_path + ".signature"
                with open(signature_file_path, 'w') as sig_file:
                    json.dump(signature, sig_file)

                messagebox.showinfo(
                    "Подпись файла",
                    f"Файл '{file_path}' успешно подписан. Подпись сохранена в '{signature_file_path}'"
                )
            except Exception as e:
                messagebox.showerror(
                    "Ошибка",
                    f"Произошла ошибка при подписи файла: {e}"
                )

    def verify_signature(self):
        if not self.current_user or 'public_key' not in self.signature_data or 'modulus' not in self.signature_data:
            messagebox.showwarning("Ошибка", "Необходимо войти в систему и иметь цифровую подпись")
            return

        file_path = filedialog.askopenfilename(title="Выберите файл для проверки подписи")
        signature_file_path = file_path + ".signature"

        if file_path and os.path.exists(signature_file_path):
            try:
                with open(file_path, 'r') as file:
                    file_data = file.read()
                with open(signature_file_path, 'r') as sig_file:
                    signature = json.load(sig_file)

                is_valid = improved_verify_signature(
                    file_data,
                    signature,
                    self.signature_data['public_key'],
                    self.signature_data['modulus']
                )
                messagebox.showinfo("Проверка подписи", "Подпись файла " + ("действительна" if is_valid else "недействительна"))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при проверке подписи: {e}")
        else:
            messagebox.showwarning("Файл не найден", "Файл подписи не найден. Убедитесь, что файл подписан и попробуйте снова.")


    def logout(self):
        self.current_user = None
        self.initialize_login_screen()

    def recreate_signature(self):
        if not self.current_user:
            messagebox.showwarning("Ошибка", "Необходимо войти в систему для пересоздания подписи")
            return

            # Генерация новой пары ключей
        new_signature_keys = generate_keys_json()

        # Сохранение новых ключей в базе данных для текущего пользователя
        success, message = self.user_controller.save_signature(self.current_user, new_signature_keys)
        if success:
            self.signature_data = self.user_controller.get_signature_data(self.current_user)  # Обновление локальных данных подписи
            messagebox.showinfo("Пересоздание подписи", "Новая цифровая подпись успешно создана и сохранена")
        else:
            messagebox.showerror("Ошибка", message)