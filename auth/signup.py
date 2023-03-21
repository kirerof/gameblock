import sqlite3
import tkinter as tk
from tkinter import messagebox
import bcrypt


root = tk.Tk()
root.title("Login")
root.geometry("1400x700")
root.configure(bg="#fff")
root.resizable(False, False)


def sign_up():
    username = login.get()
    psswrd = password.get()
    psswrd2 = password2.get()

    if username == "" or username == "Логин":
        tk.messagebox.showerror("Логин", "Введите логин")
    elif len(username) < 4:
        tk.messagebox.showerror("Слишком короткий логин", "Логин должен быть не короче 4 символов")
    elif len(psswrd) < 6:
        tk.messagebox.showerror("Слишком короткий пароль", "Пароль должен быть не короче 6 символов")
    elif psswrd == psswrd2:
        with sqlite3.connect("../db/database.db") as db:
            cursor = db.cursor()
            try:
                query = """INSERT INTO players (username, password) VALUES (?, ?)"""
                hash_password = bcrypt.hashpw(psswrd.encode(), bcrypt.gensalt())
                cursor.execute(query, (username, hash_password))
                db.commit()
                tk.messagebox.showinfo("Регистрация", "Регистрация прошла успешно")
            except sqlite3.IntegrityError:
                tk.messagebox.showerror("Имя занято", "Это имя уже занято")

    else:
        tk.messagebox.showerror("Ошибка", "Пароли должны совпадать")


def to_sign_in():
    root.destroy()


img = tk.PhotoImage(file="../static/signup.png")
tk.Label(root, image=img, bg="white").place(x=200, y=160)

frame = tk.Frame(root, width=380, height=350, bg="white")
frame.place(x=820, y=200)


heading = tk.Label(frame, text="Зарегестрироваться", fg="#57a1f8", bg="white",
                   font=("Microsoft YaHei UI Light", 23, "bold"))
heading.place(x=30, y=5)

######################################################################################


def on_enter(x):
    name = login.get()
    if name == "Логин":
        login.delete(0, "end")
    else:
        pass


def on_leave(x):
    name = login.get()
    if name == "":
        login.insert(0, "Логин")


login = tk.Entry(frame, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
login.place(x=70, y=80)
login.insert(0, "Логин")
login.bind("<FocusIn>", on_enter)
login.bind("<FocusOut>", on_leave)

tk.Frame(frame, width=250, height=2, bg="black").place(x=60, y=105)

######################################################################################


def on_enter(x):
    name = password.get()
    if name == "Пароль":
        password.delete(0, "end")
        password.config(show="*")
    else:
        pass


def on_leave(x):
    name = password.get()
    if name == "":
        password.insert(0, "Пароль")
        password.config(show="")


password = tk.Entry(frame, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
password.place(x=70, y=150)
password.insert(0, "Пароль")
password.bind("<FocusIn>", on_enter)
password.bind("<FocusOut>", on_leave)

tk.Frame(frame, width=250, height=2, bg="black").place(x=60, y=175)

##################################################################


def on_enter(x):
    name = password2.get()
    if name == "Введите пароль еще раз":
        password2.delete(0, "end")
        password2.config(show="*")
    else:
        pass


def on_leave(x):
    name = password2.get()
    if name == "":
        password2.insert(0, "Введите пароль еще раз")
        password2.config(show="")


password2 = tk.Entry(frame, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
password2.place(x=70, y=210)
password2.insert(0, "Введите пароль еще раз")
password2.bind("<FocusIn>", on_enter)
password2.bind("<FocusOut>", on_leave)

tk.Frame(frame, width=250, height=2, bg="black").place(x=60, y=235)

####################################################################

tk.Button(frame, width=35, pady=7, text="Зарегистрироваться", bg="#57a1f8", fg="white", border=0, command=sign_up).place(x=60, y=260)
label = tk.Label(frame, text="У меня есть аккаунт", bg="white", fg="black", font=("Microsoft YaHei UI Light", 9))
label.place(x=80, y=305)

sign_in = tk.Button(frame, width=10, text="Войти", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=to_sign_in)
sign_in.place(x=220, y=305)

root.mainloop()
