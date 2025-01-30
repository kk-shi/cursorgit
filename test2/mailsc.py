from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import csv

#

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


# WebDriverの初期化

chrome_options = ChromeOptions()
chrome_options.add_argument(f"--user-agent={USER_AGENT}")  # User-Agentを偽装
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # ボット検出を回避
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # "自動操作"のフラグ削除

#chrome_options.add_argument("--headless")  # ヘッドレスモード（ブラウザを非表示にする）
driver = webdriver.Chrome(options=chrome_options)


check_url="https://tjf.jp/"
rank=0


# 検索ページを開く（例: Googleで「不動産会社 東京」を検索）
search_url = "https://www.google.com/search?q=不動産会社+東京"
driver.get(search_url)
time.sleep(2)

# ページを少し待機（JavaScriptの読み込み待ち）

i=0
try:
    # スポンサー広告の要素を特定するCSSセレクタ（例）
    sponsor_selector = "[data-ad-block]"

    # スポンサー広告の要素を取得し、削除する
    sponsors = driver.find_elements(By.CSS_SELECTOR, sponsor_selector)

    for page in range(1, 11):
        

        for sponsor in sponsors:
            sponsor.decompose()
        
        # 残りの検索結果を取得する
        results = driver.find_elements(By.CSS_SELECTOR, ".yuRUbf")

        # 検索結果から情報を抽出する
        for result in results:
            title = result.find_element(By.TAG_NAME, "h3").text
            url = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(f"タイトル：{title}")
            print(f"URL：{url}")
            print(f"Rank_serch: {i}")

            print("---")
            i+=1
            if check_url in url:
                rank = i
                print(f"Rank_finding: {rank}")

        #element = driver.find_element(By.CSS_SELECTOR, "li.b_algo")
        #print(f"Processing: {element.text}")
        #url = [link.get_attribute("href") for link in element if link.get_attribute("href")]
        #print(url)
        #print(element.text)
        #links = element.findall(r"https?://\S+", element)
        # 次のページへ移動
        try:
            next_page_link = driver.find_element(By.LINK_TEXT, "次へ")  # "次へ"のリンクテキストは変更される可能性があります
            next_page_link.click()
            time.sleep(5)  # ページが読み込まれるまで待つ
        except:
            print("次のページが見つかりませんでした。")
            break
            
except:
    print("element が見つかりません")

time.sleep(120)
# ブラウザを閉じる
driver.quit()

