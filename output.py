# Member B - Output Module
# Load the stored data, list entries, and generate a pie chart.

import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = os.path.join("data", "expenses.csv")

#讀取CSV檔案並回傳完整資料列表與類別統計
def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"錯誤: 找不到 {DATA_FILE}。請先執行 input.py。")
        return None, None

    #獲取檔案最後更新時間
    mtime = os.path.getmtime(DATA_FILE)
    last_updated = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"最後更新時間: {last_updated}\n")

    all_entries = []
    category_totals = {}
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                #儲存每一筆資料用於列表顯示
                all_entries.append([row["date"], row["amount"], row["category"], row["note"]])
                
                #累加類別金額用於圓餅圖
                amount = float(row["amount"])
                category_totals[row["category"]] = category_totals.get(row["category"], 0) + amount
                
        return all_entries, category_totals
    except Exception as e:
        print(f"讀取資料時發生錯誤: {e}")
        return None, None

def show_visuals(entries, totals):
    """顯示資料列表並繪製圓餅圖"""
    if not entries:
        print("沒有資料可以顯示。")
        return

    #印出列表(CMD內)
    print(f"{'日期':<12} | {'金額':<8} | {'類別':<10} | {'備註'}")
    print("-" * 50)
    for e in entries:
        print(f"{e[0]:<12} | {e[1]:<8} | {e[2]:<10} | {e[3]}")
    print("-" * 50)

    #建立繪圖視窗
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.3) #留出底部空間給表格

    #繪製圓餅圖
    labels = list(totals.keys())
    values = list(totals.values())
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True)
    ax.set_title("Expense Distribution by Category")

    #在圓餅圖下方加入資料表格
    #只顯示最後 5 筆資料，避免表格太長
    display_data = entries[-5:] if len(entries) > 5 else entries
    table_headers = ["Date", "Amount", "Category", "Note"]
    
    the_table = plt.table(cellText=display_data,
                          colLabels=table_headers,
                          loc='bottom',
                          cellLoc='center',
                          bbox=[0, -0.4, 1, 0.3]) #調整表格位置與大小

    print("\n正在產生圖表... (關閉視窗以結束程式)")
    plt.show()

if __name__ == "__main__":
    print("=== Expense Visualization (Member B) ===")
    entries, totals = load_data()
    if entries and totals:
        show_visuals(entries, totals)