print("Hello, World!")

import time
import random
import csv
import threading
import tkinter as tk
from tkinter import messagebox

from plyer import notification

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import pandas as pd
from selenium.webdriver.common.by import By


def scrape_website():

    # Seleniumのオプション設定
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # ヘッドレスモード（ブラウザを非表示にする）
    chrome_options.add_argument("--disable-gpu")  # GPUを無効化（Windowsの場合推奨）
    chrome_options.add_argument("--no-sandbox")  # サンドボックスを無効化（Linux環境用）
    chrome_options.add_argument("--disable-dev-shm-usage")  # 共有メモリの問題を回避
    chrome_options.add_argument("--disk-cache-dir=/tmp/cache")  # キャッシュディレクトリを指定
    chrome_options.add_argument("--disk-cache-size=4096")  # キャッシュサイズを指定
    
    chrome_options2 = ChromeOptions()
    
    
    # 不要なリソースを無効化

    # WebDriverのセットアップ
    
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.nikkei.com/news/category/")  # 対象のURLを指定

    # ページが完全にロードされるまで待つ
    random_sleep_time = round(random.uniform(2, 3), 3)
    time.sleep(random_sleep_time)

    # <ul class="newsFeed_list"> 内の <a> タグを取得:(By.CSS_SELECTOR, "ul.List a")のように書く★l.をわすれない
    links = driver.find_elements(By.CSS_SELECTOR, "div.container_c2kxg2n a")
    print(f"Proce_links: {links}")
    urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]
    urls = urls[:1]  # 最初の3件だけを抽出

    # 現在のウィンドウを記録

    original_window = driver.current_window_handle

    # 各リンクのhrefを取得して表示

    # CSVファイルの準備
    csv_file = "web_data.csv"  # 出力ファイル名
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # ヘッダーの書き込み
        writer.writerow(["URL", "Title"])
        
        # 各URLを順に処理してCSVに書き込む
        for url in urls:
            print(f"Processing: {url}")
            
            # URLを新しいタブで開く
            driver.execute_script("window.open(arguments[0]);", url)
            random_sleep_time = round(random.uniform(1, 3), 3)
            time.sleep(random_sleep_time)  # ページの読み込み待ち（必要に応じて調整）
            
            # 新しいタブに切り替える
            driver.switch_to.window(driver.window_handles[-1])
            
            # 現在のページのURLとタイトルを取得
            current_url = driver.current_url
            title = driver.title[:30]
            print(f"URL: {current_url}, Title: {title}")
            
            # データをCSVに書き込む
            writer.writerow([current_url, title])
            
            # タブを閉じる
            driver.close()
            
            # 元のタブに戻る
            random_sleep_time = round(random.uniform(0.5, 2), 3)

            driver.switch_to.window(driver.window_handles[0])

    import os
    print(f"現在の作業ディレクトリ: {os.getcwd()}")
        
    # 保存したCSVファイルを読み込み
    csv_file_1 = "web_data.csv"  # 保存したCSVファイル1
    csv_file_2 = "web_data_previous.csv"  # 比較するCSVファイル2    

    print(f"csv_file-Load")
    
    # 2つのCSVファイルをDataFrameとして読み込む
    df1 = pd.read_csv(csv_file_1, encoding='utf8')
    df2 = pd.read_csv(csv_file_2, encoding='utf8')  

    print(f"csv_file-Load2")

    # 特定の列（URL列）で比較
    diff_new = df1[~df1['URL'].isin(df2['URL'])]
    diff_old = df2[~df2['URL'].isin(df1['URL'])]
    print(f"csv_file:差分比較")

    print("新しく追加されたURL:")
    print(diff_new)

    print("\n削除されたURL:")
    print(diff_old)    



    import shutil

    # 既存のCSVファイルのパス
    old_file_path = "web_data.csv"

    # 新しいCSVファイルのパス
    new_file_path = "web_data_previous.csv"

    # ファイルをコピーして新しい名前で保存
    try:
        # ファイルが存在するか確認
        if os.path.exists(old_file_path):
            # ファイルをコピー
            shutil.copy(old_file_path, new_file_path)
            print(f"ファイルをコピーしました: {old_file_path} → {new_file_path}")
        else:
            print(f"ファイルが存在しません: {old_file_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

    # 通知のタイトルとメッセージ
    title = "重要なお知らせ"
    message = "こちらをクリックして詳細を確認できます"

    # 通知に設定するリンク（URL）
    url = current_url

    if not diff_new.empty:
        print(f"diff-on:{diff_new}")


    
        # 通知を表示する関数
        def show_notification():
            # 通知の表示
            notification.notify(
                title=title,
                message=message,
                app_name="通知アプリ",
                timeout=10  # 通知が表示される時間（秒）
            )
        
        # URLをFirefoxブラウザで開く関数
        def open_url_in_firefox():
            # Firefoxのオプション設定
    
            
            #Firefoxドライバを起動
            drivers = webdriver.Chrome(options=chrome_options2)
            drivers.get(url)
        
        # 通知を表示した後、URLを開く処理を行う関数
        def notify_and_open():
            show_notification()
            time.sleep(12)  # 通知が表示されるのを待つ
            open_url_in_firefox()  # FirefoxでURLを開く
        # 通知を別スレッドで表示
        notification_thread = threading.Thread(target=notify_and_open)
        notification_thread.start()
        
        # メインスレッドで他の処理を行いたい場合は、以下に記述
        # 例: メインプログラムが終了しないようにしておく
        notification_thread.join()  # スレッドが完了するまで待つ
        #driver.quit()
        # notification.notify(
        #    title = "通知テスト",
        #    message = f"ファイルが存在しません: {diff_new}",
        #    timeout = 10
        # )
        print(f"url:{url}")

    else: 
        print(f"diff-oｆｆ:{diff_new}")
        print(f"url-off:{url}")


    time.sleep(1)
    
    driver.quit()
    # WebDriverを終了
    print("run-end")

    

    
while True:
    scrape_website()
    random_sleep_time = round(random.uniform(10, 30), 3)
    time.sleep(random_sleep_time)  # 600秒（10分）待機