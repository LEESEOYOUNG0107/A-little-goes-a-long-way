# 월발 기준으로 소비 통계 보여주기
# 장예원 추가(2025.6.14)

import glob
import re
from collections import defaultdict
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정 (Windows 기준)
if platform.system() == 'Windows':
    font_name = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    font_name = 'AppleGothic'
else:  # Linux
    font_name = 'NanumGothic'

plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 가계부 지출 파일을 월 단위로 읽어, 데이터로 처리하는 parsing
def parse_expense_files():
    data = defaultdict(lambda: defaultdict(int))
    for file in glob.glob("가계부_\uc9c0\ucd9c_*.txt"):
        match = re.search(r"가계부_\uc9c0\ucd9c_(\d{4}-\d{2})-\d{2}\.txt", file)
        if not match:
            continue
        month = match.group(1)
        with open(file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "총 지출" in line:
                    continue
                parts = line.split(":")
                if len(parts) < 2:
                    continue
                category = parts[0].strip()
                amount_match = re.search(r"([\d,]+)원", parts[1])
                if amount_match:
                    amount = int(amount_match.group(1).replace(",", ""))
                    data[month][category] += amount
    return data

# 해당 월 만 찾는 함수
def get_available_months():
    months = set()
    for file in glob.glob("가계부_\uc9c0\ucd9c_*.txt"):
        match = re.search(r"가계부_\uc9c0\ucd9c_(\d{4}-\d{2})-\d{2}\.txt", file)
        if match:
            months.add(match.group(1))
    return sorted(list(months))

# 월별 내역을 통계표로 새 창에서 보여주기
def open_stats_window():
    stats_win = tk.Toplevel()
    stats_win.title("월별 소비 통계")
    stats_win.geometry("800x600")

    # 메인 프레임
    frame = ttk.Frame(stats_win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 달 선택 Combobox
    months = get_available_months()
    selected_month = tk.StringVar()
    month_box = ttk.Combobox(frame, textvariable=selected_month, values=months, state="readonly")
    month_box.pack(pady=10)

    # Treeview (grid)
    tree = ttk.Treeview(frame, columns=("category", "amount"), show="headings")
    tree.heading("category", text="카테고리")
    tree.heading("amount", text="금액 (원)")
    tree.pack(fill="both", expand=True, pady=10)

    def show_month_data(event):
        month = selected_month.get()
        data = parse_expense_files()

        if month not in data:
            messagebox.showinfo("통계", f"{month} 에 대한 지출 데이터가 없습니다.")
            return

        categories = data[month]
        sorted_items = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        # 표 생성
        for i in tree.get_children():
            tree.delete(i)

        # 표에 자료 보여주기
        for cat, amt in sorted_items:
            tree.insert("", "end", values=(cat, f"{amt:,}"))

        # 창에서 바 차트 표시
        plt.figure(figsize=(8, 5))
        plt.title(f"{month} 소비 내역")
        plt.bar([cat for cat, _ in sorted_items], [amt for _, amt in sorted_items], color='lightblue')
        plt.xticks(rotation=45)
        plt.ylabel("금액 (원)")
        plt.tight_layout()
        plt.show()

    month_box.bind("<<ComboboxSelected>>", show_month_data)