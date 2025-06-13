# budget.py
import tkinter as tk
from tkinter import messagebox
import os
import glob
import re

def calculate_total_expenses():
    total = 0
    for filepath in glob.glob("가계부_지출_*.txt"):
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "총 수입" in line:
                    continue
                match = re.search(r":\s*([\d,]+)원", line)
                if match:
                    try:
                        amount = int(match.group(1).replace(",", ""))
                        total += amount
                    except:
                        continue
    return total

BUDGET_FILE = "budget.txt"

def deduct_from_budget(amount):
    current = load_budget()
    if current is not None:
        new_budget = current - amount
        if new_budget < 0:
            new_budget = 0
        save_budget_to_file(new_budget)


def load_budget():
    try:
        with open("budget.txt", "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return None
    except ValueError:
        return None



def save_budget_to_file(amount):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        f.write(str(amount))

def budget(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="월 예산 설정", font=("Arial", 18)).pack(pady=10)
    tk.Label(frame, text="예산 금액 입력 (원)").pack()

    budget_entry = tk.Entry(frame)
    budget_entry.pack()

    current_budget_var = tk.StringVar()
    current_budget_label = tk.Label(frame, textvariable=current_budget_var, font=("Arial", 14))
    current_budget_label.pack(pady=10)

    def update_current_budget_display():
        current = load_budget()
        total_expense = calculate_total_expenses()

        if current:
            remaining = current - total_expense
            current_budget_var.set(
                f"현재 월 예산: {current:,}원\n"
                f"총 지출: {total_expense:,}원\n"
                f"남은 예산: {remaining:,}원"
            )

            # ✅ 예산 10% 이하 경고
            if remaining <= current * 0.1:
                messagebox.showwarning("예산 경고", f"⚠️ 남은 예산이 10% 이하입니다!\n({remaining:,}원 남음)")

        else:
            current_budget_var.set("현재 월 예산: 없음")

    def save_budget():
        try:
            amount = int(budget_entry.get())
            if amount <= 0:
                raise ValueError

            current = load_budget()

            if current is not None and current != amount:
                confirm = messagebox.askyesno("예산 변경 확인",
                                              f"현재 예산은 {current:,}원입니다.\n정말 {amount:,}원으로 변경하시겠습니까?")
                if not confirm:
                    return  # 사용자가 취소했으면 저장하지 않음

            save_budget_to_file(amount)
            messagebox.showinfo("저장 완료", f"월 예산이 {amount:,}원으로 설정되었습니다.")
            update_current_budget_display()

        except ValueError:
            messagebox.showerror("입력 오류", "양의 정수를 입력하세요.")

    tk.Button(frame, text="저장", command=save_budget).pack(pady=10)
    update_current_budget_display()
