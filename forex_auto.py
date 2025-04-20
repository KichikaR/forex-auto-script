import requests
from datetime import datetime
import csv
import schedule
import time

API_KEY = "a39708e48e7645421ce05f6e"
BASE_CURRENCY = "USD"
TARGET_CURRENCY = "JPY"

def get_forex_rate():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "conversion_rates" in data:
        rate = data["conversion_rates"][TARGET_CURRENCY]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] 1 {BASE_CURRENCY} = {rate} {TARGET_CURRENCY}")
        return now, rate
    else:
        print("エラー：為替レートの取得に失敗しました")
        return None, None

def save_to_csv(timestamp, rate):
    with open("forex_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, rate])

def job():
    time_str, rate = get_forex_rate()
    if time_str and rate:
        save_to_csv(time_str, rate)

# ✅ ここを1分に変更！
schedule.every(1).minutes.do(job)

print("⏳ 自動為替取得を開始します...（Ctrl + Cで停止）")

while True:
    schedule.run_pending()
    time.sleep(1)
