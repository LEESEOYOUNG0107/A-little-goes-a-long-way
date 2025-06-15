import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import platform
import glob
import re
from collections import defaultdict
from datetime import datetime
import numpy as np

def parse_yearly_expense(year):
    data = defaultdict(int)
    for file in glob.glob("가계부_지출_*.txt"):
        match = re.search(r"가계부_지출_(\d{4})-(\d{2})-(\d{2})\.txt", file)
        if not match:
            continue
        if match.group(1) != year:
            continue
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
                    data[category] += amount
    return data

def categorize_spender(expense_data):
    total = sum(expense_data.values())
    if total == 0:
        return "데이터 없음"
    ratio = {cat: amt / total for cat, amt in expense_data.items()}
    result = []
    if sum(ratio.get(k, 0) for k in ["식비", "외식", "간식"]) > 0.4:
        result.append(" 먹방파")
    if sum(ratio.get(k, 0) for k in ["학원", "교육", "도서"]) > 0.3:
        result.append(" 꿈을 쫓는 사람")
    if sum(ratio.get(k, 0) for k in ["패션", "쇼핑", "뷰티"]) > 0.3:
        result.append(" 패션리더")
    if sum(ratio.get(k, 0) for k in ["여행", "문화"]) > 0.3:
        result.append("️ 자유로운 영혼")
    if not result:
        result.append(" 균형잡힌 소비자")
    return ", ".join(result)

def predict_next_expense(year):
    monthly_totals = defaultdict(int)
    for file in glob.glob("가계부_지출_*.txt"):
        match = re.search(r"가계부_지출_(\d{4})-(\d{2})-(\d{2})\.txt", file)
        if not match:
            continue
        y, m = match.group(1), match.group(2)
        if y != year:
            continue
        with open(file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "총 지출" in line:
                    continue
                amount_match = re.search(r"([\d,]+)원", line)
                if amount_match:
                    amount = int(amount_match.group(1).replace(",", ""))
                    monthly_totals[m] += amount
    if len(monthly_totals) < 2:
        return None
    sorted_months = sorted(monthly_totals.keys())
    values = [monthly_totals[m] for m in sorted_months]
    predicted = int(np.mean(values[-3:]))
    return predicted

def open_analysis_window():
    win = tk.Toplevel()
    win.title("소비 성향 분석 및 예측")
    win.geometry("600x500")

    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')
    else:
        plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False

    frame = ttk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    year_label = ttk.Label(frame, text="연도 선택:")
    year_label.pack()

    years = sorted({re.search(r"가계부_지출_(\d{4})", f).group(1) for f in glob.glob("가계부_지출_*.txt") if re.search(r"가계부_지출_(\d{4})", f)})
    selected_year = tk.StringVar()
    year_box = ttk.Combobox(frame, textvariable=selected_year, values=years, state="readonly")
    year_box.pack(pady=10)

    result_label = ttk.Label(frame, text="분석 결과가 여기에 표시됩니다", wraplength=550, justify="left")
    result_label.pack(pady=20)

    def analyze():
        year = selected_year.get()
        if not year:
            messagebox.showwarning("입력 오류", "연도를 선택하세요.")
            return
        data = parse_yearly_expense(year)
        category = categorize_spender(data)
        prediction = predict_next_expense(year)

        msg = f" [{year}] 소비자 유형: {category}\n"
        if prediction:
            msg += f" 다음 달 예상 지출: 약 {prediction:,}원"
        else:
            msg += " 예측할 수 있는 데이터가 부족합니다."

        result_label.config(text=msg)

    analyze_btn = ttk.Button(frame, text="소비 분석 및 예측 실행", command=analyze)
    analyze_btn.pack(pady=10)
