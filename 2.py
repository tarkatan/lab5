import random
import tkinter as tk
from tkinter import messagebox

# Функція тесту простоти Міллера-Рабіна
def is_prime_miller_rabin(p, k=40):
    if p <= 1:
        return False
    if p <= 3:
        return True
    if p % 2 == 0:
        return False
    s, d = 0, p - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def check_composite(a):
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                return False
        return True

    for _ in range(k):
        a = random.randint(2, p - 2)
        if check_composite(a):
            return False
    return True

# Генерація великого простого числа
def generate_large_prime(bits):
    while True:
        num = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime_miller_rabin(num):
            return num

# Розширений алгоритм Евкліда
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

# Генерація RSA-ключів
def generate_rsa_keys(bits, user_e=None):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    if user_e is None:
        e = 65537
    else:
        e = user_e
    gcd, _, _ = extended_gcd(e, phi)
    while gcd != 1:
        e = random.randint(2, phi - 1)
        gcd, _, _ = extended_gcd(e, phi)

    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi

    return (e, n), (d, n)

# Шифрування повідомлення
def encrypt_rsa(public_key, message):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

# Розшифрування повідомлення
def decrypt_rsa(private_key, ciphertext):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

# Функція для форматування ключів
def format_key(key, width=80):
    key_str = str(key)
    return '\n'.join([key_str[i:i+width] for i in range(0, len(key_str), width)])

# Глобальні змінні
public_key = None
private_key = None

# GUI функції
def generate_keys():
    global public_key, private_key
    bits = int(key_size_var.get())
    public_key, private_key = generate_rsa_keys(bits)
    public_key_text.delete("1.0", tk.END)
    public_key_text.insert(tk.END, f"Відкритий ключ (e, n):\n{public_key[0]}\n{format_key(public_key[1])}")
    private_key_text.delete("1.0", tk.END)
    private_key_text.insert(tk.END, f"Закритий ключ (d, n):\n{private_key[0]}\n{format_key(private_key[1])}")
    messagebox.showinfo("Ключі згенеровано", "RSA ключі успішно згенеровані!")

def encrypt_message():
    if public_key is None:
        messagebox.showwarning("Помилка", "Спочатку згенеруйте ключі!")
        return
    message = message_entry.get()
    encrypted = encrypt_rsa(public_key, message)
    encrypted_text_var.set(','.join(map(str, encrypted)))
    messagebox.showinfo("Шифрування завершено", "Повідомлення успішно зашифроване!")

def decrypt_message():
    if private_key is None:
        messagebox.showwarning("Помилка", "Спочатку згенеруйте ключі!")
        return
    encrypted_text = encrypted_text_var.get()
    if not encrypted_text:
        messagebox.showwarning("Помилка", "Введіть зашифроване повідомлення!")
        return
    try:
        ciphertext = list(map(int, encrypted_text.split(',')))
        decrypted = decrypt_rsa(private_key, ciphertext)
        decrypted_text_var.set(decrypted)
        messagebox.showinfo("Розшифрування завершено", "Повідомлення успішно розшифроване!")
    except ValueError:
        messagebox.showerror("Помилка", "Неправильний формат зашифрованого повідомлення!")

# GUI
root = tk.Tk()
root.title("Навчальна RSA система")

# Вибір розміру ключа
tk.Label(root, text="Виберіть розмір ключа (в бітах):").grid(row=0, column=0, padx=10, pady=10)
key_size_var = tk.StringVar(value="1024")
tk.Entry(root, textvariable=key_size_var).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Згенерувати ключі", command=generate_keys).grid(row=0, column=2, padx=10, pady=10)

# Відображення ключів
tk.Label(root, text="Відкритий ключ:").grid(row=1, column=0, padx=10, pady=10)
public_key_text = tk.Text(root, height=8, width=80, wrap=tk.WORD)
public_key_text.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Закритий ключ:").grid(row=2, column=0, padx=10, pady=10)
private_key_text = tk.Text(root, height=8, width=80, wrap=tk.WORD)
private_key_text.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Шифрування
tk.Label(root, text="Введіть повідомлення для шифрування:").grid(row=3, column=0, padx=10, pady=10)
message_entry = tk.Entry(root, width=50)
message_entry.grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Зашифрувати", command=encrypt_message).grid(row=3, column=2, padx=10, pady=10)

# Зашифроване повідомлення
tk.Label(root, text="Введіть зашифроване повідомлення:").grid(row=4, column=0, padx=10, pady=10)
encrypted_text_var = tk.StringVar()
tk.Entry(root, textvariable=encrypted_text_var, width=50).grid(row=4, column=1, padx=10, pady=10)

# Розшифрування
tk.Button(root, text="Розшифрувати", command=decrypt_message).grid(row=5, column=2, padx=10, pady=10)
tk.Label(root, text="Розшифроване повідомлення:").grid(row=5, column=0, padx=10, pady=10)
decrypted_text_var = tk.StringVar()
tk.Entry(root, textvariable=decrypted_text_var, width=50).grid(row=5, column=1, padx=10, pady=10)

root.mainloop()
