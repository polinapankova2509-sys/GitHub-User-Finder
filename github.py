import tkinter as tk
from tkinter import messagebox
import requests
import json

# Путь к файлу избранных пользователей
FAVORITES_FILE = 'favorites.json'

def load_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)

def search_user():
    username = entry.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
        return

    try:
        response = requests.get(f'https://api.github.com/users/{username}')
        response.raise_for_status()
        user_data = response.json()
        listbox.insert(tk.END, f"{user_data['login']} - {user_data['html_url']}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Пользователь не найден или ошибка сети: {e}")

def add_to_favorites():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Ошибка", "Выберите пользователя из списка")
        return
    user_info = listbox.get(selected[0])
    username = user_info.split(' - ')[0]
    favorites = load_favorites()
    if username not in favorites:
        favorites.append(username)
        save_favorites(favorites)
        messagebox.showinfo("Успех", f"{username} добавлен в избранное")

# Основное окно
root = tk.Tk()
root.title("GitHub User Finder")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

search_btn = tk.Button(root, text="Поиск", command=search_user)
search_btn.pack(pady=5)

listbox = tk.Listbox(root, width=60, height=15)
listbox.pack(pady=10)

fav_btn = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
fav_btn.pack(pady=5)

root.mainloop()