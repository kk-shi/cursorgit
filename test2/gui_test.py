import tkinter as tk
from selenium import webdriver
from tkinter import messagebox

# URLを開く関数
def open_browser():
    try:
        # Chromeオプション設定
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")

        # Chromeブラウザを起動
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")  # 開きたいURL

        # メッセージボックスで通知
        messagebox.showinfo("ブラウザ起動", "ブラウザが正常に起動しました！")
    except Exception as e:
        messagebox.showerror("エラー", f"ブラウザ起動中にエラーが発生しました:\n{str(e)}")

# GUIを作成
def create_notification():
    # メインウィンドウを作成
    root = tk.Tk()
    root.title("通知アプリ")
    root.geometry("300x150")  # ウィンドウサイズ

    # ラベルを追加
    label = tk.Label(root, text="新しい通知があります！", font=("Arial", 14))
    label.pack(pady=10)

    # ボタンを追加
    button = tk.Button(root, text="ブラウザを開く", command=open_browser, bg="blue", fg="white")
    button.pack(pady=10)

    # GUIループを開始
    root.mainloop()

# 通知ウィンドウを表示
create_notification()